
__author__ = 'Hex'

import re
import urllib
import urllib2
import datetime

if __name__=="__main__":
    beginDate=datetime.date(2013,1,1)#设定开始时间
    endDate=datetime.date(2013,10,30)#设定结束时间
    Num=0#设定抓取文件起始命名
    for i in range((endDate-beginDate).days+1):
        day=beginDate+datetime.timedelta(days=i)
        #urlList="http://www.reuters.com/resources/archive/us/20121126.html"
        urlList=r'http://www.reuters.com/resources/archive/us/'+str(day.year)+str(day.month).zfill(2)+str(day.day).zfill(2)+r'.html'
        try:
            urlNewsList=urllib2.urlopen(urlList).read()
        except:
            continue
        else:
            newsListRes=re.findall("<div class=\"headlineMed\"><a href='(http://www.reuters.com/article/[0-9]*/[0-9]*/[0-9]*/.*?)'>",urlNewsList)
            for newsUrl in newsListRes[0:30]:#选择当天新闻数目
                try:
                    content=urllib2.urlopen(newsUrl).read()
                except:
                    continue
                else:
                    titleRe=re.search(r'<title>(.*?)</title>',content,re.DOTALL)
                    if titleRe:
                        title=titleRe.group(1).strip().replace('\n',' ')
                        dateRe=re.search(r'http://www.reuters.com/article/([0-9]*/[0-9]*/[0-9]*)/.*',newsUrl)
                        if dateRe:
                            date=dateRe.group(1).strip()
                            paragraphRe=re.search(r'.*<span class="focusParagraph">(.*)</span></span>.*',content,re.DOTALL)
                            if paragraphRe:
                                paragraph=paragraphRe.group(1)
                                paragraph=re.sub(r'<.*?>','',paragraph)
                                #paragraph.replace('\n','')
                                #paragraph.replace('\r','')
                                paragraph=re.sub("[\s]+",' ',paragraph)
                                paragraph.strip()
                                if paragraph.find("TESTING")>0:
                                    continue
                                Num=Num+1
                                fnews=open(r'./news-reuter/'+str(Num)+r'.txt','w')
                                fnews.write('<TITLE>'+title+'</TITLE>'+'\n')
                                fnews.write('<URL>'+newsUrl.strip()+'</URL>'+'\n')
                                fnews.write('<DATE>'+date+'</DATE>'+'\n')
                                fnews.write('<NEWS>'+paragraph+'</NEWS>'+'\n')
                                fnews.close()




