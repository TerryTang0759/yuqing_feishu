# coding=utf-8
"""
测试AI API连接和口播稿生成功能
"""

import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ai_news_script_generator import AINewsScriptGenerator
except ImportError:
    print("❌ 无法导入 ai_news_script_generator 模块")
    sys.exit(1)

def test_api():
    """测试API连接"""
    print("=== AI API 连接测试 ===\n")
    
    # 从环境变量读取配置
    api_key = os.environ.get("AI_API_KEY", "")
    api_type = os.environ.get("AI_API_TYPE", "deepseek")
    model = os.environ.get("AI_MODEL", "deepseek-chat")
    
    if not api_key:
        print("❌ 未找到 AI_API_KEY 环境变量")
        print("\n请设置环境变量：")
        print("export AI_API_KEY='your_api_key_here'")
        print("export AI_API_TYPE='deepseek'")
        print("export AI_MODEL='deepseek-chat'")
        return False
    
    print(f"✅ API密钥已配置")
    print(f"✅ API类型: {api_type}")
    print(f"✅ 模型: {model}\n")
    
    # 创建配置
    config = {
        "enabled": True,
        "api_type": api_type,
        "api_key": api_key,
        "api_base": "",
        "model": model,
        "max_tokens": 500,  # 测试时使用较小的token数
        "temperature": 0.7
    }
    
    # 创建生成器
    generator = AINewsScriptGenerator(config)
    
    # 测试数据
    test_data = {
        "stats": [
            {
                "word": "芯片 半导体 集成电路",
                "count": 3,
                "titles": [
                    {"title": "中国芯片迎来最大IPO", "source": "百度热搜", "ranks": [1]},
                    {"title": "我国芯片制造核心装备取得重要突破", "source": "财联社", "ranks": [2]},
                    {"title": "性能突破性提升！我国攻克半导体材料世界难题", "source": "财联社", "ranks": [3]}
                ]
            },
            {
                "word": "A股 上证指数 深证成指 创业板",
                "count": 2,
                "titles": [
                    {"title": "A股为何四连跌退守4100点", "source": "今日头条", "ranks": [15]},
                    {"title": "半导体封测概念股两日累计涨超30%", "source": "财联社", "ranks": [10]}
                ]
            }
        ],
        "total_titles": 5
    }
    
    print("正在测试API连接和口播稿生成...\n")
    
    try:
        script = generator.generate_script(test_data)
        
        if script:
            print("=" * 60)
            print("✅ 测试成功！生成的口播稿：")
            print("=" * 60)
            print(script)
            print("=" * 60)
            print("\n✅ API连接正常，功能可用！")
            return True
        else:
            print("❌ 口播稿生成失败（返回为空）")
            return False
            
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        print("\n可能的原因：")
        print("1. API密钥无效或已过期")
        print("2. 网络连接问题")
        print("3. API服务暂时不可用")
        print("4. 余额不足")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
