#coding:gbk
import sys
import traceback
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import redis
from ttypes import HotFeature
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport.TTransport import TMemoryBuffer

trunk = 20000

class Hot:
    def __init__(self, docid = '', pv = 0, cl = 0, readtime = 0, coldstart_pv = 0, coldstart_cl = 0):
        self.docid = docid
        self.pv = pv
        self.cl = cl
        self.readtime = readtime
        self.coldstart_pv = coldstart_pv
        self.coldstart_cl = coldstart_cl
    def to_string(self):
	return  self.docid + '\t' + str(self.pv) + ' ' + str(self.cl) + ' ' + str('%.2f'%self.readtime) +  ' ' + str(self.cl/(self.pv+0.00001)) + ' ' + str(self.coldstart_pv) + ' ' + str(self.coldstart_cl) + ' ' + str(self.coldstart_cl/(self.coldstart_pv+0.00001))


def get_doc_hot_by_thread(docid_list):
    docid_hot_list = []
    r = redis.Redis(host='***', port=1680, password='**', charset='gbk')
    redis_result_list = []
    try:
        redis_result_list = r.mget(docid_list)
        if redis_result_list is not None and len(redis_result_list) == len(docid_list):
            for i in range(len(redis_result_list)):
                if redis_result_list[i] is None or len(redis_result_list[i]) == 0:
                    continue
                docid = docid_list[i]
                tMemory_o = TMemoryBuffer(redis_result_list[i])
                tBinaryProtocol_o = TBinaryProtocol(tMemory_o)
                hot_feature = HotFeature()
                hot_feature.read(tBinaryProtocol_o)
                pv = hot_feature.app_show_num if hot_feature.app_show_num is not None else 0
                cl = hot_feature.app_read_num if hot_feature.app_read_num is not None else 0
                readtime = hot_feature.app_read_duration_double if hot_feature.app_read_duration_double is not None else 0
                coldstart_pv = hot_feature.coldstart_show_num if hot_feature.coldstart_show_num is not None else 0
                coldstart_cl = hot_feature.coldstart_read_num if hot_feature.coldstart_read_num is not None else 0

                docid_hot_list.append((docid, pv, cl, readtime, coldstart_pv, coldstart_cl))
    except:
        traceback.print_exc()
    return docid_hot_list


def get_doc_hot(docid_list):
    docid_hot_dict = {}
    pool = ThreadPool(processes=10)
    step = 200
    tmp = [docid_list[i:i+step] for i in range(0, len(docid_list), step)]
    map_results = pool.map(get_doc_hot_by_thread, tmp)
    for r in map_results:
        for docid, pv, cl, readtime, coldstart_pv, coldstart_cl in r:
            docid_hot_dict[docid] = Hot(docid, pv, cl, readtime, coldstart_pv, coldstart_cl)
    return docid_hot_dict
    

def read_data():
    icount = 0 
    texts = []
    for line in file(sys.argv[1]): 
        texts.append(line.strip())
        icount += 1
        if icount % trunk == 0:
            yield texts
            texts = []
    yield texts
 

def parallel_deal():
    global trunk
    texts = read_data()
    cpus = 10
    ichunk = 0
    fw = open(sys.argv[2], 'w')
    for t in texts:
        pool = Pool(cpus)
        step = 2000
        results = []
        for i in range(0, len(t), step):
            sub_t = t[i : min(i + step, len(t))]
            results.append(pool.apply_async(get_doc_hot, (sub_t,)))
        pool.close()
        pool.join()
        ichunk += 1
        print "finished samples:", trunk * (ichunk - 1) + len(t)
        for i in xrange(len(results)):
            for docid, hot in results[i].get().items():
		fw.write(hot.to_string() + '\n')
    fw.close()
    
 
if __name__ == "__main__":
    parallel_deal()

