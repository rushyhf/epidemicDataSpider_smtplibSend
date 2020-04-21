from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup 
import smtplib
from email.mime.text import MIMEText
from email.header import Header #导入库

path = 'C:\********\chromedriver.exe' #声明浏览器路径
browser = webdriver.Chrome(path) #声明浏览器，此处使用Chrome
url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3' #声明网址
browser.get(url) #打开所声明的网址
beaSoup = BeautifulSoup(browser.page_source, 'lxml') #声明BeautifulSoup对象

#对爬取的数据进行选择：
content_time = beaSoup.find('div', class_='Virus_1-1-253_32Y_aO') #数据更新时间
content_Chi = beaSoup.find('div', class_='VirusSummarySix_1-1-253_ZRHUKw') #国内数据板块
content_for = beaSoup.find('table', class_='VirusSummary_1-1-253_26c8Iu VirusSummary_1-1-253_2fRxdu') #全球数据板块
content_Ame = beaSoup.find('tr', class_='VirusTable_1-1-253_2AH4U9') #美国数据板块

str_time = content_time.text.replace('数据说明',' ') #数据更新时间有多余字符，将其替换为空格
str_Chi = '国内：现有确诊'
content_Chi_exist = beaSoup.find('div', class_='VirusSummarySix_1-1-253_3haLBF VirusSummarySix_1-1-253_2ZJJBJ') #国内现有确诊
content_Chi_exist_change = beaSoup.find('div', class_='VirusSummarySix_1-1-253_3I_ZN9') #国内现有确诊人数变化情况
content_Chi_all = beaSoup.find('div', class_='VirusSummarySix_1-1-253_3wCKWi VirusSummarySix_1-1-253_c39Mfc') #国内累计确诊人数及变化情况
content_Chi_death = beaSoup.find('div', class_='VirusSummarySix_1-1-253_3wCKWi VirusSummarySix_1-1-253_27xUAr') #国内累计死亡人数及变化情况
str_Chi += (content_Chi_exist.text +
            content_Chi_exist_change.text + ' ' +
            content_Chi_all.text + ' ' +
            content_Chi_death.text) #汇总国内情况
# print(str_Chi)

str_for = '全球：'
content_for_all = beaSoup.find('div', class_='VirusSummary_1-1-253_1erbWM') #全球累计确诊人数及变化情况
content_for_death = beaSoup.find('div', class_='VirusSummary_1-1-253_28rIkx') #全球累计死亡人数及变化情况
str_for += (content_for_2.text + ' ' + content_for_3.text)
# print(str_for) #汇总全球数据

#美国数据是表格情况，以下是数据选择的一种思路，应该有更简单的思路，请自己探索：
str_Ame = '美国：'
cnt = 0
tup = ('a','新增','a',' 累计确诊','a',' 累计死亡')
for b in content_Ame:
    if cnt%2 == 1:
        str_Ame += tup[cnt]
        str_Ame += b.text
    cnt += 1
# print(str_Ame)
browser.close() #关闭浏览器
str = str_time + '\n\r' + str_Chi + '\n\r' + str_for + '\n\r' + str_Ame #汇总所有数据情况
print(str) #输出所有数据情况

mail_host = "smtp.qq.com" #设置服务器
mail_user = "******@qq.com" #设置邮箱用户名
mail_pass = "*******" #此处口令为邮箱开启IMAP时获取的代码，不是QQ密码

sender = '******@qq.com' #发送端用户名
receivers = ['******@qq.com'] #接收端用户名

message = MIMEText(str, 'plain', 'utf-8') #邮件内容
message['From'] = Header("python", 'utf-8') #发件人
message['To'] = Header("测试", 'utf-8') #收件人
subject = 'Python SMTP 邮件'
message['Subject'] = Header(subject, 'utf-8') #邮件主题

try:
    smtpObj = smtplib.SMTP() #声明对象
    smtpObj.connect(mail_host, 25) #25为SMTP端口号
    smtpObj.login(mail_user, mail_pass) #登录
    smtpObj.sendmail(sender, receivers, message.as_string()) #发送
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
