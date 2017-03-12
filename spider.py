# coding=utf-8

import re,json
import requests
from file import File
from lxml import html

class Spider:
    headers = {
            "X-Requested-With": 'XMLHttpRequest',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
            #"Origin": 'https://www.lagou.com',
            "Cookie": 'user_trace_token=20170211115515-2db01e4efbb24178989f2b6139d3698e; LGUID=20170211115515-e593a6c4-f00d-11e6-8f71-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486785316; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486789519; _ga=GA1.2.1374329991.1486785316; LGRID=20170211130519-af0ec03c-f017-11e6-a32c-525400f775ce; TG-TRACK-CODE=search_code; JSESSIONID=A5AC6E7C54130E13C1519ABA7F70BC3C; SEARCH_ID=053c985ab53e463eb5f747658872ef29',
            "Connection": 'keep-alive'
            }
    __lowSalaryMin = 0.0
    __lowSalaryMax = 0.0
    __highSalaryMin = 0.0
    __highSalaryMax = 0.0

    containTextList = []
    shieldCompanyList = []

    def clearContainText(self):
        self.containTextList = []

    def addContainText(self,text):
        self.containTextList.append(text)

    def clearShieldCompany(self):
        self.shieldCompanyList = []

    def addShieldCompany(self,company):
        self.shieldCompanyList.append(company)

    def setLowSalaryMin(self,value):
        self.__lowSalaryMin = value

    def setLowSalaryMax(self,value):
        self.__lowSalaryMax = value

    def setHighSalaryMin(self,value):
        self.__highSalaryMin = value

    def setHighSalaryMax(self,value):
        self.__highSalaryMax = value

    def setSalay(self,valueLowMin ,valueLowMax,valueHighMin,valueHighMax):
        self.setLowSalaryMin(valueLowMin)
        self.setLowSalaryMax(valueLowMax)
        self.setHighSalaryMin(valueHighMin)
        self.setHighSalaryMax(valueHighMax)

    def __init__(self,search,city):
        self.search = search
        self.city = city

    def __getPage(self):
        url = 'https://www.lagou.com/jobs/list_'+self.search+'?city='+self.city+'&cl=false&fromSearch=true&labelWords=&suginput='
        html = requests.get(url,headers =self.headers)
        html.encoding = 'utf-8'
        rst = re.search(r'<span class="span totalNum">\d\d',html.text)
        if not rst:
            rst = re.search(r'<span class="span totalNum">\d',html.text)
        return  int(rst.group()[28:])

    def __matchText(self,content):
        if len(self.containTextList) == 0:
            return True
        for text in self.containTextList:
            if text in  content :
                return True
        return False

    def __match(self,file,workMsg):
        thisCompany = workMsg['companyShortName']
        for company in self.shieldCompanyList:
            if  company in  thisCompany:
                return

        salary = workMsg['salary']

        low =0
        high =0
        if '-' in salary:
            salarys = salary.split('-')
            low = float(salarys[0].replace('k','').replace('K',''))
            high = float(salarys[1].replace('k','').replace('K',''))
        elif 'K' in salary:
            salarys = salary.split('K')
            low = (self.__lowSalaryMin + self.__lowSalaryMax)/2
            high = float(salarys[0])
        else:
            salarys = salary.split('k')
            low = (self.__lowSalaryMin + self.__lowSalaryMax)/2
            high = float(salarys[0])




        if(low>self.__lowSalaryMin and high > self.__highSalaryMin and high < self.__highSalaryMax and low<self.__lowSalaryMax):
            url = 'https://www.lagou.com/jobs/'+str(workMsg['positionId'])+'.html'
            page = requests.get(url,headers =self.headers)
            contentList = re.findall('<p>.*</p>',page.text)
            message = workMsg['positionName'] +':\t----'+ workMsg['companyShortName'] + workMsg['salary'] + workMsg['financeStage'] + workMsg['workYear']
            if self.__matchText(message):
                file.addSaveText(message)
                file.addSaveText('https://www.lagou.com/jobs/'+str(workMsg['positionId'])+'.html')
                file.addSaveText('\n')
                return

            for content in contentList:
                if self.__matchText(content):
                    file.addSaveText(message)
                    file.addSaveText('https://www.lagou.com/jobs/'+str(workMsg['positionId'])+'.html')
                    file.addSaveText('\n')
                    return


    def analyse(self):
        pageCount = self.__getPage()
        messageFile = File("work.txt")
        messageFile.startAddText()

        for i in range(1,pageCount+1):
            print '正在分析第'+str(i)+'页/总页数：'+str(pageCount)
            url = 'http://www.lagou.com/jobs/positionAjax.json?city='+self.city+'&first='+'true'+'&kd='+self.search+'&pn='+str(i)
            page = requests.get(url,headers =self.headers)
            page.encoding = 'utf-8'
            data = json.loads(page.text)
            for workMsg in data['content']['positionResult']['result'] :
                self.__match(messageFile,workMsg)
