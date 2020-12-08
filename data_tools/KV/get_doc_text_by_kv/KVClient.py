#encoding=gbk
import sys
import httplib
import json
import time
import traceback
import re
import hashlib

KV_DEFAULT_KEY = "-1"
KV_PER_SEARCH = 200

def get_title_md5(title):
    change_pos = re.compile('"|��|��|,|\.|��|~|��|,|\?|��|:|\(|\)|\[|\]|��|��|-|��|��|��|��|!|;|��')
    title = change_pos.sub("", title)
    title_md5 = hashlib.md5(title).hexdigest()
    return title_md5

def json_unicode_to_gbk(jo_unicode):
    if type(jo_unicode) == dict:
        jo_gbk = {}
        for key in jo_unicode:
             value_gbk = json_unicode_to_gbk(jo_unicode[key])
             jo_gbk[key.encode('gbk')] = value_gbk
        return jo_gbk
    elif type(jo_unicode) == list:
        return [json_unicode_to_gbk(x) for x in jo_unicode]
    elif type(jo_unicode) == unicode:
        return jo_unicode.encode('gbk','ignore')
    else:return jo_unicode

def transform_key(key):
    if not key:key = KV_DEFAULT_KEY
    return key

#get title by kv
def mget_title_by_kv(id_list):
    id = [transform_key(x) for x in id_list]
    conn = httplib.HTTPConnection("kv.sogou-op.org")
    request_len = KV_PER_SEARCH
    total_len = len(id_list)
    result = []
    for index in  range(0,total_len/request_len + 1):
        start_index = index*request_len
        end_index   = (index+1)*request_len

        tmp_id_list = id_list[start_index:end_index]
        if len(tmp_id_list) == 0:continue
        conn.request("POST" ,url="/mget/110216/article_forward_index/", body="\n".join(tmp_id_list))
        resp = conn.getresponse()
        if resp.status == 200:
            resp_str = resp.read()
            tups = resp_str.strip('\r\n').split('\r\n$')
            for term in tups[1:]:
                pos = term.find('\r\n')
                if pos != -1:
                    article_str = term[pos+len('\r\n'):]
                    try:
                        article = json.loads(article_str,encoding="gbk")
                        title = article.get("title","").encode('gbk')
                    except:
                        traceback.print_exc()
                        title = None
                    result.append(title)
                    continue
                result.append("")
        else:
            print>>sys.stderr,"[ERROR] KV PI Request, ERROR CODE %s"%(resp.status)
            result.extend([""] * len(tmp_id_list))
    return result


def mget_forward_index(id_list,attr_list=None):
    id = [transform_key(x) for x in id_list]
    conn = httplib.HTTPConnection("***")
    request_len = KV_PER_SEARCH
    total_len = len(id_list)
    result = []
    for index in  range(0,total_len/request_len + 1):
        start_index = index*request_len
        end_index   = (index+1)*request_len

        tmp_id_list = id_list[start_index:end_index]
        if len(tmp_id_list) == 0:continue
        conn.request("POST" ,url="***", body="\n".join(tmp_id_list))
        resp = conn.getresponse()
        if resp.status == 200:
            resp_str = resp.read()
            tups = resp_str.strip('\r\n').split('\r\n$')
            for term in tups[1:]:
                pos = term.find('\r\n')
                if pos != -1:
                    article_str = term[pos+len('\r\n'):]
                    try:
                        article = json.loads(article_str,encoding="gbk")
                        article = json_unicode_to_gbk(article)
                        #article = eval(article_str)
                        if attr_list:
                            for attr in article.keys():
                                if not attr in attr_list:del article[attr]

                    except:
                        traceback.print_exc()
                        article = None 
                else:
                    article = None
                result.append(article)
        else:
            print>>sys.stderr,"[ERROR] KV PI Request, ERROR CODE %s"%(resp.status)
            result.extend([None] * len(tmp_id_list))
        time.sleep(0.5)
    return result

def get_kv_doc(id_list):
    ret = mget_forward_index(id_list)
    return ret


