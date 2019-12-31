#coding=gbk
import sys
import time

for line in sys.stdin:
    tups = line.strip().decode("gbk","ignore").split("\t")
    if len(tups) < 36:
        continue
    if tups[0] == "req":
        (req,mid,tm,action,topic,mark,title,keywords,userinfo,imsi,url,account,channel,art_source,OS,account_openid,abtestid,sub_topic,image_type,read_duration,position,app_ver,aduser_flag,location,pagetime,rec_reason,adid,vulgar,sub_list,ip,action_source,recall_word,video_type,channel_id,doc_id,product) = tups[0:36]
        if channel_id != "1":
            continue
        #if topic == "outer_video":
        #    continue
        #if ".mp4" in url:
        #    continue
        if art_source == "15":
            continue
        if not mid:
            continue
        if not doc_id:
            continue
        if doc_id.startswith("AD_") == True:
            continue
        if action != "6":
            continue
        #try:
        #    duration = float(read_duration)
        #except:
        #    continue
        #if duration >= 0 and duration < 3:
        #    continue
        if product != sys.argv[1]:
            continue
        if int(app_ver) < 6511:
            continue
        if rec_reason != '931':
            continue
        output = doc_id + "\tcl"
        print output.encode("gbk","ignore")
    if len(tups) < 37:
        continue
    if tups[0] == "resp":
        (resp,mid,tm,article_cnt,num,mark_tag,title,reason,read_num,topic,keywords,pub_time,article_template,img_list,url,account,channel,flag,openid,ab_test_id,sub_topic,userinfo,position,version,aduser_flag,user_location,pagetime,rec_reason,ad_id,vulgar,book_word,ip,recall_word,video_type,channel_id,doc_id,product) = tups[0:37]
        if channel_id != "1":
            continue
        #if topic == "outer_video":
        #    continue
        #if ".mp4" in url:
        #    continue
        if not mid:
            continue
        if not doc_id:
            continue
        if doc_id.startswith("AD_") == True:
            continue
        if product != sys.argv[1]:
            continue
        if int(version) < 6511:
            continue
        if rec_reason != '931':
            continue
        output = doc_id + "\tpv"
        print output.encode("gbk","ignore")
