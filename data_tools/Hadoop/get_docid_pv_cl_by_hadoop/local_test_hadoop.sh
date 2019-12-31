head -n 100000 data/part-00000 | python hadoop_script/mapper.py sgsapp | sort | python hadoop_script/reducer.py
