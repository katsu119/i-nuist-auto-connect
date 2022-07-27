import requests
import json
import os
import subprocess


class ConnectNuist:
    def __init__(self):
        self.url_login = 'http://a.nuist.edu.cn/api/v1/login'
        self.url_logout = 'http://a.nuist.edu.cn/api/v1/logout'
        self.account_info = {
            "username": "02502673344",  # 你的账户名
            "password": "02502673344",  # 密码
            "ifautologin": "1",  # 是否自动登陆，好像没太大作用
            "channel": "4",  # 运营商选择 移动2 电信3 联通4 断开0
        }
        self.inuist = requests.session()
        self.account_info['usripadd'] = self.get_ip()

    def login(self):
        ssid = self.get_current_ssid()
        if ssid != 'i-NUIST':
            print('当前网络非i-NUIST')
            exit(-1)
        status = None
        if self.get_status() == 1:
            status = 1
        else:
            self.first_page()
            res = self.second_page()
            if res['code'] == 200:
                status = 1
            else:
                status = 0
        return status

    def logout(self):
        res = self.third_page()
        if res['code'] == 200:
            status = 1
        else:
            status = 0
        return status

    def get_ip(self):
        url_ip = 'http://a.nuist.edu.cn/api/v1/ip'
        res = self.inuist.get(url_ip)
        res = json.loads(res.text)
        return res['data']

    def get_status(self):
        usr_ip = 'http://a.nuist.edu.cn/api/v1/fresh'
        data = self.account_info.copy()
        data['channel'] = '_ONELINEINFO'
        data["pagesign"] = 'thirdauth'
        data = json.dumps(data)
        data = data.replace(' ', '')
        res = self.inuist.post(self.url_login, data=data, )
        res = res.json()
        if res['code'] != 200:
            print('账户信息错误')
            print(res)
            exit(-1)
        else:
            res = res['data']['outport']
            if res == '初始出口' or res == '0.00':
                status = 0
            else:
                status = 1
            return status

    def first_page(self):
        data = self.account_info.copy()
        data['channel'] = "_GET"
        data["pagesign"] = "firstauth"
        data = json.dumps(data)
        data = data.replace(' ', '')
        res = self.inuist.post(self.url_login, data=data, )
        return res.json()

    def second_page(self):
        data = self.account_info.copy()
        data["pagesign"] = "secondauth"
        data = json.dumps(data)
        data = data.replace(' ', '')
        res = self.inuist.post(self.url_login, data=data, )
        return res.json()

    # Logout
    def third_page(self):
        data = self.account_info.copy()
        data["pagesign"] = "thirdauth"
        data["channel"] = '0'
        data = json.dumps(data)
        data = data.replace(' ', '')
        res = self.inuist.post(self.url_logout, data=data, )
        return res.json()

    @staticmethod
    def get_current_ssid():
        cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        task = subprocess.Popen([cmd, '-I'], stdout=subprocess.PIPE)
        out, err = task.communicate()
        task.wait()
        out = out.decode()
        if out != '':
            out = out.split('\n')
            out = list(map(lambda s: s.strip(), out))
            out = list(filter(lambda s: 'SSID' in s and 'BSSID' not in s, out))[0]
            out = out.split(' ')[1]
        return out


def notification(message):
    command = "osascript -e 'display notification \"{}\" with title \"I-NUIST\"'".format(message)
    os.system(command)


def main():
    inuist = ConnectNuist()
    res = inuist.login()
    if res != 1:
        notification('连接失败')
    else:
        notification('连接成功')


if __name__ == "__main__":
    main()
