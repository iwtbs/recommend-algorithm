python gen_appid_and_appname.py ../3_stat_app_times/data/app_times 300 ./data/appid ./data/appname

python crawl_app_info.py id ./data/appid ./data/appid_info

python crawl_app_info.py name ./data/appname ./data/appname_info
