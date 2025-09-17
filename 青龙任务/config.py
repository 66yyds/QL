import json
import os
from typing import Optional

class Config:
    """配置类，负责加载和管理应用配置"""
    
    def __init__(self, config_path: str = '/host/ql/config/token.json'):
        self.config_path = config_path
        self.token = None
        self.ip = "0.0.0.0"
        self.load_config()
        
    def load_config(self) -> None:
        """从JSON文件加载配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as file:
                    data = json.load(file)
                    self.token = data.get('value')
                    print(f"Token加载成功: {self.token[:10]}...") if self.token else print("Token为空")
            else:
                print(f"配置文件不存在: {self.config_path}")
        except json.JSONDecodeError:
            print(f"配置文件格式错误: {self.config_path}")
        except Exception as e:
            print(f"加载配置时出错: {e}")
    
    def get_api_headers(self) -> dict:
        """获取API请求头"""
        return {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Authorization': f'Bearer {self.token}',
            'Connection': 'keep-alive',
            'Origin': f'http://{self.ip}:5700',
            'Referer': f'http://{self.ip}:5700/crontab',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
        }
    
    def get_base_url(self) -> str:
        """获取API基础URL"""
        return f'http://{self.ip}:5700'    