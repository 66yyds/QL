from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Any

from api_client import QingLongApiClient
import time


class TaskProcessor:
    """任务处理器，负责管理定时任务的执行"""
    
    def __init__(self, api_client: QingLongApiClient):
        self.api_client = api_client
    
    def stop_tasks(self, task_ids: List[int]) -> List[Tuple[int, bool, Any]]:
        """停止指定任务"""
        results = []
        for task_id in task_ids:
            results.append(self.api_client.stop_cron_task(task_id))
        return results
    
    def run_tasks(self, task_ids: List[int], max_workers: int = 3) -> List[Tuple[int, bool, Any]]:
        """并发执行指定任务"""
        if not task_ids:
            return []
            
        print(f"准备执行 {len(task_ids)} 个定时任务...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 移除tqdm，直接使用map获取结果
            results = list(executor.map(self.api_client.run_cron_task, task_ids))
        
        return results
    
    def process_tasks(self, stop_ids: List[int], target_ids: List[int] = None, 
                     max_workers: int = 3) -> None:
        """处理任务流程：停止指定任务，查询任务状态，执行符合条件的任务"""
        # 停止指定任务
        if stop_ids:
            print(f"正在停止 {len(stop_ids)} 个任务...")
            stop_results = self.stop_tasks(stop_ids)
            self._print_results(stop_results, "停止")
        
        time.sleep(4)

        # 查询任务
        task_ids = self.api_client.query_tasks(target_ids)
        print(f"查询完成，待执行任务: {len(task_ids)}")
        
        # 执行任务
        if task_ids:
            run_results = self.run_tasks(task_ids, max_workers)
            self._print_results(run_results, "执行")
    
    def _print_results(self, results: List[Tuple[int, bool, Any]], action: str) -> None:
        """打印任务执行结果"""
        print(f"\n===== {action}结果 =====")
        success_count = 0
        
        for task_id, success, info in results:
            status = "✅ 成功" if success else "❌ 失败"
            print(f"任务 {task_id}: {status}")
            
            if success:
                success_count += 1
                print(f"  状态: {info.get('status', '未知')}")
                print(f"  消息: {info.get('message', f'{action}成功')}")
            else:
                print(f"  错误: {info}")
        
        total = len(results)
        failed = total - success_count
        print(f"\n总{action}: {total}, 成功: {success_count}, 失败: {failed}")