ps -ef | grep crawl_app_en_info.py | grep -v vim | awk '{print $2}' | xargs kill -9 
