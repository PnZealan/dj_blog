#-*- coding : utf-8 -*-
import re
import requests
import urllib2
import json
from urllib import unquote
'''reload(sys)
sys.setdefaultencoding('utf-8')'''




class bdpanSpider:
        def __init__(self):
                bduss = '0RZS3h0cW92MGhoUlhJbHNpRzJVaG1NSXhVWkFhN1lVdGhxZXNyM2poSmtUODVZSVFBQUFBJCQAAAAAAAAAAAEAAABXli2JX-ezuuy3276nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGTCplhkwqZYU'
                stoken = '2427d4ecab01fb989dffcd4ec7e9eaf47606abed79211507709f1f41b02d02e7'
                bdstoken = '1e9ae7b19b80603e243e2b5665946c64'
                res_content=r'"app_id":"(\d*)".*"parent_path":"(.*?)".*"path":"([^"]*)".*"uk":(\d*).*"bdstoken":"(\w*)".*"shareid":(\d*)' 
                self.p=re.compile(res_content)
                self.app_id=""
                self.uk=""
                self.bdstoken=""
                self.shareid=""
                self.path=""
                self.headers = {
                    'Host':"pan.baidu.com",
                    'Accept':'*/*',
                    'Accept-Language':'en-US,en;q=0.8',
                    'Cache-Control':'max-age=0',
                    'Referer':'https://pan.baidu.com/disk/home',
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                    'Cookie':'BDUSS=%s;STOKEN=%s;'%(bduss,stoken),
                    'DNT':'1',
                    'Host':'pan.baidu.com',
                    'Pragma':'no-cache',
                    'X-Requested-With':'XMLHttpRequest',
                    }
        def getbody(self,url):
                try:
                        req=requests.get(url,headers=self.headers)
                        content=req.content
                        #print content
                except Exception,e:
                        print "[Error]",str(e)
                else:
                        L=self.p.findall(content)
                        if L:
                                #print L
                                self.app_id=L[0][0]
                                self.pa_path = L[0][1]
                                self.path=L[0][2]
                                self.uk=L[0][3]
                                self.bdstoken=L[0][4]
                                self.shareid=L[0][5]
                                return self.filename(url, self.shareid, self.uk)
                        else:
                            return 'invalid url'
        def addziyuan(self):
                url_post="https://pan.baidu.com/share/transfer?shareid="+self.shareid+"&from="+self.uk+"&bdstoken="+self.bdstoken+"&channel=chunlei&clienttype=0&web=1&app_id=250528&logid=MTQ5MjA0ODExOTE0NTAuNjg1ODk3MTk4ODIyNDE2Mw=="
                payload = {
                    'filelist':'["%s/%s"]'%(unquote(self.pa_path),self.file_name),
                    'path':'/wechat',
                    }
                #print "[Info]Url_Post:",url_post
                #print "[Info]payload:",payload
                try:
                        req=requests.post(url=url_post,data=payload,headers=self.headers)
                        result=json.loads(req.content)
                        #print req.content
                        #print result
                        tag=result["errno"]
                        #print tag
                        if tag == 0:
                                content =  "[Result]Add Success"
                        elif tag == 12:
                                content =  "[Result]Already Exist"
                        else:
                                content =  result
                        #print content
                        #print '["%s/%s"]'%(unquote(self.pa_path),self.file_name)
                        return content
                except Exception,e:
                        print "[Error]",str(e)
        def filename(self,url,shareid,uk):
            headers = {
                'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate, sdch, br',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'DNT':'1',
                'Host':'pan.baidu.com',
                'Pragma':'no-cache',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest'
                }
            #request = urllib2.Request(self.url,headers=headers)
            #r = urllib2.urlopen(request)
            try:
                r = requests.get(url,headers=headers)
                html = r.content
            except Exception,e:
                print e
            '''with open('2.txt','w') as p:
                p.write(html)'''
            #regx = r'<h2 class="file-name" title="(.*?)"'
            #regx = r'<h2 class="file-name" title="(.*?)".*?</h2>'
            regx = r'<meta name="renderer" content="webkit">.*?<title>(.*?)</title>'
            pattern = re.compile(regx, re.S)
            if html:
                result = re.findall(pattern, html)
                #print result
                ind = len(result[0])
                self.file_name = result[0][:ind-48]
                return self.addziyuan()   
                        
                        
if __name__ == '__main__':
    a = bdpanSpider().getbody('http://pan.baidu.com/share/link?shareid=891905572&uk=1297528333&fid=396938031835776')
    print a
