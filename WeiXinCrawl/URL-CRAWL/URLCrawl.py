import re
from urllib.request import quote
import time
from selenium import webdriver
import random
from bs4 import BeautifulSoup
import redis
from PIL import Image
from io import BytesIO
import os
import matplotlib.pyplot as plt
import sys
sys.path.append('E:\DataAnalysis\project\WeiXinCrawl\Setting')
from useragent import *

class urlCrawl:

    def __init__(self):
        self.keyword = '人工智能'
        self.url = 'https://weixin.sogou.com/weixin?query='+quote(self.keyword)+'&_sug_type_=&s_from=input&_sug_=n&type=2&page=1&ie=utf8'
        options = webdriver.ChromeOptions() # 创建chrome参数对象
        options.add_argument('headless')  # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        options.add_argument('--user-agent="' + random.choice(MY_USER_AGENT) + '"')  # 设置请求头
        self.driver = webdriver.Chrome(chrome_options=options)  # 创建chrome无界面对象
        self.driver.maximize_window()  # 最大化窗口
        self.conn = redis.Redis(host="127.0.0.1", port=6379,db=1)
        #SUV=00C27A7ADDD95B725C653FB393992213; CXID=0089016E2220A498DB69F29DBB90CE09; SUID=61A8747B3965860A5C704FEA000D062D; ad=Xlllllllll2tZz71lllllVCa@GclllllWT7elyllllwllllljllll5@@@@@@@@@@; wuid=AAGYRRh1JwAAAAqGCmKfWQ4AGwY=; IPLOC=CN1100; sct=18; SNUID=2196883513169DE5B1B8A76D1386AD34; pgv_pvi=6027654144; sw_uuid=8302102938; ssuid=9935786087; LSTMV=283%2C284; LCLKINT=12473; ABTEST=0|1563351567|v1; weixinIndexVisited=1; JSESSIONID=aaaXuaoK5nHPH7k2B66Qw; PHPSESSID=222se1o9q7ipad5m8p6jod47e0; ppinf=5|1565664376|1566873976|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTYlOUMlQTglRTYlOUMlQUMlRTYlQjAlQjQlRTYlQkElOTB8Y3J0OjEwOjE1NjU2NjQzNzZ8cmVmbmljazozNjolRTYlOUMlQTglRTYlOUMlQUMlRTYlQjAlQjQlRTYlQkElOTB8dXNlcmlkOjQ0Om85dDJsdUQ4djdFWk1KdW9WXzBGTG9ZSW5rY0lAd2VpeGluLnNvaHUuY29tfA; pprdig=pUOwdqkvr_ztP4_kR-zaN0KMN9t3JWgM1v5BRGzV_Z-qjYnrdUiNR6M-vpAaBOL8IC1l9jj9lTo1W4jET0l4EUqkpnNL_7L58i5JlDyQiEuTVZWUWVH4lOU4TWh4loXl-dbFQEWeHu0bYhStfEmzQRZXCy7XIHP52fy2eWckayM; sgid=09-42566599-AV1SJHh5RfDic44AFycbg794; ppmdig=1565664376000000661b5edc16a1e561a14bfa97fda2f661

    def getCookies(self):
        cookieslist = []
        str_ = 'SUV=00C27A7ADDD95B725C653FB393992213; CXID=0089016E2220A498DB69F29DBB90CE09; SUID=61A8747B3965860A5C704FEA000D062D; ad=Xlllllllll2tZz71lllllVCa@GclllllWT7elyllllwllllljllll5@@@@@@@@@@; wuid=AAGYRRh1JwAAAAqGCmKfWQ4AGwY=; IPLOC=CN1100; sct=19; SNUID=2196883513169DE5B1B8A76D1386AD34; pgv_pvi=6027654144; sw_uuid=8302102938; ssuid=9935786087; LSTMV=283%2C284; LCLKINT=12473; ABTEST=0|1563351567|v1; weixinIndexVisited=1; JSESSIONID=aaaXuaoK5nHPH7k2B66Qw; PHPSESSID=222se1o9q7ipad5m8p6jod47e0; ppinf=5|1565664376|1566873976|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTYlOUMlQTglRTYlOUMlQUMlRTYlQjAlQjQlRTYlQkElOTB8Y3J0OjEwOjE1NjU2NjQzNzZ8cmVmbmljazozNjolRTYlOUMlQTglRTYlOUMlQUMlRTYlQjAlQjQlRTYlQkElOTB8dXNlcmlkOjQ0Om85dDJsdUQ4djdFWk1KdW9WXzBGTG9ZSW5rY0lAd2VpeGluLnNvaHUuY29tfA; pprdig=pUOwdqkvr_ztP4_kR-zaN0KMN9t3JWgM1v5BRGzV_Z-qjYnrdUiNR6M-vpAaBOL8IC1l9jj9lTo1W4jET0l4EUqkpnNL_7L58i5JlDyQiEuTVZWUWVH4lOU4TWh4loXl-dbFQEWeHu0bYhStfEmzQRZXCy7XIHP52fy2eWckayM; sgid=09-42566599-AV1SJHh5RfDic44AFycbg794; ppmdig=1565664376000000661b5edc16a1e561a14bfa97fda2f661'
        item_arr = str_.split(';')
        for i in item_arr:
            dict_ = {}
            arr_ = i.split('=')
            dict_['name'] = arr_[0].lstrip()
            dict_['value'] = arr_[1].lstrip()
            cookieslist.append(dict_)
        return cookieslist

    def startCrawl(self):
        driver = self.driver
        driver.get(self.url)
        for i in self.getCookies():
            self.driver.add_cookie(i)
        print('Cookies is OK')
        while True:
            if len(driver.find_elements_by_id('seccodeInput')) > 0:
                self.get_V_Code_picture(driver)  #此方法会刷新验证码
                self.get_show_Code()
                driver.find_element_by_id("seccodeInput").clear()
                driver.find_element_by_id("seccodeInput").send_keys(self.get_V_Code()) #需要填写的验证码
                driver.find_element_by_id("submit").click()  #提交验证码
                time.sleep(5)
                if len(driver.find_elements_by_id("error-tips")) > 0:
                    print('验证码错误')
                    continue
                else:
                    print('验证成功') #等待加载

            if len(driver.find_elements_by_id('sogou_next')) > 0: #还有下一页
                soup = BeautifulSoup(driver.page_source, 'lxml')  # 获取当前页面全部内容
                for li in soup.find('div', class_="news-box").ul.find_all('li'):  # 迭代内容
                    url = li.find('div', class_="txt-box").h3.a['data-share']
                    #txt = ''.join(re.findall('[\u4e00-\u9fa5]',li.find('div', class_="txt-box").h3.a.text)) #正则提取文章标题的汉字部分
                    self.conn.lpush(self.keyword,url)
                driver.find_element_by_id('sogou_next').click()  #进入下一页
                print('success')
                time.sleep(2)

            else:   #没有下一页
                break

    def get_V_Code_picture(self,driver):
        driver.find_element_by_xpath('//*[@id="change-img"]').click() #刷新验证码
        screenshot = driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        captcha = screenshot.crop((330, 260, 500,400)) #验证码的四个点
        captcha.save('E:\DataAnalysis\project\WeiXinCrawl\picture\\vcode.png')

    def get_show_Code(self):
        img = Image.open(os.path.join('E:\DataAnalysis\project\WeiXinCrawl\picture\\vcode.png'))
        plt.figure("验证码截图")  # 图像窗口名称
        plt.imshow(img)
        plt.axis('off')  # 关掉坐标轴为 off
        plt.title('请记住并在控制台输入图片中的验证码',fontproperties="SimHei")  # 图像题目
        plt.show()

    def get_V_Code(self):
        code = input(" 请填写验证码:")
        return code

ucl = urlCrawl()
ucl.startCrawl()








