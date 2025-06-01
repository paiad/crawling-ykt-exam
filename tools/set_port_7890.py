import winreg
import ctypes


def set_proxy(enable=True, ip="127.0.0.1", port="8080"):
    proxy_server = f"{ip}:{port}"
    INTERNET_SETTINGS = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'

    try:
        print(f"[INFO] 开始设置代理: {'开启' if enable else '关闭'}，地址: {proxy_server if enable else '无'}")

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, INTERNET_SETTINGS, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, 'ProxyEnable', 0, winreg.REG_DWORD, 1 if enable else 0)
            if enable:
                winreg.SetValueEx(key, 'ProxyServer', 0, winreg.REG_SZ, proxy_server)

        # 通知系统代理设置已经更改
        internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
        internet_set_option(0, 39, 0, 0)
        internet_set_option(0, 37, 0, 0)

        print("[SUCCESS] 代理设置成功！")

    except Exception as e:
        print(f"[ERROR] 设置代理失败: {e}")


#  设置代理为127.0.0.1:7890
set_proxy(enable=True, ip="127.0.0.1", port="7890")


