# coding=utf-8
"""
数字人视频生成模块
支持多个平台：KreadoAI、阿里云Wan-2.2-S2V等
"""

import os
import json
import time
from pathlib import Path
from typing import Optional, Dict
import requests


class DigitalHumanGenerator:
    """数字人视频生成器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get("enabled", False)
        self.platform = config.get("platform", "kreadoai")  # kreadoai, aliyun, omnihuman
        self.api_key = os.environ.get("DIGITAL_HUMAN_API_KEY", config.get("api_key", ""))
        self.api_secret = os.environ.get("DIGITAL_HUMAN_API_SECRET", config.get("api_secret", ""))
        self.avatar_image = config.get("avatar_image", "")  # 数字人形象图片路径
        self.output_format = config.get("output_format", "mp4")
        
        # 平台特定配置
        if self.platform == "kreadoai":
            self.api_base = config.get("api_base", "https://api.kreadoai.com")
            self.video_quality = config.get("video_quality", "720p")
        elif self.platform == "aliyun":
            self.api_base = config.get("api_base", "https://dashscope.aliyuncs.com")
            self.video_resolution = config.get("video_resolution", "720p")
    
    def generate_video(
        self, 
        audio_file: str, 
        output_file: Optional[str] = None
    ) -> Optional[str]:
        """
        生成数字人视频
        
        Args:
            audio_file: 音频文件路径
            output_file: 输出视频文件路径（可选）
        
        Returns:
            成功返回视频文件路径，失败返回None
        """
        if not self.enabled:
            return None
        
        if not self.api_key:
            print("⚠️ 数字人视频生成未启用：未配置API密钥")
            return None
        
        audio_path = Path(audio_file)
        if not audio_path.exists():
            print(f"⚠️ 音频文件不存在: {audio_file}")
            return None
        
        if self.platform == "kreadoai":
            return self._generate_with_kreadoai(audio_file, output_file)
        elif self.platform == "aliyun":
            return self._generate_with_aliyun(audio_file, output_file)
        elif self.platform == "omnihuman":
            return self._generate_with_omnihuman(audio_file, output_file)
        else:
            print(f"⚠️ 不支持的平台: {self.platform}")
            return None
    
    def _generate_with_kreadoai(
        self, 
        audio_file: str, 
        output_file: Optional[str] = None
    ) -> Optional[str]:
        """使用KreadoAI生成视频"""
        try:
            print(f"正在使用KreadoAI生成数字人视频...")
            
            # 确定输出文件路径
            if not output_file:
                audio_path = Path(audio_file)
                output_file = str(audio_path.parent / f"{audio_path.stem}.mp4")
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 1. 上传音频文件
            upload_url = f"{self.api_base}/v1/files/upload"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            
            with open(audio_file, "rb") as f:
                files = {"file": (Path(audio_file).name, f, "audio/mpeg")}
                data = {"type": "audio"}
                
                upload_response = requests.post(
                    upload_url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=60
                )
            
            if upload_response.status_code != 200:
                print(f"⚠️ 音频上传失败: {upload_response.status_code}")
                return None
            
            upload_data = upload_response.json()
            if upload_data.get("code") != 0:
                print(f"⚠️ 音频上传失败: {upload_data.get('message')}")
                return None
            
            audio_file_id = upload_data["data"]["file_id"]
            print(f"✅ 音频文件已上传: {audio_file_id}")
            
            # 2. 上传或选择数字人形象
            # 如果没有指定形象，使用默认形象
            avatar_id = self.config.get("avatar_id", "")
            if not avatar_id and self.avatar_image:
                # 上传形象图片
                with open(self.avatar_image, "rb") as f:
                    files = {"file": (Path(self.avatar_image).name, f, "image/jpeg")}
                    data = {"type": "image"}
                    
                    avatar_upload_response = requests.post(
                        upload_url,
                        headers=headers,
                        files=files,
                        data=data,
                        timeout=60
                    )
                    
                    if avatar_upload_response.status_code == 200:
                        avatar_data = avatar_upload_response.json()
                        if avatar_data.get("code") == 0:
                            avatar_id = avatar_data["data"]["file_id"]
            
            # 3. 创建视频生成任务
            create_url = f"{self.api_base}/v1/videos/create"
            create_payload = {
                "audio_file_id": audio_file_id,
                "avatar_id": avatar_id or self.config.get("default_avatar_id", ""),
                "quality": self.video_quality,
                "format": self.output_format
            }
            
            create_response = requests.post(
                create_url,
                headers=headers,
                json=create_payload,
                timeout=30
            )
            
            if create_response.status_code != 200:
                print(f"⚠️ 创建视频任务失败: {create_response.status_code}")
                return None
            
            create_data = create_response.json()
            if create_data.get("code") != 0:
                print(f"⚠️ 创建视频任务失败: {create_data.get('message')}")
                return None
            
            video_task_id = create_data["data"]["task_id"]
            print(f"✅ 视频生成任务已创建: {video_task_id}")
            
            # 4. 轮询任务状态
            status_url = f"{self.api_base}/v1/videos/status/{video_task_id}"
            max_wait_time = 300  # 最大等待5分钟
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                status_response = requests.get(
                    status_url,
                    headers=headers,
                    timeout=30
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    if status_data.get("code") == 0:
                        task_status = status_data["data"]["status"]
                        
                        if task_status == "completed":
                            video_url = status_data["data"]["video_url"]
                            print(f"✅ 视频生成完成: {video_url}")
                            
                            # 5. 下载视频
                            video_response = requests.get(video_url, timeout=120)
                            if video_response.status_code == 200:
                                with open(output_path, "wb") as f:
                                    f.write(video_response.content)
                                
                                file_size = output_path.stat().st_size
                                print(f"✅ 数字人视频已生成: {output_path} ({file_size / 1024 / 1024:.2f} MB)")
                                return str(output_path)
                            else:
                                print(f"⚠️ 视频下载失败: {video_response.status_code}")
                                return None
                        elif task_status == "failed":
                            error_msg = status_data["data"].get("error", "未知错误")
                            print(f"⚠️ 视频生成失败: {error_msg}")
                            return None
                        elif task_status in ["pending", "processing"]:
                            print(f"⏳ 视频生成中... ({task_status})")
                            time.sleep(5)  # 等待5秒后重试
                        else:
                            print(f"⚠️ 未知任务状态: {task_status}")
                            return None
                    else:
                        print(f"⚠️ 查询任务状态失败: {status_data.get('message')}")
                        return None
                else:
                    print(f"⚠️ 查询任务状态失败: {status_response.status_code}")
                    return None
            
            print("⚠️ 视频生成超时")
            return None
            
        except Exception as e:
            print(f"⚠️ KreadoAI视频生成出错: {e}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def _generate_with_aliyun(
        self, 
        audio_file: str, 
        output_file: Optional[str] = None
    ) -> Optional[str]:
        """使用阿里云Wan-2.2-S2V生成视频"""
        try:
            print(f"正在使用阿里云Wan-2.2-S2V生成数字人视频...")
            
            # 确定输出文件路径
            if not output_file:
                audio_path = Path(audio_file)
                output_file = str(audio_path.parent / f"{audio_path.stem}.mp4")
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 读取音频文件
            with open(audio_file, "rb") as audio_data:
                # 读取形象图片
                if not self.avatar_image or not Path(self.avatar_image).exists():
                    print("⚠️ 未指定数字人形象图片")
                    return None
                
                with open(self.avatar_image, "rb") as image_data:
                    # 调用阿里云API
                    api_url = f"{self.api_base}/api/v1/services/aigc/video-generation/generation"
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "multipart/form-data"
                    }
                    
                    files = {
                        "image": ("avatar.jpg", image_data, "image/jpeg"),
                        "audio": ("audio.mp3", audio_data, "audio/mpeg")
                    }
                    
                    data = {
                        "model": "wan2.2-s2v",
                        "resolution": self.video_resolution
                    }
                    
                    response = requests.post(
                        api_url,
                        headers=headers,
                        files=files,
                        data=data,
                        timeout=180
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("code") == "Success":
                            video_url = result["data"]["video_url"]
                            
                            # 下载视频
                            video_response = requests.get(video_url, timeout=120)
                            if video_response.status_code == 200:
                                with open(output_path, "wb") as f:
                                    f.write(video_response.content)
                                
                                file_size = output_path.stat().st_size
                                print(f"✅ 数字人视频已生成: {output_path} ({file_size / 1024 / 1024:.2f} MB)")
                                return str(output_path)
                            else:
                                print(f"⚠️ 视频下载失败: {video_response.status_code}")
                                return None
                        else:
                            print(f"⚠️ 视频生成失败: {result.get('message')}")
                            return None
                    else:
                        print(f"⚠️ API调用失败: {response.status_code}")
                        return None
                        
        except Exception as e:
            print(f"⚠️ 阿里云视频生成出错: {e}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def _generate_with_omnihuman(
        self, 
        audio_file: str, 
        output_file: Optional[str] = None
    ) -> Optional[str]:
        """使用OmniHuman 1.5生成视频"""
        # TODO: 实现OmniHuman集成
        print("⚠️ OmniHuman平台暂未实现")
        return None


def generate_digital_human_video(
    audio_file: str,
    config: Dict,
    output_file: Optional[str] = None
) -> Optional[str]:
    """
    生成数字人视频
    
    Args:
        audio_file: 音频文件路径
        config: 数字人视频配置字典
        output_file: 输出视频文件路径（可选）
    
    Returns:
        成功返回视频文件路径，失败返回None
    """
    generator = DigitalHumanGenerator(config)
    return generator.generate_video(audio_file, output_file)
