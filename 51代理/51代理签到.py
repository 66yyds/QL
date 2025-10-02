import os
import requests
import traceback




"""
环境变量名称:wuyi
1111#222
账号#密码
如上示例，#分割,一个账号一行
登录完成运行脚本后删除变量，重新运行脚本即可！
"""



x = "wuyi.so"
def download_xingkong_so(url):
    """下载so文件"""
    try:
        print(f"开始下载{x}...")
        # 增加超时设置，防止无限等待
        response = requests.get(url, stream=True, verify=False, timeout=30)
        response.raise_for_status()  # 检查HTTP错误状态
        
        # 获取文件大小用于进度显示
        file_size = int(response.headers.get('Content-Length', 0))
        downloaded_size = 0
        
        with open(x, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024*16):  # 增大块大小提高下载效率
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # 显示下载进度
                    if file_size > 0:
                        progress = (downloaded_size / file_size) * 100
                        print(f"下载进度: {progress:.2f}%", end='\r')
        
        print(f"\n{x}下载成功")
        return True
    except requests.exceptions.Timeout:
        print("下载超时，请检查网络连接")
        return False
    except Exception as e:
        print(f"下载失败: {str(e)}")
        print("错误详情:", traceback.format_exc())
        return False

def check_download_and_import():
    """检查文件，不存在则下载，然后尝试导入"""
    url = "https://gh.jasonzeng.dev/https://raw.githubusercontent.com/66yyds/QL/7c4e6439b39eb71a0230248e19f0dac2bcdcd75b/51%E4%BB%A3%E7%90%86/wuyi.so"

    # 检查文件是否存在
    if not os.path.exists(x):
        print(f"{x}不存在，准备下载...")
        if not download_xingkong_so(url):
            print("无法下载文件，无法继续")
            return None
    else:
        # 检查文件是否为空或过小
        file_size = os.path.getsize(x)
        if file_size == 0 or file_size < 1024:
            os.remove(x)
            if not download_xingkong_so(url):
                print("无法下载文件，无法继续")
                return None
    
    try:
        # 尝试导入模块
        import wuyi

        return wuyi
    except ImportError as e:
        print("错误详情:", traceback.format_exc())
        return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        print("错误详情:", traceback.format_exc())
        return None

def main():
    
    xx = check_download_and_import()
    if xx:
        try:
            xx.main()
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()


