import requests
import json


class ConnectNuist:
    def __init__(self):
        self.url_login = 'http://a.nuist.edu.cn/api/v1/login'
        self.url_logout = 'http://a.nuist.edu.cn/api/v1/logout'
        self.account_info = {
            "username": "",  # 你的账户名
            "password": "12345678",  # 密码
            "ifautologin": "12345678",  # 是否自动登陆，好像没太大作用
            "channel": "4",  # 运营商选择 移动2 电信3 联通4
        }
        self.inuist = requests.session()
        self.account_info['usripadd'] = self.get_ip()

    def login(self):
        self.first_page()
        res = self.second_page()
        print(res['message'])
        return res

    def logout(self):
        res = self.third_page()
        print(res['message'])
        return res

    def get_ip(self):
        url_ip = 'http://a.nuist.edu.cn/api/v1/ip'
        res = self.inuist.get(url_ip)
        res = json.loads(res.text)
        return res['data']

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


if __name__ == "__main__":
    inuist = ConnectNuist()
    inuist.login()
