#coding:gbk
import sys
import re

appid_list = []
appname_list = []


def judge_is_appid(app):
    parts = app.split('.')
    if len(parts) <= 1: # QQ
        return False
    if len(parts[-1]) == 0: # Link.
        return False
    if parts[-1] == 'com':
        return False        # Booking.com
    max_part_len = max(map(lambda x: len(x), parts))
    if max_part_len <= 1:
        return False    # B.A.W
    for part in parts:
        re_result = re.search('^[0-9]+$', part)
        if re_result:
            return False    # STracter_V2.0
    re_result = re.search('^[0-9a-zA-Z\._]+$', app)
    if re_result:
        return True
    else:
        return False


def output(appxx_list, output_path):
    fw = open(output_path, 'w')
    for appxx in appxx_list:
        fw.write(appxx + '\n')
    fw.close()


for line in file(sys.argv[1]):
    items1 = line.strip().split('\t')
    if len(items1) != 2:
        continue
    app = items1[0]
    times = int(items1[1])
    if times < int(sys.argv[2]):
	continue
    if judge_is_appid(app):
        appid_list.append(app)
    else:
        appname_list.append(app)


output(appid_list, sys.argv[3])
output(appname_list, sys.argv[4])
