# coding=utf-8
"""
口播稿历史记录管理
"""

import json
from pathlib import Path
from datetime import datetime
import pytz


def save_script_history(script_file: str, stats: dict):
    """
    保存口播稿历史记录
    
    Args:
        script_file: 口播稿文件路径
        stats: 统计数据
    """
    script_path = Path(script_file)
    if not script_path.exists():
        return
    
    # 读取口播稿内容
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()
    
    # 创建历史记录
    beijing_tz = pytz.timezone("Asia/Shanghai")
    current_time = datetime.now(beijing_tz)
    
    history_entry = {
        "timestamp": current_time.isoformat(),
        "date": current_time.strftime("%Y年%m月%d日"),
        "time": current_time.strftime("%H:%M:%S"),
        "word_count": len(script_content),
        "keyword_groups": stats.get("keyword_groups", 0),
        "total_titles": stats.get("total_titles", 0),
        "file_path": str(script_path),
        "preview": script_content[:200] + "..." if len(script_content) > 200 else script_content
    }
    
    # 保存到历史文件
    history_file = Path("output/script_history.json")
    history_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 读取现有历史
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []
    
    # 添加新记录
    history.append(history_entry)
    
    # 只保留最近30条记录
    history = history[-30:]
    
    # 保存历史
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 口播稿历史已保存: {history_file}")


def view_script_history(limit: int = 10):
    """
    查看口播稿历史记录
    
    Args:
        limit: 显示最近N条记录
    """
    history_file = Path("output/script_history.json")
    
    if not history_file.exists():
        print("暂无历史记录")
        return
    
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)
    
    print(f"=== 口播稿历史记录（最近 {min(limit, len(history))} 条）===\n")
    
    for i, entry in enumerate(history[-limit:][::-1], 1):
        print(f"{i}. {entry['date']} {entry['time']}")
        print(f"   字数: {entry['word_count']} 字")
        print(f"   关键词组: {entry['keyword_groups']} 个")
        print(f"   处理标题: {entry['total_titles']} 条")
        print(f"   预览: {entry['preview']}")
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "view":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        view_script_history(limit)
    else:
        print("=== 口播稿历史记录工具 ===\n")
        print("用法:")
        print("  python3 script_history.py view [数量]")
        print("\n示例:")
        print("  python3 script_history.py view 10  # 查看最近10条记录")
