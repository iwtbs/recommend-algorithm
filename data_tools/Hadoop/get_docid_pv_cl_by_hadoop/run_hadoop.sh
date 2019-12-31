start_day_hour=`date -d "-2 hours" +"%Y%m%d%H"`
start_day_hour=`date -d "-1 days" +"%Y%m%d"`23
start_day_hour_2=${start_day_hour:0:8}" "${start_day_hour:8:10}
echo ${start_day_hour}
echo ${start_day_hour_2}

product='sgsapp'

interval=24

HADOOP_DATA_DIR=**
HADOOP_OUTPUT_DIR=***/${start_day_hour}

hadoop fs -test -e ${HADOOP_DATA_DIR}
if [ $? -ne 0 ];then
    echo "hadoop data dir ${HADOOP_DATA_DIR} does not exists!"
    exit -1
fi

hadoop fs -test -e ${HADOOP_OUTPUT_DIR}
if [ $? -eq 0 ];then
    hadoop fs -rmr ${HADOOP_OUTPUT_DIR}
fi

for((i=0;i<${interval};i++))
do
    
    tm=`date -d "${start_day_hour_2} -${i} hours" +"%Y%m%d%H"`
    file_dir=${HADOOP_DATA_DIR}/online1_${tm}
    #hadoop fs -test -e ${file_dir}
    #if [ $? -eq 0 ];then
    #    inputs=${inputs}" -input ${file_dir}"
    #fi
    inputs=${inputs}" -input ${file_dir}"
done

echo "Hadoop input dir: ${inputs}"


hadoop org.apache.hadoop.streaming.HadoopStreaming \
-files hadoop_script \
-D mapred.map.tasks=64 \
-D mapred.reduce.tasks=64 \
-D stream.num.map.output.key.fields=1 \
-D num.key.fields.for.partition=1 \
-D mapred.job.name=get_user_mid \
-D mapred.output.compress=true \
-D mapred.output.compression.type=BLOCK \
-D mapred.output.compression.codec=com.hadoop.compression.lzo.LzopCodec  \
-D mapred.task.timeout=3600000 \
-D mapreduce.map.memory.mb=2048 \
-D mapreduce.reduce.memory.mb=2048 \
-mapper "python hadoop_script/mapper.py ${product}" \
-reducer "python hadoop_script/reducer.py" \
${inputs} \
-output ${HADOOP_OUTPUT_DIR} \
-inputformat KeyValueTextInputFormat


hadoop fs -get ${HADOOP_OUTPUT_DIR} .
lzop -cd ${start_day_hour}/*.lzo > data/${product}_${start_day_hour}
rm -rf ${start_day_hour}
