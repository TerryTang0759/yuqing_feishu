# coding=utf-8
"""
口播稿导出工具
支持导出为Markdown、纯文本等格式
"""

import json
import os
from pathlib import Path
from datetime import datetime
import pytz


def export_script_to_markdown(script_file: str, output_file: str = None):
    """
    将口播稿导出为Markdown格式
    
    Args:
        script_file: 口播稿文件路径
        output_file: 输出文件路径（可选）
    """
    script_path = Path(script_file)
    if not script_path.exists():
        print(f"❌ 文件不存在: {script_file}")
        return None
    
    # 读取口播稿
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()
    
    # 生成Markdown内容
    beijing_tz = pytz.timezone("Asia/Shanghai")
    current_time = datetime.now(beijing_tz)
    
    # 计算预计时长（更精确）
    word_count = len(script_content)
    reading_speed = 200  # 字/分钟（正常语速）
    estimated_minutes = max(1, word_count // reading_speed)
    
    # 格式化口播稿内容（保留段落结构）
    formatted_content = script_content.strip()
    
    markdown = f"""# 📢 财经新闻口播稿

<div align="center">

**生成时间** | **字数统计** | **预计时长**
--- | --- | ---
{current_time.strftime("%Y年%m月%d日<br>%H:%M:%S")} | {word_count} 字 | 约 {estimated_minutes} 分钟

</div>

---

{formatted_content}

---

<div align="center">

*本口播稿由AI自动生成，仅供参考*

</div>
"""
    
    # 确定输出文件路径
    if not output_file:
        output_file = script_path.parent / f"{script_path.stem}.md"
    else:
        output_file = Path(output_file)
    
    # 保存Markdown文件
    output_file.write_text(markdown, encoding="utf-8")
    print(f"✅ Markdown文件已导出: {output_file}")
    
    return str(output_file)


def list_all_scripts(script_dir: str = "output"):
    """
    列出所有口播稿文件
    
    Args:
        script_dir: 输出目录
    """
    script_path = Path(script_dir)
    script_files = list(script_path.rglob("script/口播稿.txt"))
    
    if not script_files:
        print("未找到任何口播稿文件")
        return []
    
    print(f"找到 {len(script_files)} 个口播稿文件：\n")
    for i, script_file in enumerate(sorted(script_files, reverse=True), 1):
        stat = script_file.stat()
        size = stat.st_size
        mtime = datetime.fromtimestamp(stat.st_mtime)
        
        with open(script_file, "r", encoding="utf-8") as f:
            content = f.read()
            word_count = len(content)
        
        print(f"{i}. {script_file}")
        print(f"   时间: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   字数: {word_count} 字")
        print(f"   大小: {size} 字节")
        print()
    
    return script_files


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        script_file = sys.argv[1]
        export_script_to_markdown(script_file)
    else:
        print("=== 口播稿导出工具 ===\n")
        print("用法:")
        print("  python3 export_script.py <口播稿文件路径>")
        print("\n示例:")
        print("  python3 export_script.py output/YYYY年MM月DD日/html/script/口播稿.txt")
        print("\n列出所有口播稿:")
        list_all_scripts()
