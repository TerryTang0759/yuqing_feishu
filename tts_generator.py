# coding=utf-8
"""
TTS语音合成模块
支持多种TTS引擎：edge-tts, gTTS, pyttsx3
"""

import os
import asyncio
from pathlib import Path
from typing import Optional, Dict
import re


# 尝试导入edge-tts（推荐，免费且质量好）
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# 尝试导入gTTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# 尝试导入pyttsx3（离线TTS）
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class TTSGenerator:
    """TTS语音合成器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get("enabled", False)
        self.engine = config.get("engine", "edge-tts")
        self.voice = config.get("voice", "zh-CN-XiaoxiaoNeural")  # edge-tts默认中文女声
        self.rate = config.get("rate", "+0%")  # 语速
        self.output_format = config.get("output_format", "mp3")
        
        # 检查引擎可用性
        if self.enabled:
            if self.engine == "edge-tts" and not EDGE_TTS_AVAILABLE:
                print("⚠️ edge-tts未安装，TTS功能将禁用。安装命令: pip install edge-tts")
                self.enabled = False
            elif self.engine == "gtts" and not GTTS_AVAILABLE:
                print("⚠️ gTTS未安装，TTS功能将禁用。安装命令: pip install gtts")
                self.enabled = False
            elif self.engine == "pyttsx3" and not PYTTSX3_AVAILABLE:
                print("⚠️ pyttsx3未安装，TTS功能将禁用。安装命令: pip install pyttsx3")
                self.enabled = False
    
    async def generate_with_edge_tts(self, text: str, output_file: str) -> bool:
        """使用edge-tts生成语音"""
        try:
            # 清理文本（移除Markdown格式标记）
            clean_text = self._clean_text(text)
            
            # 检查文本长度，如果太长则分段
            max_length = 5000  # edge-tts单次限制
            if len(clean_text) > max_length:
                print(f"⚠️ 文本过长({len(clean_text)}字)，将分段处理")
                return await self._generate_long_text_edge_tts(clean_text, output_file)
            
            # 生成语音
            communicate = edge_tts.Communicate(
                text=clean_text,
                voice=self.voice,
                rate=self.rate
            )
            
            await communicate.save(output_file)
            return True
            
        except Exception as e:
            print(f"⚠️ edge-tts生成失败: {e}")
            return False
    
    async def _generate_long_text_edge_tts(self, text: str, output_file: str) -> bool:
        """分段处理长文本"""
        try:
            # 按段落分割
            paragraphs = re.split(r'\n\n+', text)
            audio_files = []
            
            for i, para in enumerate(paragraphs):
                if not para.strip():
                    continue
                
                para_file = f"{output_file}.part{i}.mp3"
                communicate = edge_tts.Communicate(
                    text=para.strip(),
                    voice=self.voice,
                    rate=self.rate
                )
                await communicate.save(para_file)
                audio_files.append(para_file)
            
            # 合并音频文件（需要ffmpeg）
            if len(audio_files) > 1:
                try:
                    import subprocess
                    # 创建文件列表
                    file_list = f"{output_file}.list.txt"
                    with open(file_list, "w") as f:
                        for af in audio_files:
                            f.write(f"file '{af}'\n")
                    
                    # 使用ffmpeg合并
                    subprocess.run([
                        "ffmpeg", "-f", "concat", "-safe", "0",
                        "-i", file_list, "-c", "copy", output_file
                    ], check=True, capture_output=True)
                    
                    # 清理临时文件
                    for af in audio_files:
                        Path(af).unlink(missing_ok=True)
                    Path(file_list).unlink(missing_ok=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("⚠️ ffmpeg未安装，无法合并音频，将使用第一段音频")
                    if audio_files:
                        Path(output_file).unlink(missing_ok=True)
                        Path(audio_files[0]).rename(output_file)
            else:
                if audio_files:
                    Path(output_file).unlink(missing_ok=True)
                    Path(audio_files[0]).rename(output_file)
            
            return True
            
        except Exception as e:
            print(f"⚠️ 长文本TTS生成失败: {e}")
            return False
    
    def generate_with_gtts(self, text: str, output_file: str) -> bool:
        """使用gTTS生成语音"""
        try:
            clean_text = self._clean_text(text)
            tts = gTTS(text=clean_text, lang='zh-cn', slow=False)
            tts.save(output_file)
            return True
        except Exception as e:
            print(f"⚠️ gTTS生成失败: {e}")
            return False
    
    def generate_with_pyttsx3(self, text: str, output_file: str) -> bool:
        """使用pyttsx3生成语音（不支持直接保存为文件，需要转换）"""
        try:
            engine = pyttsx3.init()
            
            # 设置语速
            engine.setProperty('rate', 150)
            
            # 设置音量
            engine.setProperty('volume', 0.9)
            
            # 尝试设置中文语音（如果有）
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            clean_text = self._clean_text(text)
            engine.save_to_file(clean_text, output_file.replace('.mp3', '.wav'))
            engine.runAndWait()
            
            # 如果需要mp3格式，需要转换（这里只保存为wav）
            return True
        except Exception as e:
            print(f"⚠️ pyttsx3生成失败: {e}")
            return False
    
    def _clean_text(self, text: str) -> str:
        """清理文本，移除Markdown格式"""
        # 移除加粗标记
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        # 移除其他Markdown标记
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # 保留段落结构
        return text.strip()
    
    def generate_audio(self, text: str, output_file: str) -> Optional[str]:
        """
        生成语音文件
        
        Args:
            text: 要转换的文本
            output_file: 输出文件路径
        
        Returns:
            成功返回文件路径，失败返回None
        """
        if not self.enabled:
            return None
        
        if not text or not text.strip():
            print("⚠️ 文本为空，无法生成TTS")
            return None
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if self.engine == "edge-tts":
                # 使用异步方式
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                success = loop.run_until_complete(
                    self.generate_with_edge_tts(text, str(output_path))
                )
            elif self.engine == "gtts":
                success = self.generate_with_gtts(text, str(output_path))
            elif self.engine == "pyttsx3":
                success = self.generate_with_pyttsx3(text, str(output_path))
            else:
                print(f"⚠️ 不支持的TTS引擎: {self.engine}")
                return None
            
            if success and output_path.exists():
                file_size = output_path.stat().st_size
                print(f"✅ TTS音频已生成: {output_path} ({file_size / 1024:.1f} KB)")
                return str(output_path)
            else:
                print("⚠️ TTS音频生成失败")
                return None
                
        except Exception as e:
            print(f"⚠️ TTS生成出错: {e}")
            return None


def generate_tts_audio(script_file: str, config: Dict) -> Optional[str]:
    """
    为口播稿生成TTS音频
    
    Args:
        script_file: 口播稿文件路径
        config: TTS配置字典
    
    Returns:
        成功返回音频文件路径，失败返回None
    """
    script_path = Path(script_file)
    if not script_path.exists():
        print(f"⚠️ 口播稿文件不存在: {script_file}")
        return None
    
    # 读取口播稿内容
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()
    
    # 生成TTS
    tts = TTSGenerator(config)
    output_file = script_path.parent / f"{script_path.stem}.{config.get('output_format', 'mp3')}"
    
    return tts.generate_audio(script_content, str(output_file))


if __name__ == "__main__":
    # 测试TTS功能
    test_text = "你好，这是一个TTS测试。今天天气真好。"
    test_config = {
        "enabled": True,
        "engine": "edge-tts",
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "+0%",
        "output_format": "mp3"
    }
    
    tts = TTSGenerator(test_config)
    result = tts.generate_audio(test_text, "test_output.mp3")
    if result:
        print(f"✅ 测试成功，音频文件: {result}")
    else:
        print("❌ 测试失败")
