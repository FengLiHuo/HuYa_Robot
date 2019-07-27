#from selenium.webdriver import ActionChains #动作
import time #时间
import random #随机
import requests #接口自动化框架
import json #json处理
import traceback #异常处理
import emoji #emoji表情
import re #正则表达式

#黑名单(模糊匹配) 不会欢迎和感谢以及回复黑名单里的人
blacklist = [
    "葉子",
    "芯芯姐-等你来约",
    "场控",
    "場控",
    "漲粉",
    "房管",
    "招主播",
    "機器",
    "机器"
]

#进入直播间并登陆
def login(driver, url):
    #进入直播间
    driver.get(url)
    #最大化
    driver.maximize_window()
    #虎牙会提示账号登陆地点异常所以通过QQ来进行快捷登陆
    #点击登录
    time.sleep(0.5)
    driver.find_element_by_id("nav-login").click()
    time.sleep(2)
    #进入登陆小窗口的框架
    driver.switch_to_frame("UDBSdkLgn_iframe")
    #选择QQ登录
    time.sleep(1)
    driver.find_element_by_class_name("qq-icon").click()
    #切换句柄 去登录页面
    driver = switch_handle(driver)
    #进入登录页面的框架
    time.sleep(2)
    driver.switch_to_frame("ptlogin_iframe")
    #点击我的QQ
    time.sleep(2)
    driver.find_element_by_id("nick_864247945").click()
    #切换句柄 回到直播间
    driver = switch_handle(driver)
    
    time.sleep(2)
    #跳转回来以后可能还是有登陆窗口，刷新一下
    driver.refresh()
    time.sleep(1)
    
    time.sleep(2)
    #关闭弹窗
    close(driver)
    
    '''已弃用 移除视频元素后视频流的传输可能并未停止
    #移除视频元素等高占用的元素
    js_remove = "var element = document.getElementById('J_playerMain');element.parentNode.removeChild(element);"
    driver.execute_script(js_remove)
    
    #将视频暂停    已弃用 没有太多意义
    try:
        #动作对象
        action = ActionChains(driver)
        #创建动作并执行 鼠标移至视频上
        action.move_to_element(driver.find_element_by_id("player-video")).perform()
        time.sleep(0.1)
        #暂停视频
        driver.find_element_by_id("player-btn").click()
    except Exception as e:
        pass
    '''
    
    print("service start...")
    
    #返回浏览器对象
    #return driver 
    
#感谢礼物
def thank_for_gift(driver):
    #记录次数
    num = 0
    #将每一个新元素都追加进列表里，就可以获取一共有多少个元素
    list = []
    
    #循环获取得到第一个礼物元素，获取到第一个就停止
    while(len(list) < 1):
        try:
            #将礼物元素添加进列表
            list.append(driver.find_element_by_xpath("(//div[@class='tit-h-send'])[last()]"))
        except Exception as e:
            continue
    
    #死循环 不断获取元素
    while True:
        time.sleep(0.5)
        try:
            #获取最新的礼物元素
            element = driver.find_element_by_xpath("(//div[@class='tit-h-send'])[last()]")
            #与列表中的最后一个，也就是上一个判断是否是一样的
            if(list[-1] != element):
                #不一样说明是新元素，添加到列表里
                list.append(element)
            
            #每一个新元素只发一次感谢
            if(num == len(list)-1):
                #送礼人
                name = driver.find_element_by_xpath("(//div[@class='tit-h-send'])[last()]/span").text
                #selenium的写入方法不支持emoji 将其去掉
                #emoji转英文
                name = emoji.demojize(name)
                #去掉emoji的英文
                name = re.sub(':.*?:',"",name)
                #数量
                number = driver.find_elements_by_xpath("(//div[@class='tit-h-send'])[last()]/span")[3].text
                #礼物名
                gift_name = driver.find_element_by_xpath("(//div[@class='tit-h-send'])[last()]/span[@class='cont-item send-gift']/img").get_attribute("alt")
                #答谢
                text = "[送花]感谢"+name+"送的"+number+"个"+gift_name
                
                #判断是否在黑名单内
                correct = True
                for i in range(0,len(blacklist)):
                    #模糊匹配 判断名字中是否包含有黑名单词汇
                    if(blacklist[i] in name):
                        correct = False
                #不在黑名单里就是true 发送弹幕
                if(correct):
                    time.sleep(0.5)
                    #由于多线程同时运行，如果多个行为同时出现，其中一个线程需要先等待1秒再输入，否则两句话会挤在一起
                    #获取文本框的值
                    input = driver.find_element_by_id("pub_msg_input").get_attribute("value")
                    #判断是否为空，如果为空就直接执行
                    if(input.strip() == ""):
                        driver.find_element_by_id("pub_msg_input").clear()
                        driver.find_element_by_id("pub_msg_input").send_keys(text)
                        time.sleep(1.5)
                        driver.find_element_by_id("msg_send_bt").click()
                        #不为空就等待1秒，等另一个线程输入发送完成后再输入
                    else:
                        time.sleep(2)
                        driver.find_element_by_id("pub_msg_input").clear()
                        driver.find_element_by_id("pub_msg_input").send_keys(text)
                        time.sleep(1.5)
                        driver.find_element_by_id("msg_send_bt").click()
                #次数+1
                num = num + 1   
        except Exception as e:
            continue
        
#欢迎贵宾
def welcome(driver):
    #记录次数
    num = 0
    #将每一个新元素都追加进列表里，就可以获取一共有多少个元素
    list = []
    
    #循环获取得到第一个贵宾元素，获取到第一个就停止
    while(len(list) < 1):
        try:
            #将贵宾元素添加进列表
            list.append(driver.find_element_by_xpath("(//span[@class='msg-nobleEnter-pic'])[last()]/preceding-sibling::span"))
        except Exception as e:
            continue
    
    while True:
        time.sleep(0.5)
        try:
            #获取最新的贵宾
            element = driver.find_element_by_xpath("(//span[@class='msg-nobleEnter-pic'])[last()]/preceding-sibling::span")
            #与列表中的最后一个，也就是上一个判断是否是一样的
            if(list[-1] != element):
                #不一样说明是新元素，添加到列表里
                list.append(element)
            
            #每一个新元素只发一次感谢
            if(num == len(list)-1):
                #贵宾名
                name = driver.find_element_by_xpath("(//span[@class='msg-nobleEnter-pic'])[last()]/preceding-sibling::span").text
                #selenium的写入方法不支持emoji 将其去掉
                #emoji转英文
                name = emoji.demojize(name)
                #去掉emoji的英文
                name = re.sub(':.*?:',"",name)
                #欢迎
                text = "[喜欢]欢迎"+name+"进入直播间~"
                
                #判断是否在黑名单内
                correct = True
                for i in range(0,len(blacklist)):
                    if(blacklist[i] in name):
                        correct = False
                #不在黑名单里就是true 发送弹幕
                if(correct):
                    time.sleep(0.5)
                    #由于多线程同时运行，如果多个行为同时出现，其中一个线程需要先等待1秒再输入，否则两句话会挤在一起
                    input = driver.find_element_by_id("pub_msg_input").get_attribute("value")
                    if(input.strip() == ""):
                        driver.find_element_by_id("pub_msg_input").clear()
                        driver.find_element_by_id("pub_msg_input").send_keys(text)
                        time.sleep(1.5)
                        driver.find_element_by_id("msg_send_bt").click()
                    else:
                        time.sleep(2)
                        driver.find_element_by_id("pub_msg_input").clear()
                        driver.find_element_by_id("pub_msg_input").send_keys(text)
                        time.sleep(1.5)
                        driver.find_element_by_id("msg_send_bt").click()
                #次数+1
                num = num + 1
        except Exception as e:
            continue

#定时求订阅求一次订阅
def please(driver):
    while True:
        text = [
            "有人给主播扣个666吗",
            "关注主播不迷路，送礼主播陪你睡[害羞][害羞][害羞]",
            "十个荧光棒或大宝剑即可获得粉丝勋章，坐上贵宾席哦~[赞]",
            "想要进入尊贵的贵宾席吗，那就卡个牌子吧！[赞]",
            "这个世界，需要英雄",
            "sixsixsix",
            "以前有一个人点了个订阅，然后卡了个牌子，后来...",
            "666666",
            "牛啤牛啤",
            "喜欢主播可以点一下订阅哦[喜欢]",
            "错过了我这么好的主播你不会后悔吗！",
            "大家闲着没事可以卡卡牌子，喷喷主播哦",
            "主播好帅可以给我生猴子吗[送花]",
            "在@后面加想说的话可以与我聊天哦[害羞]"
            "欢迎加入主播的同性交友Q群：557422607[害羞]"
        ]
        #随机数抽取列表里的句子
        rand = random.randint(0,14)
        #发送弹幕
        #由于多线程同时运行，如果多个行为同时出现，其中一个线程需要先等待1秒再输入，否则两句话会挤在一起
        input = driver.find_element_by_id("pub_msg_input").get_attribute("value")
        if(input.strip() == ""):
            driver.find_element_by_id("pub_msg_input").clear()
            driver.find_element_by_id("pub_msg_input").send_keys(text[rand])
            time.sleep(1.5)
            driver.find_element_by_id("msg_send_bt").click()
        else:
            time.sleep(2)
            driver.find_element_by_id("pub_msg_input").clear()
            driver.find_element_by_id("pub_msg_input").send_keys(text[rand])
            time.sleep(1.5)
            driver.find_element_by_id("msg_send_bt").click()
        time.sleep(120)

#AI对话交互
def ai(driver):
    #记录次数
    num = 0
    #将每一个新元素都追加进列表里，就可以获取一共有多少个元素
    list = []   
    
    #循环获取得到第一个对话元素，获取到第一个就停止
    while(len(list) < 1):
        try:
            #将对话元素添加进列表
            list.append(driver.find_element_by_xpath("(//span[starts-with(text(),'@')])[last()]"))
        except Exception as e:
            continue
    
    while True:
        time.sleep(0.5)
        try:
            #获取最新的对话
            element = driver.find_element_by_xpath("(//span[starts-with(text(),'@')])[last()]")
            #与列表中的最后一个，也就是上一个判断是否是一样的
            if(list[-1] != element):
                #不一样说明是新元素，添加到列表里
                list.append(element)   
               
            #每一个新元素只回复一次
            if(num == len(list)-2):
                #对话
                msg = driver.find_element_by_xpath("(//span[starts-with(text(),'@')])[last()]").text
                #获取对话人的姓名
                name = driver.find_element_by_xpath("(//span[starts-with(text(),'@')])[last()]/preceding-sibling::span").text
                #selenium的写入方法不支持emoji 将其去掉
                #emoji转英文
                name = emoji.demojize(name)
                #去掉emoji的英文
                name = re.sub(':.*?:',"",name)
                #将对话前面的@去掉
                msg = msg.lstrip("@")
                #回复
                text = tuling_api(msg)
                
                #判断是否在黑名单内
                correct = True
                for i in range(0,len(blacklist)):
                    if(blacklist[i] in name):
                        correct = False
                #不在黑名单里就是true 发送弹幕
                if(correct):
                    #发送弹幕
                    time.sleep(0.5)
                    #由于多线程同时运行，如果多个行为同时出现，其中一个线程需要先等待1秒再输入，否则两句话会挤在一起
                    input = driver.find_element_by_id("pub_msg_input").get_attribute("value")
                    if(input.strip() == ""):
                        driver.find_element_by_id("pub_msg_input").clear()
                        driver.find_element_by_id("pub_msg_input").send_keys(text)
                        time.sleep(1.5)
                        driver.find_element_by_id("msg_send_bt").click()
                    else:
                        time.sleep(2)
                        driver.find_element_by_id("pub_msg_input").clear()
                        driver.find_element_by_id("pub_msg_input").send_keys(text)
                        time.sleep(1.5)
                        driver.find_element_by_id("msg_send_bt").click()
                #次数+1
                num = num + 1
        except Exception as e:
            continue

#调用图灵机器人接口
def tuling_api(msg):
    #秘钥
    key = "9d062a8c6257487fafb5e5856464a3a0"
    #用户名
    id = "477381"
    #接口的url
    url = "http://openapi.tuling123.com/openapi/api/v2"
    
    #请求报文
    data = {
        "reqType":0,
        "perception": {
            "inputText": {
                "text": "%s"%(msg)
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "",
                    "province": "",
                    "street": ""
                }
            }
        },
        "userInfo": {
            "apiKey": key,
            "userId": id
        }
    }
    
    data = json.dumps(data).encode(encoding='utf_8')
    
    r = requests.post(url,data).json()
    
    return r['results'][0]['values']['text']
    
#切换句柄
def switch_handle(driver):
    #获取当前句柄
    thisHandle = driver.current_window_handle
    #获取所有句柄
    handles = driver.window_handles
    #遍历判断
    for handle in handles:
        if(handle != thisHandle):
            driver.switch_to_window(handle)
    
    #返回浏览器对象
    return driver 

#因为不明弹窗的机制，所以封装一个方法来关闭
def close(driver):
    try:
        #可能会有几个弹窗把它们点掉
        driver.find_element_by_class_name("tips-firstTime").click()
    except Exception as e:
        pass
    try:
        #可能会有几个弹窗把它们点掉
        driver.find_element_by_xpath("//span[text()='我知道了']").click()
    except Exception as e:
        pass
    
    