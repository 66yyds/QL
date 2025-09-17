from config import Config
from api_client import QingLongApiClient
from task_processor import TaskProcessor

def main():
    # 加载配置
    config = Config()
    
    # 初始化API客户端
    api_client = QingLongApiClient(config)
    
    # 初始化任务处理器
    task_processor = TaskProcessor(api_client)
    
    # 配置任务参数
    stop_ids = [51]  # 要停止的任务ID列表
    target_ids = [51]  # 目标任务ID列表，为空则处理所有符合条件的任务
    
    # 处理任务
    task_processor.process_tasks(stop_ids, target_ids)

if __name__ == "__main__":
    main()    