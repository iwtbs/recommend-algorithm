#coding:gbk
import sys
import redis
import KVClient
import traceback
import time,datetime
from multiprocessing import Pool

def get_doc_text(docid_list):
    docid_text_list= []
    sub_docid_list = []
    for i in range(len(docid_list)):
        sub_docid_list.append(docid_list[i])
        if len(sub_docid_list) == 200 or i == len(docid_list) - 1:
            sub_docid_dict = dict(zip(sub_docid_list, sub_docid_list))
            forward_list = []
            try:
                forward_list = KVClient.mget_forward_index(sub_docid_list)
            except:
                traceback.print_exc()
                continue
            sub_docid_list = []
            for forward in forward_list:
                _id = ''
                video_sig = ''
                title = ''
                url = ''
                account_weight = ''
                if forward is not None:
                    if forward.has_key('_id'):
                        _id = forward['_id']
                    if forward.has_key('video_sig'):
                        video_sig = str(forward['video_sig'])
                    if forward.has_key('title'):
                        title = forward['title']
                    if forward.has_key('url'):
                        url = forward['url']
                    if forward.has_key('account_weight'):
                        account_weight = str(forward['account_weight'])
                    output = _id + '#@#' + video_sig + '#@#' + title + '#@#' + url  + '#@#' + account_weight
                    docid_text_list.append(output)
    return docid_text_list


def read_data():
    trunk = 10000
    icount = 0 
    texts = []
    for line in file(sys.argv[1]): 
        texts.append(line)
        icount += 1
        if icount % trunk == 0:
            yield texts
            texts = []
    yield texts
 

def parallel_deal():
    texts = read_data()
    fw_text = open(sys.argv[2], "w")
    cpus = 10
    ichunk = 0
    for t in texts:
        pool = Pool(cpus)
        step = int(len(t) / cpus)
        tmp = [t[i:i+step] for i in range(0, len(t) , step)]
        results = pool.map(get_doc_text, tmp)
        pool.close()
        pool.join()
        # 写入
        for r in results:
            for i in r:
                fw_text.write(i + "\n")
        ichunk += 1
        print "finished samples:",len(t) * ichunk
    fw_text.close()
 
 
if __name__ == "__main__":
    parallel_deal()


