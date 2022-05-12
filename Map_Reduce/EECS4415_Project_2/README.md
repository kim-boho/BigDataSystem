# EECS4415-Big Data Systems: Project 2 (20%)

**Title:** Distributed Big Data Analytics using Python   
**Start:** February 21, 2022, @ 9:00am EST   
**Due:** March 14, 2022, by 9:00pm EST

## Objectives

This project involves performing distributed analytics on a large-scale dataset using Python on a Hadoop cluster. The dataset is a subset of Yelp's businesses, reviews, and user data. It was originally put together for the Yelp Dataset Challenge, which is a chance for students to conduct research or analysis on Yelp's data and share their discoveries. The dataset consists of five JSON files, which contain information about businesses across 8 metropolitan areas in the USA and Canada.
The dataset can be found and downloaded [here](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3) (registration to Kaggle is required).

There are four questions in this project. You will write four sets of Python scripts that implement four MapReduce algorithms. The first set of scripts constructs an inverted index of the business categories; the second set computes frequency distributions about users; the third set finds top-K records; the fourth set analyzes the relationships between check-ins and businesses.

## Implementation
* You may clone this repository and implement your solution in the corresponding files. 
* The three lines in the *info.txt* file include information about you (first name, last name, and 9-digit student ID). Please update the *info.txt* file accordingly. For example, if your name is *Foo Bar* and your student ID is *123456789*. The *info.txt* file should be as follows:
    ```
    Foo
    Bar
    123456789
    ```
* All scripts are to be written using Python >= 3.7.0.
* You should use LF line terminators in your scripts.
* You may NOT change the shebang line(`#!/usr/local/bin/python3.9`) of the Python scripts in your submission.
* You may NOT use any third-party packages. Only [built-in Python libraries](https://docs.python.org/3.9/library/) are allowed.
* You should round your answer to at most 2 decimal places (only if necessary) using the built-in [`round()`](https://docs.python.org/3/library/functions.html#round) function.

Important notes:
* You should strictly follow the implementation instructions, the input/output format, and the filename. Implementations that do not follow the correct format will be marked as 0.
* You may NOT change the filename of the Python scripts and the output files (if any).
* The time limit for each set of scripts (MapReduce algorithm) is 360 seconds. If your script goes beyond the time limit, it will be terminated and marked as 0.
* To get full marks, your code must be well-commented.

**Hint:** It is highly recommended to test your implementations in the Docker-based Hadoop environment provided in [Lab3](https://eclass.yorku.ca/pluginfile.php/3465412/mod_folder/content/0/EECS4415-Tutorial3-HDFS.pdf) and [Lab4](https://eclass.yorku.ca/pluginfile.php/3482046/mod_folder/content/0/EECS4415-Tutorial4-MapReduce.pdf). We will use the same environment to evaluate your submission.

## Submission
You need to zip your repository and submit as one zip file with the name of *project2.zip* on eClass by the due date. The directory structure in *project2.zip* should look like this:

```
EECS4415_Project_2/
├─ q1mapper.py
├─ q1reducer.py
├─ q2mapper.py
├─ q2reducer.py
├─ q3mapper.py
├─ q3reducer.py
├─ q4mapper.py
├─ q4reducer.py
├─ info.txt
├─ README.md
├─ Q1.png
├─ .gitignore
```
You should strictly follow the specified directory structure. Implementations that do not follow the correct directory structure will be marked as 0.

**Hint:** Please note that you should not include any output files in your submission. We will execute your codes to generate the outputs and then compare them with the correct answers.

## Evaluation
Your scripts will be executed in a Hadoop cluster (Apache Hadoop 3.3.1). An automated judge will programmatically evaluate your solution. Please refer to each question for the detailed breakdown of project marks. Please note implementations that do not exactly follow the implementation and submission instructions will be marked as 0 by the judge system.


## Q1. Distributed Construction of the Inverted Index (25%)
In information retrieval, an inverted index is an index data structure that stores a mapping from words to a collection of documents that they appear in. Your task is to build an inverted index that maps categories (of businesses) to businesses. In other words, given a collection of businesses, an inverted index is a dictionary where each category is associated with a list of the business ids (comma-separated) that belong to that category. See the example below:

![Inverted index](Q1.png)

In this question, your task is to write two Python scripts (***q1mapper.py*** and ***q1reducer.py***) that implement a MapReduce algorithm for constructing the inverted index. For a given collection of Yelp business data ([*yelp_academic_dataset_business.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_business.json)), the algorithm computes the inverted index of the categories to businesses that are **open on the weekend** (Saturdays, Sundays, or both). The output of the MapReduce job should consist of a number of lines in the following format:
```
category	[id1, id2, id3, id4]
```
Namely, each line should contain a category and a list of indexes, separated by **a tab character** (\t). The order does not matter.

For example:

```
Hotels & Travel	['01OmT3PXceLBRsYyWdummy', '023Lc6yStQnKuqymEdummy', '03PyMX1yFb_VYgPw4dummy']
Canadian (New)	['04L7iPGEirkbMLjCfdummy', '05IsY_MFfDBY7JUXgdummy', '06kN4XJq0TtubaPyqdummy', '07sJIkOlJsO1e1PHtdummy']
```

Your script should be run as follows:
```
$ yarn jar /path-to-jar/hadoop-streaming-3.3.1.jar -files q1mapper.py,q1reducer.py -mapper /path-to-mapper/q1mapper.py -reducer /path-to-reducer/q1reducer.py -input /path-to-json-in-hdfs/yelp_academic_dataset_business.json -output /path-to-directory-in-hdfs/output
```
For example:
```
$ yarn jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -files q1mapper.py,q1reducer.py -mapper ./q1mapper.py -reducer ./q1reducer.py -input /yelp_academic_dataset_business.json -output /output
```
The original file provided by Kaggle ([*yelp_academic_dataset_business.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_business.json)) will be used for evaluation.

## Q2. Distributed Computation of Frequencies (25%)
In this question, your task is to write two Python scripts (***q2mapper.py*** and ***q2reducer.py***) that implement a MapReduce algorithm for computing frequencies. For a given collection of Yelp user data ([*yelp_academic_dataset_user.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_user.json)), the algorithm computes the percent proportion of Yelp accounts created in each month (irrespective of the year). For example, the input dataset contains four users who joined Yelp on 2010-01-01, 2011-02-01, 2018-03-01, and 2018-04-01, respectively. In this case, the percent proportions should be 25% for January, 25% for February, 25% for March, 25% for April, and 0% for the other months. The output of the MapReduce job should be one line per pair of values separated by **a tab character** (\t) as follows:
```
month(integer)	proportion%
```
For example:
```
1	1.23%
2	2.34%
3	3.45%
4	4.56%
5	5.67%
6	6.78%
7	7.89%
8	8.9%
9	9.1%
10	10.24%
11	20.48%
12	19.36%	
```
Due to rounding, the percentages may not add up to 100%. 

Your script should be run as follows:
```
$ yarn jar /path-to-jar/hadoop-streaming-3.3.1.jar -files q2mapper.py,q2reducer.py -mapper /path-to-mapper/q2mapper.py -reducer /path-to-reducer/q2reducer.py -input /path-to-json-in-hdfs/yelp_academic_dataset_user.json -output /path-to-directory-in-hdfs/output
```
For example:
```
$ yarn jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -files q2mapper.py,q2reducer.py -mapper ./q2mapper.py -reducer ./q2reducer.py -input /yelp_academic_dataset_user.json -output /output
```
The original file provided by Kaggle ([*yelp_academic_dataset_user.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_user.json)) will be used for evaluation.


## Q3. Distributed Computation of the Top-k Reviews (25%)
Yelp users can vote a review as useful, funny, or cool (UFC). The total number of UFC votes of a review is the sum of useful, funny, and cool votes it has received. For example, a review has received 10 useful votes, 20 funny votes, and 30 cool votes. In this case, the total number of UFC votes is 60 for this review. For a given collection of Yelp review data ([*yelp_academic_dataset_review.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_review.json)), your task is to write two Python scripts (***q3mapper.py*** and ***q3reducer.py***) that implement a MapReduce algorithm to find the **top 4415** reviews with the most UFC votes in descending order (from the most UFC votes to the least). If there are multiple reviews with the same number of UFC votes, they should be sorted in descending order according to the date created (from the most recently created to the least). The output of the MapReduce job should be one line per pair of values separated by **a tab character** (\t) as follows:
```
review_id	#UFC_votes
```
For example:
```
AafK4UJ4d75U9bK04dummy	4096
BbydWwiOFHkB_ajwCdummy	2048
CcM3BH28X7hLGOEDedummy	1024
DdG2x0EE7t1aKqSxEdummy	512
EeG2x0CS7t1aKqSxEdummy	256
FfG2x0447t1aKqSxEdummy	128
GgG2x0157t1aKqSxEdummy	64
HhG2x0157t1aKqSxEdummy	32
IiG2x0157t1aKqSxEdummy	32
JjG2x0157t1aKqSxEdummy	16
KkG2x0157t1aKqSxEdummy	8
...
```
In the example above, the reviews HhG2x0157t1aKqSxEdummy and IiG2x0157t1aKqSxEdummy have the same number of UFC votes. The review HhG2x0157t1aKqSxEdummy comes before IiG2x0157t1aKqSxEdummy because the review HhG2x0157t1aKqSxEdummy was created later than IiG2x0157t1aKqSxEdummy.

Your script should be run as follows:
```
$ yarn jar /path-to-jar/hadoop-streaming-3.3.1.jar -files q3mapper.py,q3reducer.py -mapper /path-to-mapper/q3mapper.py -reducer /path-to-reducer/q3reducer.py -input /path-to-json-in-hdfs/yelp_academic_dataset_review.json -output /path-to-directory-in-hdfs/output
```
For example:
```
$ yarn jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -files q3mapper.py,q3reducer.py -mapper ./q3mapper.py -reducer ./q3reducer.py -input /yelp_academic_dataset_review.json -output /output
```
The original file provided by Kaggle ([*yelp_academic_dataset_review.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_review.json)) will be used for evaluation.

## Q4. Distributed Generation of Checkin Logs (25%)
The Yelp check-in data ([*yelp_academic_dataset_checkin.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_checkin.json)) contains the information about check-ins on businesses, in which each line consists of a business ID and a comma-separated list of timestamps for each check-in. In this question, your task is to write two Python scripts (***q4mapper.py*** and ***q4reducer.py***) that implement a MapReduce algorithm to generate check-in logs in a distributed manner. Each line of the check-in logs should contain a unique identifier (UID), the timestamp of the check-in, and the name of the business. The order of the log does not matter. The UID should follow the same format as the Yelp dataset, which is a **random-generated unique string with 22 characters**. The valid characters to construct UID include: uppercase letters (A-Z), lowercase letters (a-z), numbers (0-9), underscore (_), and dash (-). The output of the MapReduce job should be one line per triplet (separated by **a tab character**) as follows:

```
uid	timestamp	business_name
```
For example:
```
cXAC0I4CEeykaetxJdummy	2022-02-21 17:02:08	York University
cXAD8o4CEeyPW-txJdummy	2022-02-22 14:07:04	York University
cXAH6Y4CEey_COtxJdummy	2022-05-15 06:28:29	Lassonde School of Engineering
cXAGJo4CEeyuZutxJdummy	2022-03-04 00:17:43	Lassonde School of Engineering
TvpK-Y4CEeyr1DUGsdummy	2022-01-25 03:19:54	YYZ
TvpLQ44CEeyRhDUGsdummy	2022-01-25 04:34:30	YYZ
TvpLjo4CEeyigDUGsdummy	2022-01-26 03:53:17	YYZ
...
```
Two input files ([*yelp_academic_dataset_checkin.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_checkin.json) and [*yelp_academic_dataset_business.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_business.json)) will be paased to the MapReduce job. Your script should be run as follows:
```
$ yarn jar /path-to-jar/hadoop-streaming-3.3.1.jar -files q4mapper.py,q4reducer.py -mapper /path-to-mapper/q4mapper.py -reducer /path-to-reducer/q4reducer.py -input /path-to-json-in-hdfs/yelp_academic_dataset_business.json -input /path-to-json-in-hdfs/yelp_academic_dataset_checkin.json -output /path-to-directory-in-hdfs/output
```
For example:
```
$ yarn jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar -files q4mapper.py,q4reducer.py -mapper ./q4mapper.py -reducer ./q4reducer.py -input /yelp_academic_dataset_business.json -input /yelp_academic_dataset_checkin.json -output /output
```
The original files provided by Kaggle ([*yelp_academic_dataset_checkin.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_checkin.json) and [*yelp_academic_dataset_business.json*](https://www.kaggle.com/yelp-dataset/yelp-dataset/version/3?select=yelp_academic_dataset_business.json)) will be used for evaluation.
