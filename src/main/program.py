from selenium import webdriver #UI自动化框架
from selenium.webdriver.chrome.options import Options #chrome浏览器参数
from tool import utilities as u #工具
import threading #线程

'''
虎牙直播弹幕机器人
启动需要最新版谷歌浏览器，并登陆QQ(需要已绑定手机号可以正常使用虎牙的)
by 冯离惑

需要下载第三方包：selenium,requests,emoji
'''
#需要进入的直播间
url = "https://www.huya.com/dongfangyuechu"

if __name__ == "__main__":    
    '''已弃用 无头浏览器可能会增加CPU占用
    #创建chrome参数对象
    opt = Options()
    #设置无界面
    opt.add_argument("--headless")
    opt.add_argument("--disable-gpu")
    #设置浏览器大小
    opt.add_argument("--window-size=1920,1080")
    #浏览器无界面对象
    driver = webdriver.Chrome(options = opt)
    '''
    #浏览器对象
    driver = webdriver.Chrome()
    #登陆
    u.login(driver, url)
    
    '''
    以下多个功能需要同时进行，我们开启多个线程
    '''

    #感谢礼物功能的线程
    thread_thanks = threading.Thread(target=u.thank_for_gift, args=(driver,))
    #启动感谢礼物功能线程
    thread_thanks.start() 
    
    #欢迎贵宾功能的线程
    thread_welcome = threading.Thread(target=u.welcome, args=(driver,))     
    #启动欢迎贵宾功能线程
    thread_welcome.start()     
    
    #求订阅功能的线程
    thread_please = threading.Thread(target=u.please, args=(driver,))    
    #启动求订阅功能线程
    thread_please.start()         
    
    #AI对话功能的线程
    thread_ai = threading.Thread(target=u.ai, args=(driver,))    
    #启动AI对话功能线程
    thread_ai.start() 
    