# coding=utf-8
"""
AI新闻口播稿生成器
支持多种大模型API：OpenAI、DeepSeek、Claude等
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import pytz
import requests
import time


class AINewsScriptGenerator:
    """AI新闻口播稿生成器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_type = config.get("api_type", "openai")  # openai, deepseek, claude, custom
        self.api_key = config.get("api_key", "")
        self.api_base = config.get("api_base", "")
        self.model = config.get("model", "gpt-3.5-turbo")
        self.max_tokens = config.get("max_tokens", 2000)  # 默认增加到2000，支持更详细的口播稿
        self.temperature = config.get("temperature", 0.7)
        self.enabled = config.get("enabled", False)
        
    def generate_script(self, news_data: Dict) -> Optional[str]:
        """
        生成新闻口播稿
        
        Args:
            news_data: 包含新闻统计数据的字典
            
        Returns:
            生成的口播稿文本，失败返回None
        """
        if not self.enabled:
            print("  ⚠️ AI功能未启用")
            return None
            
        if not self.api_key:
            print("  ⚠️ AI API密钥未配置")
            return None
            
        try:
            # 构建提示词
            prompt = self._build_prompt(news_data)
            
            if not prompt:
                print("  ⚠️ 提示词构建失败")
                return None
            
            # 调用API
            print(f"  📡 正在调用AI API ({self.api_type})...")
            script = self._call_api(prompt)
            
            if not script or not script.strip():
                print(f"  ⚠️ AI API返回为空")
                return None
            
            print(f"  ✅ AI API调用成功，生成了 {len(script)} 字的口播稿")
            return script
        except Exception as e:
            import traceback
            print(f"  ⚠️ AI口播稿生成失败: {e}")
            print(f"     详细错误: {traceback.format_exc()}")
            return None
    
    def _build_prompt(self, news_data: Dict) -> str:
        """构建AI提示词"""
        stats = news_data.get("stats", [])
        total_titles = sum(stat["count"] for stat in stats)
        
        # 获取当前日期和时间（北京时间）
        beijing_tz = pytz.timezone("Asia/Shanghai")
        current_date = datetime.now(beijing_tz)
        date_str = current_date.strftime("%Y年%m月%d日")
        weekday_str = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][current_date.weekday()]
        current_hour = current_date.hour
        
        # 根据时间判断时段
        if 5 <= current_hour < 12:
            time_greeting = "早上好"
            time_period = "上午"
        elif 12 <= current_hour < 14:
            time_greeting = "中午好"
            time_period = "中午"
        elif 14 <= current_hour < 18:
            time_greeting = "下午好"
            time_period = "下午"
        elif 18 <= current_hour < 22:
            time_greeting = "晚上好"
            time_period = "晚上"
        else:
            time_greeting = "晚上好"
            time_period = "晚间"
        
        time_str = current_date.strftime("%H时%M分")
        
        # 构建新闻摘要 - 增加信息量
        news_summary = []
        # 处理所有关键词组，不限制数量
        for i, stat in enumerate(stats, 1):
            keyword = stat["word"]
            count = stat["count"]
            titles = stat.get("titles", [])
            
            # 提取更多新闻标题（增加到5-8条，不限制排名）
            top_titles = []
            for title_data in titles[:8]:  # 每个关键词组最多8条
                title = title_data.get("title", "")
                source = title_data.get("source", "")
                rank = title_data.get("ranks", [0])[0] if title_data.get("ranks") else 0
                
                # 显示排名信息
                rank_info = f"[排名{rank}]" if rank > 0 else ""
                top_titles.append(f"【{source}】{title} {rank_info}")
            
            if top_titles:
                news_summary.append(f"{i}. {keyword}相关新闻（共{count}条）：\n" + "\n".join(f"   - {t}" for t in top_titles))
        
        news_text = "\n\n".join(news_summary)
        
        prompt = f"""你是一位专业的财经新闻主播。请根据以下热点新闻，生成一段专业、详细的新闻口播稿。

**重要提示：**
- 当前北京时间：{date_str}，{weekday_str}，{time_str}
- 现在是{time_period}时段
- 口播稿开头必须使用："{time_greeting}，今天是{date_str}，{weekday_str}"
- 不要使用"中午好"、"早上好"等错误的时间问候语，必须使用"{time_greeting}"

要求：
1. 时长控制在2-3分钟（约500-800字），确保信息量充足
2. 语言专业、流畅，适合口播
3. 按重要性排序，涵盖所有主要新闻主题
4. 使用"首先"、"其次"、"此外"、"另外"、"最后"等连接词
5. 每个主题都要有具体内容，不要只是简单列举标题
6. 开头必须使用："{time_greeting}，今天是{date_str}，{weekday_str}"
7. 结尾要有总结性话语

热点新闻摘要（共{len(stats)}个主题，{total_titles}条新闻）：
{news_text}

请生成详细的口播稿，确保涵盖所有重要新闻："""
        
        return prompt
    
    def _call_api(self, prompt: str) -> str:
        """调用AI API"""
        if self.api_type == "openai" or self.api_type == "deepseek":
            return self._call_openai_api(prompt)
        elif self.api_type == "claude":
            return self._call_claude_api(prompt)
        elif self.api_type == "custom":
            return self._call_custom_api(prompt)
        else:
            raise ValueError(f"不支持的API类型: {self.api_type}")
    
    def _call_openai_api(self, prompt: str) -> str:
        """调用OpenAI兼容API（包括DeepSeek）"""
        if self.api_type == "deepseek":
            api_url = self.api_base or "https://api.deepseek.com/v1/chat/completions"
        else:
            api_url = self.api_base or "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一位专业的财经新闻主播，擅长将复杂信息转化为简洁流畅的口播稿。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    
    def _call_claude_api(self, prompt: str) -> str:
        """调用Claude API"""
        api_url = self.api_base or "https://api.anthropic.com/v1/messages"
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["content"][0]["text"].strip()
    
    def _call_custom_api(self, prompt: str) -> str:
        """调用自定义API"""
        api_url = self.api_base
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 根据实际API格式调整
        data = {
            "prompt": prompt,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        # 根据实际API响应格式调整
        return result.get("text", result.get("content", "")).strip()


def generate_news_script(news_data: Dict, config: Dict) -> Optional[str]:
    """
    生成新闻口播稿的便捷函数
    
    Args:
        news_data: 新闻统计数据
        config: AI配置字典
        
    Returns:
        口播稿文本或None
    """
    generator = AINewsScriptGenerator(config)
    return generator.generate_script(news_data)
