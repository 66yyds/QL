import os
import requests
import traceback

# 多账号信息，使用#分隔不同账号，&分隔用户名和密码
# 使用换行分隔，
accounts = """
123456789&123456789
abc&abc
"""

def download_xingkong_so(url):
    """下载xingkong.so文件"""
    try:
        response = requests.get(url, stream=True, verify=False, timeout=30)
        response.raise_for_status() 
        
        file_size = int(response.headers.get('Content-Length', 0))
        downloaded_size = 0
        
        with open("xingkong.so", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024*16):  
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)

                    if file_size > 0:
                        progress = (downloaded_size / file_size) * 100
                        print(f"下载进度: {progress:.2f}%", end='\r')
        
        print("\nxingkong.so下载成功")
        return True
    except requests.exceptions.Timeout:
        print("下载超时，请检查网络连接")
        return False
    except Exception as e:
        print(f"下载失败: {str(e)}")
        print("错误详情:", traceback.format_exc())
        return False

def check_download_and_import():
    url = "https://github.com/66yyds/QL/blob/main/%E6%98%9F%E7%A9%BA%E4%BB%A3%E7%90%86/xingkong.so?raw=true"
    if not os.path.exists("xingkong.so"):
        print("xingkong.so不存在，准备下载...")
        if not download_xingkong_so(url):
            print("无法下载文件，无法继续")
            return None
    else:
        if os.path.getsize("xingkong.so") == 0:
            print("xingkong.so文件为空，重新下载...")
            os.remove("xingkong.so")
            if not download_xingkong_so(url):
                print("无法下载文件，无法继续")
                return None
    try:
        import xingkong
        return xingkong
    except ImportError as e:
        return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

def parse_accounts(accounts_str, account_sep='\n', user_pass_sep='&'):
    accounts_list = []

    for account in accounts_str.split(account_sep):
        account = account.strip()
        if not account:
            continue
        if user_pass_sep in account:
            username, password = account.split(user_pass_sep, 1)
            accounts_list.append((username.strip(), password.strip()))
        else:
            print(f"账号格式错误: {account}，缺少分隔符{user_pass_sep}")
    return accounts_list

def main():
    xingkong_module = check_download_and_import()
    if xingkong_module:
        # 解析账号列表
        accounts_list = parse_accounts(accounts)
        print(f"共解析到{len(accounts_list)}个账号，开始处理...")
        
        # 遍历所有账号进行登录
        for i, (username, password) in enumerate(accounts_list, 1):
            print(f"\n处理第{i}个账号: {username}")
            try:
                login_result = xingkong_module.xklogin(username, password)
            except Exception as e:
                print(f"登录过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main()
    
