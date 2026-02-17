# coding=utf-8
"""
飞书口播稿发送模块
支持发送口播稿文本和音频文件到飞书群
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict
from urllib.parse import quote
import requests


def send_script_to_feishu_webhook(
    webhook_url: str,
    script_text: str,
    audio_file_path: Optional[str] = None,
    base_url: Optional[str] = None,
    proxy_url: Optional[str] = None,
) -> bool:
    """
    通过飞书webhook发送口播稿文本和音频链接
    
    注意：飞书webhook不支持直接发送文件，只能发送文本和链接
    
    Args:
        webhook_url: 飞书webhook URL
        script_text: 口播稿文本内容
        audio_file_path: 音频文件路径（可选）
        base_url: 基础URL（用于生成音频文件链接，如GitHub Pages）
        proxy_url: 代理URL（可选）
    
    Returns:
        成功返回True，失败返回False
    """
    try:
        # 构建消息内容
        content = f"📢 **AI财经热点新闻汇总播报**\n\n{script_text}"
        
        # 如果有音频文件且配置了base_url，添加音频链接
        if audio_file_path and base_url:
            audio_filename = Path(audio_file_path).name
            # 构建音频文件URL（假设文件在output目录下）
            relative_path = str(Path(audio_file_path)).replace("\\", "/")
            # 对路径中的中文字符进行URL编码，保留 /
            encoded_path = "/".join(quote(segment, safe="") for segment in relative_path.split("/"))
            audio_url = f"{base_url.rstrip('/')}/{encoded_path}"
            content += f"\n\n🎵 **音频文件**: [点击收听]({audio_url})"
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        
        headers = {"Content-Type": "application/json"}
        proxies = None
        if proxy_url:
            proxies = {"http": proxy_url, "https": proxy_url}
        
        response = requests.post(
            webhook_url,
            headers=headers,
            json=payload,
            proxies=proxies,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ 飞书口播稿发送成功（文本）")
            if audio_file_path and base_url:
                print(f"   音频链接: {audio_url}")
            return True
        else:
            print(f"⚠️ 飞书口播稿发送失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ 飞书口播稿发送出错: {e}")
        return False


def send_script_to_feishu_api(
    app_id: str,
    app_secret: str,
    chat_id: str,
    script_text: str,
    audio_file_path: Optional[str] = None,
    proxy_url: Optional[str] = None,
) -> bool:
    """
    通过飞书开放平台API发送口播稿文本和音频文件
    
    需要配置飞书应用（App Bot），获取app_id和app_secret
    
    Args:
        app_id: 飞书应用ID
        app_secret: 飞书应用Secret
        chat_id: 群聊ID
        script_text: 口播稿文本内容
        audio_file_path: 音频文件路径（可选）
        proxy_url: 代理URL（可选）
    
    Returns:
        成功返回True，失败返回False
    """
    try:
        # 1. 获取tenant_access_token
        token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        token_payload = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        proxies = None
        if proxy_url:
            proxies = {"http": proxy_url, "https": proxy_url}
        
        token_response = requests.post(
            token_url,
            json=token_payload,
            proxies=proxies,
            timeout=30
        )
        
        if token_response.status_code != 200:
            print(f"⚠️ 获取飞书token失败: {token_response.status_code}")
            return False
        
        token_data = token_response.json()
        if token_data.get("code") != 0:
            print(f"⚠️ 获取飞书token失败: {token_data.get('msg')}")
            return False
        
        access_token = token_data["tenant_access_token"]
        
        # 2. 发送文本消息
        send_text_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        text_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        text_payload = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": f"📢 **AI财经热点新闻汇总播报**\n\n{script_text}"})
        }
        
        text_response = requests.post(
            send_text_url,
            headers=text_headers,
            json=text_payload,
            proxies=proxies,
            timeout=30
        )
        
        if text_response.status_code == 200:
            print("✅ 飞书口播稿文本发送成功")
        else:
            print(f"⚠️ 飞书口播稿文本发送失败: {text_response.status_code}")
        
        # 3. 如果有音频文件，上传并发送
        if audio_file_path and Path(audio_file_path).exists():
            # 上传文件
            upload_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
            upload_headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            with open(audio_file_path, "rb") as f:
                files = {"file": (Path(audio_file_path).name, f, "audio/mpeg")}
                data = {"file_type": "stream"}  # 音频文件类型
                
                upload_response = requests.post(
                    upload_url,
                    headers=upload_headers,
                    files=files,
                    data=data,
                    proxies=proxies,
                    timeout=60  # 文件上传可能需要更长时间
                )
            
            if upload_response.status_code == 200:
                upload_data = upload_response.json()
                if upload_data.get("code") == 0:
                    file_token = upload_data["data"]["file_token"]
                    
                    # 发送文件消息
                    send_file_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
                    file_headers = {
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                    file_payload = {
                        "receive_id": chat_id,
                        "msg_type": "file",
                        "content": json.dumps({"file_key": file_token})
                    }
                    
                    file_response = requests.post(
                        send_file_url,
                        headers=file_headers,
                        json=file_payload,
                        proxies=proxies,
                        timeout=30
                    )
                    
                    if file_response.status_code == 200:
                        print("✅ 飞书口播稿音频发送成功")
                        return True
                    else:
                        print(f"⚠️ 飞书口播稿音频发送失败: {file_response.status_code}")
                        return False
                else:
                    print(f"⚠️ 飞书文件上传失败: {upload_data.get('msg')}")
                    return False
            else:
                print(f"⚠️ 飞书文件上传失败: {upload_response.status_code}")
                return False
        
        return text_response.status_code == 200
        
    except Exception as e:
        print(f"⚠️ 飞书API发送出错: {e}")
        import traceback
        print(traceback.format_exc())
        return False


def send_script_to_feishu(
    script_file_path: str,
    audio_file_path: Optional[str] = None,
    config: Optional[Dict] = None,
) -> bool:
    """
    发送口播稿到飞书（自动选择webhook或API方式）
    
    Args:
        script_file_path: 口播稿文本文件路径
        audio_file_path: 音频文件路径（可选）
        config: 配置字典，包含：
            - feishu_webhook_url: webhook URL（webhook方式）
            - feishu_app_id: 应用ID（API方式）
            - feishu_app_secret: 应用Secret（API方式）
            - feishu_chat_id: 群聊ID（API方式）
            - base_url: 基础URL（用于生成音频链接）
            - proxy_url: 代理URL（可选）
    
    Returns:
        成功返回True，失败返回False
    """
    if not Path(script_file_path).exists():
        print(f"⚠️ 口播稿文件不存在: {script_file_path}")
        return False
    
    # 读取口播稿文本
    with open(script_file_path, "r", encoding="utf-8") as f:
        script_text = f.read()
    
    if not config:
        config = {}
    
    # 优先使用API方式（如果配置了）
    if config.get("feishu_app_id") and config.get("feishu_app_secret") and config.get("feishu_chat_id"):
        return send_script_to_feishu_api(
            app_id=config["feishu_app_id"],
            app_secret=config["feishu_app_secret"],
            chat_id=config["feishu_chat_id"],
            script_text=script_text,
            audio_file_path=audio_file_path,
            proxy_url=config.get("proxy_url"),
        )
    # 否则使用webhook方式
    elif config.get("feishu_webhook_url"):
        return send_script_to_feishu_webhook(
            webhook_url=config["feishu_webhook_url"],
            script_text=script_text,
            audio_file_path=audio_file_path,
            base_url=config.get("base_url"),
            proxy_url=config.get("proxy_url"),
        )
    else:
        print("⚠️ 未配置飞书webhook URL或API凭证，无法发送口播稿")
        return False
