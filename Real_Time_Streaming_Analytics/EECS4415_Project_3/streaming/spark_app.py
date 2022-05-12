
import sys
import requests
from datetime import datetime, timedelta
import re
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession, Window
from pyspark.sql.functions import row_number, monotonically_increasing_id
import numpy as np
import pandas as pd

def calculateCurrentTime(currentTime):
    splitedTime = re.split('[ ]', currentTime)
    pushed_date = splitedTime[0]
    pushed_time = splitedTime[1]
    time_li = pushed_time.split(":")
    currentHour = time_li[0]
    currentMin = time_li[1]
    current_timeStamp = pushed_date+currentHour+currentMin
    # Ex) 2022-04-07T23:09:37Z ==> 2022-04-072309
    return current_timeStamp

def aggregate_count(new_values, total_sum):
	  return sum(new_values) + (total_sum or 0)

def get_sql_context_instance(spark_context):
    if('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SparkSession(spark_context)
    return globals()['sqlContextSingletonInstance']

def send_df_to_dashboard(df):
    # Send total count, star average, pushed time information in pandas dictionary form
    url = 'http://webapp:5000/updateData'
    data = df.toPandas().to_dict('list')
    requests.post(url, json=data)

def send_df_to_dashboard2(df):
    # Send most frequent top 10 words information in pandas dictionary form
    url = 'http://webapp:5000/updateData2'
    data = df.toPandas().to_dict('list')
    requests.post(url, json=data)

def process_rdd(time,rdd):
    pass
    print("----------- %s -----------" % str(time))
    try:

        # Transform received rdd to data frame

        sql_context = get_sql_context_instance(rdd.context)

        total = rdd.filter(lambda word: "Python" == word[0] or "Java" == word[0] or "CSharp" == word[0]).map(lambda w: Row(Language=w[0], Count=w[1]))
        totalDf = sql_context.createDataFrame(total)
        totalDf.createOrReplaceTempView("total")

        stars = rdd.filter(lambda word: "PythonStar" == word[0] or "JavaStar" == word[0] or "CSharpStar" == word[0]).map(lambda w: Row(LanguageStar=w[0].split("Star")[0], TotalStars=w[1]))
        starDf = sql_context.createDataFrame(stars)
        starDf.createOrReplaceTempView("star")

        pushedTime = rdd.filter(lambda word: "Time," in word[0] and word[0].split(",")[1] == calculateCurrentTime(str(datetime.utcnow()-timedelta(minutes=1)))).map(lambda w: Row(PushedIn60sec=w[0].split(",")[0].split("PushedTime")[0], PushedIn60secCount=w[1]))
        pushedtimeDf = sql_context.createDataFrame(pushedTime)
        pushedtimeDf.createOrReplaceTempView("time")

        wordsCount = rdd.filter(lambda word: "Word," in word[0]).map(lambda w: Row(Language=w[0].split(",")[0].split("Word")[0], Word=w[0].split(",")[1]+","+str(w[1]), WordCount=w[1]))
        wordsCountDf = sql_context.createDataFrame(wordsCount)
        wordsCountDf.createOrReplaceTempView("word")
        p = sql_context.sql("select Word as PythonWordTop10 from word where Language = 'Python' order by WordCount DESC limit 10")
        j = sql_context.sql("select Word as JavaWordTop10 from word where Language = 'Java' order by WordCount DESC limit 10")
        c = sql_context.sql("select Word as CSharpWordTop10 from word where Language = 'CSharp' order by WordCount DESC limit 10")
        p = p.withColumn("index",row_number().over(Window.orderBy(monotonically_increasing_id())))
        j = j.withColumn("index",row_number().over(Window.orderBy(monotonically_increasing_id())))
        c = c.withColumn("index",row_number().over(Window.orderBy(monotonically_increasing_id())))
        p.createOrReplaceTempView("pyw")
        j.createOrReplaceTempView("jaw")
        c.createOrReplaceTempView("csw")

        # Print
        wordResultDf = sql_context.sql("select pyw.index, PythonWordTop10, JavaWordTop10, CSharpWordTop10 from (select jaw.index, JavaWordTop10, CSharpWordTop10 from jaw, csw where jaw.index = csw.index) as temp ,pyw where pyw.index = temp.index order by pyw.index")
        wordResultDf.show()
        resultDf = sql_context.sql("select Language, Count, StarAverage, PushedIn60secCount from (select Language, Count, round(TotalStars/Count, 2) as StarAverage from total, star where Language = LanguageStar) as temp, time where temp.Language = PushedIn60sec order by Language DESC")
        resultDf.show()

        # Send data to dashboard for web application
        send_df_to_dashboard(resultDf)
        send_df_to_dashboard2(wordResultDf)

    except ValueError:
        print("Waiting for data...")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

if __name__ == "__main__":
    DATA_SOURCE_IP = "data-source"
    DATA_SOURCE_PORT = 9999
    sc = SparkContext(appName="Project3")
    sc.setLogLevel("ERROR")
    # Set batch per 60 sec
    ssc = StreamingContext(sc, 60)
    ssc.checkpoint("checkpoint_Project3")
    data = ssc.socketTextStream(DATA_SOURCE_IP, DATA_SOURCE_PORT)

    wordsRdd = data.flatMap(lambda word: [str(word)])

    # Separate data using filter and, map and reduce them

    # Recently pushed time fora each language repository
    pythonPushedTime = wordsRdd.filter(lambda word: "PythonPushedTime," in word).map(lambda x: (x,1)).reduceByKey(lambda a, b: a + b).updateStateByKey(aggregate_count)
    javaPushedTime = wordsRdd.filter(lambda word: "JavaPushedTime," in word).map(lambda x: (x,1)).reduceByKey(lambda a, b: a + b).updateStateByKey(aggregate_count)
    csharpPushedTime = wordsRdd.filter(lambda word: "CSharpPushedTime," in word).map(lambda x: (x,1)).reduceByKey(lambda a, b: a + b).updateStateByKey(aggregate_count)

    # Total stars of repository for each language repository
    starSum = wordsRdd.filter(lambda word: "PythonStar," in word or "JavaStar," in word or "CSharpStar," in word).map(lambda x: (x.split(",")[0],int(x.split(",")[1]))).reduceByKey(lambda a, b: a + b).updateStateByKey(aggregate_count)

    # Total count for each language repository
    languageSum = wordsRdd.filter(lambda word: (word == "Python" or word == "Java" or word == "CSharp")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).updateStateByKey(aggregate_count)

    # Description words per each language repository
    pythonWord = wordsRdd.filter(lambda word: "PythonWord," in word).map(lambda x: (x,1)).reduceByKey(lambda a, b: a + b).updateStateByKey(aggregate_count)
    javaWord = wordsRdd.filter(lambda word: "JavaWord," in word).map(lambda x: (x,1)).reduceByKey(lambda a, b: a + b).updateStateByKey(aggregate_count)
    csharpWord = wordsRdd.filter(lambda word: "CSharpWord," in word).map(lambda x: (x,1)).reduceByKey(lambda a, b: a + b).updateStateByKey(aggregate_count)

    # Make the rdds one rdd and send it for further process
    wordcountRdd = pythonWord.union(javaWord).union(csharpWord)
    pushedTimeRdd = pythonPushedTime.union(javaPushedTime).union(csharpPushedTime)
    languageSum.union(starSum).union(pushedTimeRdd).union(wordcountRdd).foreachRDD(process_rdd)

    ssc.start()
    ssc.awaitTermination()