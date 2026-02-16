# coding=utf-8
"""
测试TTS功能
"""

from tts_generator import TTSGenerator, generate_tts_audio
from pathlib import Path

# 测试配置
test_config = {
    "enabled": True,
    "engine": "edge-tts",
    "voice": "zh-CN-XiaoxiaoNeural",  # 女声，温柔
    "rate": "+0%",
    "output_format": "mp3"
}

def test_tts_short():
    """测试短文本TTS"""
    print("=== 测试1: 短文本TTS ===")
    test_text = "你好，这是一个TTS测试。今天是2026年1月17日，欢迎收听财经新闻。"
    
    tts = TTSGenerator(test_config)
    result = tts.generate_audio(test_text, "test_short.mp3")
    
    if result and Path(result).exists():
        size = Path(result).stat().st_size
        print(f"✅ 短文本测试成功")
        print(f"   文件: {result}")
        print(f"   大小: {size / 1024:.1f} KB")
        return True
    else:
        print("❌ 短文本测试失败")
        return False

def test_tts_script():
    """测试完整口播稿TTS"""
    print("\n=== 测试2: 完整口播稿TTS ===")
    
    # 自动使用当天口播稿
    import pytz
    from datetime import datetime
    today = datetime.now(pytz.timezone("Asia/Shanghai")).strftime("%Y年%m月%d日")
    script_file = f"output/{today}/html/script/口播稿.txt"
    script_path = Path(script_file)
    
    if not script_path.exists():
        print(f"⚠️ 口播稿文件不存在: {script_file}")
        return False
    
    # 读取文件大小
    script_size = script_path.stat().st_size
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
        word_count = len(content)
    
    print(f"   口播稿字数: {word_count} 字")
    print(f"   文件大小: {script_size} 字节")
    print(f"   语音: {test_config['voice']}")
    print("   正在生成TTS音频（可能需要30-60秒）...")
    
    result = generate_tts_audio(script_file, test_config)
    
    if result and Path(result).exists():
        audio_size = Path(result).stat().st_size
        print(f"\n✅ 完整口播稿测试成功")
        print(f"   音频文件: {result}")
        print(f"   文件大小: {audio_size / 1024 / 1024:.2f} MB")
        print(f"   压缩比: {script_size / audio_size:.1f}x")
        return True
    else:
        print("❌ 完整口播稿测试失败")
        return False

def list_voices():
    """列出可用的中文语音"""
    print("\n=== 查看可用中文语音 ===")
    try:
        import asyncio
        import edge_tts
        
        async def get_voices():
            voices = await edge_tts.list_voices()
            chinese_voices = [v for v in voices if v['Locale'].startswith('zh-CN')]
            return chinese_voices
        
        voices = asyncio.run(get_voices())
        print(f"\n找到 {len(voices)} 个中文语音：\n")
        for i, voice in enumerate(voices, 1):
            name = voice['ShortName']
            gender = voice['Gender']
            locale = voice['Locale']
            print(f"{i}. {name} ({gender}) - {locale}")
        
        return True
    except Exception as e:
        print(f"⚠️ 无法列出语音: {e}")
        return False

if __name__ == "__main__":
    print("🎤 TTS功能测试\n")
    
    # 测试1: 短文本
    test1_result = test_tts_short()
    
    # 测试2: 完整口播稿
    test2_result = test_tts_script()
    
    # 列出可用语音
    list_voices()
    
    print("\n" + "="*50)
    if test1_result and test2_result:
        print("✅ 所有测试通过！")
        print(f"\n📁 生成的音频文件：")
        print(f"   • test_short.mp3 - 短文本测试")
        audio_file = Path(f"output/{today}/html/script/口播稿.mp3")
        if audio_file.exists():
            print(f"   • {audio_file} - 完整口播稿")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
    print("="*50)
