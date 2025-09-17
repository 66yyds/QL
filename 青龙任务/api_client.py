import requests
import time
from typing import Dict, List, Tuple, Any
from config import Config
import json

class QingLongApiClient:
    """青龙面板API客户端"""
    
    def __init__(self, config: Config):
        self.config = config
        self.headers = config.get_api_headers()
        self.base_url = config.get_base_url()
    
    def _send_request(self, method: str, endpoint: str, params: dict = None, 
                     json_data: Any = None) -> Tuple[bool, Any]:
        """发送HTTP请求并处理响应"""
        url = f"{self.base_url}{endpoint}"
        try:

                
            response = requests.request(
                method,
                url,
                headers=self.headers,
                json=json_data,
                verify=False,
                timeout=10
            )
            #print(response.text)
            response.raise_for_status()
            return True, response.json()
        except requests.exceptions.RequestException as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    def stop_cron_task(self, task_id: int) -> Tuple[int, bool, Any]:
        """停止定时任务"""
        endpoint = f"/open/crons/stop?t={int(time.time() * 1000)}"
        success, result = self._send_request("PUT", endpoint, json_data=[task_id])
        return task_id, success, result
    
    def run_cron_task(self, task_id: int) -> Tuple[int, bool, Any]:
        """运行定时任务"""
        endpoint = "/open/crons/run"
        success, result = self._send_request("PUT", endpoint, json_data=[task_id])
        return task_id, success, result
    
    def query_tasks(self, target_ids: List[int] = None) -> List[int]:
        """查询任务状态并返回符合条件的任务ID"""
        if target_ids is None:
            target_ids = []
            
        filters = {}
        query_string = json.dumps({"filters": None, "sorts": None, "filterRelation": "and"})
        endpoint = f"/open/crons?searchValue=&page=1&size=20&filters={json.dumps(filters)}&queryString={query_string}&t={int(time.time() * 1000)}"
        
        success, result = self._send_request("GET", endpoint)
        task_ids = []
        
        if success and 'data' in result and 'data' in result['data']:
            print(f"\n===== 任务查询结果 =====")
            for task in result['data']['data']:
                task_id = task['id']
                status = task['status']
                name = task['name']
                
                if status != 0:
                    print(f"停止 {name} (ID: {task_id})")
                    if not target_ids or task_id in target_ids:
                        task_ids.append(task_id)
                else:
                    print(f"运行中 {name} (ID: {task_id})")
        else:
            print(f"查询任务失败: {result}")
            
        return task_ids    