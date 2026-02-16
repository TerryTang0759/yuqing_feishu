# coding=utf-8
"""
测试飞书webhook发送功能
"""

import requests
import json
from pathlib import Path

# 飞书webhook URL（从环境变量读取，避免明文泄露）
import os
WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK_URL", "")

def test_simple_message():
    """测试发送简单文本消息"""
    print("=== 测试1: 发送简单文本消息 ===")
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": "测试消息：这是一条来自TrendRadar的测试消息"
        }
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                print("✅ 测试消息发送成功")
                return True
            else:
                print(f"⚠️ 发送失败: {result.get('msg')}")
                return False
        else:
            print(f"⚠️ HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 发送出错: {e}")
        return False

def test_script_message():
    """测试发送口播稿消息"""
    print("\n=== 测试2: 发送口播稿消息 ===")
    
    # 读取口播稿
    # 自动查找最新的口播稿
    import pytz
    from datetime import datetime
    today = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y年%m月%d日")
    script_file = Path(f"output/{today}/html/script/口播稿.txt")
    if not script_file.exists():
        print(f"⚠️ 口播稿文件不存在: {script_file}")
        return False
    
    with open(script_file, "r", encoding="utf-8") as f:
        script_text = f.read()
    
    # 限制长度
    if len(script_text) > 2000:
        script_text = script_text[:2000] + "\n\n...（内容较长，已截断）"
    
    # 构建消息
    content = f"📢 **AI生成口播稿**\n\n{script_text}"
    
    # 如果有base_url，添加音频链接
    base_url = "https://joyce677.github.io/TrendRadar"
    audio_file = script_file.parent / "口播稿.mp3"
    if audio_file.exists() and base_url:
        relative_path = f"output/{today}/html/script/口播稿.mp3"
        audio_url = f"{base_url}/{relative_path}"
        content += f"\n\n🎵 **音频文件**: [点击收听]({audio_url})"
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                print("✅ 口播稿消息发送成功")
                if audio_file.exists():
                    print(f"   音频链接: {audio_url}")
                return True
            else:
                print(f"⚠️ 发送失败: {result.get('msg')}")
                return False
        else:
            print(f"⚠️ HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 发送出错: {e}")
        return False

def test_rich_text_message():
    """测试发送富文本消息（如果支持）"""
    print("\n=== 测试3: 发送富文本消息 ===")
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "📢 AI生成口播稿"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "这是一条测试消息，用于验证飞书webhook功能。"
                    }
                }
            ]
        }
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                print("✅ 富文本消息发送成功")
                return True
            else:
                print(f"⚠️ 发送失败: {result.get('msg')}")
                return False
        else:
            print(f"⚠️ HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 发送出错: {e}")
        return False

if __name__ == "__main__":
    print("🧪 飞书Webhook测试\n")
    
    # 测试1: 简单消息
    test1 = test_simple_message()
    
    # 测试2: 口播稿消息
    test2 = test_script_message()
    
    # 测试3: 富文本消息（可选）
    # test3 = test_rich_text_message()
    
    print("\n" + "="*50)
    if test1 and test2:
        print("✅ 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查配置和网络连接")
    print("="*50)
