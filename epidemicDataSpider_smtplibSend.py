from lxml import etree
from selenium import webdriver#导入库
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header

path = 'C:\******\chromedriver.exe'
browser = webdriver.Chrome(path)#声明浏览器
url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3'
browser.get(url)#打开浏览器预设网址
beaSoup = BeautifulSoup(browser.page_source, 'lxml')

content_time = beaSoup.find('div', class_='Virus_1-1-253_32Y_aO')
content_Chi = beaSoup.find('div', class_='VirusSummarySix_1-1-253_ZRHUKw')
content_for = beaSoup.find('table', class_='VirusSummary_1-1-253_26c8Iu VirusSummary_1-1-253_2fRxdu')
content_Ame = beaSoup.find('tr', class_='VirusTable_1-1-253_2AH4U9')

str_time = content_time.text.replace('数据说明',' ')
str_Chi = '国内：现有确诊'
content_Chi_exist = beaSoup.find('div', class_='VirusSummarySix_1-1-253_3haLBF VirusSummarySix_1-1-253_2ZJJBJ')
content_Chi_exist_change = beaSoup.find('div', class_='VirusSummarySix_1-1-253_3I_ZN9')
content_Chi_all = beaSoup.find('div', class_='VirusSummarySix_1-1-253_3wCKWi VirusSummarySix_1-1-253_c39Mfc')
content_Chi_death = beaSoup.find('div', class_='VirusSummarySix_1-1-253_3wCKWi VirusSummarySix_1-1-253_27xUAr')

str_Chi += (content_Chi_exist.text +
            content_Chi_exist_change.text + ' ' +
            content_Chi_all.text + ' ' +
            content_Chi_death.text)
# print(str_Chi)

str_for = '全球：'
content_for_2 = beaSoup.find('div', class_='VirusSummary_1-1-253_1erbWM')
content_for_3 = beaSoup.find('div', class_='VirusSummary_1-1-253_28rIkx')
str_for += (content_for_2.text + ' ' + content_for_3.text)
# print(str_for)

str_Ame = '美国：'
cnt = 0
tup = ('a','新增','a',' 累计确诊','a',' 累计死亡')
for b in content_Ame:
    if cnt%2 == 1:
        str_Ame += tup[cnt]
        str_Ame += b.text
    cnt += 1
# print(str_Ame)
browser.close()#关闭浏览器
str = str_time + '\n\r' + str_Chi + '\n\r' + str_for + '\n\r' + str_Ame
print(str)
# 第三方 SMTP 服务
mail_host = "smtp.qq.com"       # 设置服务器
mail_user = "******@qq.com"   # 用户名
mail_pass = "******"  # 口令

sender = '******@qq.com'
receivers = ['******@qq.com']# 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEText(str, 'plain', 'utf-8')  #消息
message['From'] = Header("python", 'utf-8')        #发件人
message['To'] = Header("测试", 'utf-8')              #收件人
subject = 'Python SMTP 邮件'                     #主题
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
