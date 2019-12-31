#coding:gbk
import sys
import ssl
import urllib
import urllib2
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
context = ssl._create_unverified_context()

def crawl_tencent_by_appid(appid):
    appname = ""
    cate = ""
    req = urllib2.Request(url = 'http://android.myapp.com/myapp/detail.htm?apkName=' + appid, headers = headers)
    try:
        content = urllib2.urlopen(req, timeout=5).read().decode('utf-8', 'ignore').encode('gbk', 'ignore')
    except:
        return appname,cate
    re_result = re.search(' appname="(.*?)" appicon', content)
    if re_result:
        appname = re_result.group(1)
    re_result = re.search('id="J_DetCate">(.*?)</a>', content)
    if re_result:
        cate = re_result.group(1)
    return appname.strip(), cate.strip()


def crawl_xiaomi_by_appid(appid):
    appname = ""
    cate = ""
    req = urllib2.Request(url = 'http://app.mi.com/details?id=' + appid, headers = headers)
    try:
        content = urllib2.urlopen(req, timeout=5).read().decode('utf-8', 'ignore').encode('gbk', 'ignore')
    except:
        return appname,cate
    re_result = re.search('class="intro-titles"><p>(.*?)</p><h3>(.*?)</h3><p class="special-font action', content)
    if re_result:
        appname = re_result.group(2)
    re_result = re.search('class="special-font action"><b>分类：</b>(.*?)<span style="margin', content)
    if re_result:
        cate = re_result.group(1)
    return appname.strip(), cate.strip()


def crawl_wandoujia_by_appid(appid):
    appname = ""
    cate = ""
    req = urllib2.Request(url = 'https://www.wandoujia.com/apps/' + appid, headers = headers)
    try:
        content = urllib2.urlopen(req, timeout=5).read().decode('utf-8', 'ignore').encode('gbk', 'ignore')
    except:
        return appname,cate
    re_result = re.search('itemprop="name">(.*?)</span>', content)
    if re_result:
        appname = re_result.group(1)
    re_result = re.findall('itemprop="SoftwareApplicationCategory" data-track="detail-click-appTag">(.*?)</a>', content)
    if re_result:
        for term in re_result:
            cate += term + ';'
    return appname.strip(), cate.strip()


def crawl_xiaomi_by_appname(appname):
    appname_urlcode = urllib.quote(appname.decode("gbk","ignore").encode("utf8","ignore"))
    req = urllib2.Request(url = 'http://app.mi.com/searchAll?typeall=phone&keywords=' + appname_urlcode, headers = headers)
    try:
        content = urllib2.urlopen(req, timeout=5).read().decode('utf-8', 'ignore').encode('gbk', 'ignore')
    except:
        return '',''
    re_result = re.findall('height="72"></a><h5><a href="/details\?id=(.*?)</a></h5><p class="app-desc">', content)
    #print re_result
    appid = ''
    for info in re_result:
        #print info
        items = info.split('&ref=search">')
        if len(items) == 2:
            id = items[0]
            name = items[1]
            #print id, name
            if name is not None and name == appname:
                appid = id
                break
    if len(appid) == 0:
        return '',''
    _, cate = crawl_xiaomi_by_appid(appid)
    return appid, cate



def crawl_wandoujia_by_appname(appname):
    appname_urlcode = urllib.quote(appname.decode("gbk","ignore").encode("utf8","ignore"))
    req = urllib2.Request(url = 'https://www.wandoujia.com/search?key=' + appname_urlcode, headers = headers)
    try:
        content = urllib2.urlopen(req, timeout=5).read().decode('utf-8', 'ignore').encode('gbk', 'ignore')
    except:
        return '',''
    re_result = re.findall('<h2 class="app-title-h2"><a href="https://www.wandoujia.com/apps/(.*?)</a><span class="tagline wap-hide">', content)
    #print re_result
    appid = ''
    for info in re_result:
        #print info
        items = info.split('" class="name">')
        if len(items) == 2:
            id = items[0]
            name = items[1]
            #print id, name
            if name is not None and name == appname:
                appid = id
                break
    if len(appid) == 0:
        return '',''
    _, cate = crawl_wandoujia_by_appid(appid)
    return appid, cate


if sys.argv[1] == 'id':
    fw = open(sys.argv[3], 'w')
    for line in file(sys.argv[2]):
        appid = line.strip()
        appname1,cate1 = crawl_tencent_by_appid(appid)
        appname2,cate2 = crawl_xiaomi_by_appid(appid)
        appname3,cate3  = crawl_wandoujia_by_appid(appid)
        output = appid + '\t' + appname1 + '@' + cate1 + '#' + appname2 + '@' + cate2 + '#' + appname3 + '@' + cate3
        print output
        fw.write(output + '\n')
    fw.close()
elif sys.argv[1] == 'name':
    fw = open(sys.argv[3], 'w')
    for line in file(sys.argv[2]):
        appname = line.strip()
        appid1,cate1 = crawl_xiaomi_by_appname(appname)
	appid2,cate2 = crawl_wandoujia_by_appname(appname)
        output = appname + '\t' + appid1 + '@' + cate1 + '#' + appid2 + '@' + cate2
        print output 
        fw.write(output + '\n')
    fw.close()
