# coding=utf-8
"""
数字人视频生成测试脚本
用于测试数字人视频生成功能（需要配置API Key）
"""

import os
from pathlib import Path
from digital_human_generator import generate_digital_human_video

# 测试配置
test_config = {
    "enabled": True,
    "platform": "kreadoai",  # 或 "aliyun", "omnihuman"
    "api_key": os.environ.get("DIGITAL_HUMAN_API_KEY", ""),
    "api_secret": os.environ.get("DIGITAL_HUMAN_API_SECRET", ""),
    "avatar_image": "avatars/default.jpg",  # 数字人形象图片
    "video_quality": "720p",
    "output_format": "mp4"
}

def test_digital_human_generation():
    """测试数字人视频生成"""
    print("🎬 数字人视频生成测试\n")
    
    # 检查API Key
    if not test_config["api_key"]:
        print("⚠️ 未配置API Key")
        print("请设置环境变量: export DIGITAL_HUMAN_API_KEY='your_api_key'")
        return False
    
    # 检查音频文件
    audio_file = "output/2026年01月17日/script/口播稿.mp3"
    if not Path(audio_file).exists():
        print(f"⚠️ 音频文件不存在: {audio_file}")
        print("请先生成TTS音频文件")
        return False
    
    # 检查形象图片
    if test_config["avatar_image"] and not Path(test_config["avatar_image"]).exists():
        print(f"⚠️ 形象图片不存在: {test_config['avatar_image']}")
        print("请准备数字人形象图片（推荐尺寸：512x512 或 1024x1024）")
        return False
    
    print(f"📝 配置信息：")
    print(f"  • 平台: {test_config['platform']}")
    print(f"  • 音频文件: {audio_file}")
    print(f"  • 形象图片: {test_config['avatar_image']}")
    print(f"  • 视频质量: {test_config['video_quality']}")
    print()
    
    # 生成视频
    print("正在生成数字人视频...")
    print("（可能需要1-3分钟，请耐心等待）")
    print()
    
    video_file = generate_digital_human_video(
        audio_file,
        test_config,
        output_file="output/2026年01月17日/script/口播稿.mp4"
    )
    
    if video_file and Path(video_file).exists():
        file_size = Path(video_file).stat().st_size
        print(f"\n✅ 测试成功！")
        print(f"   视频文件: {video_file}")
        print(f"   文件大小: {file_size / 1024 / 1024:.2f} MB")
        return True
    else:
        print("\n❌ 测试失败")
        return False

if __name__ == "__main__":
    test_digital_human_generation()
