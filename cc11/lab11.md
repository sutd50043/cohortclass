---
author: ISTD, SUTD
title: Lab 11 Spark
date: Feb 7, 2024
logo: 
footnote:
header-includes: |
 \usepackage{tikz}
 \usetikzlibrary{positioning}
 \usetikzlibrary{arrows}
 \usetikzlibrary{shapes.multipart}
---



# Learning outcome


By the end of this lesson, you are able to

* Submit PySpark jobs to a Spark cluster
* Paralelize data processing using PySpark 

# Google Colab versus aws

You have two options to run this lab: 
* Google Colab file: [https://colab.research.google.com/drive/1ZYjP-g9ZO_jqGXbGA_8uJt4hhroWE9m8?usp=sharing](https://colab.research.google.com/drive/1ZYjP-g9ZO_jqGXbGA_8uJt4hhroWE9m8?usp=sharing)
* Instructions below on aws AMI image or Flintrock cluster as per the previous class. 

The PySpark code you write will be identical, save for the URL / local file path from which you load the files. If you opt for Google Colab, then you can switch to the instructions there. 



# Submit a PySpark job to a Spark cluster 

1. Using FlintRock or the AMI image, launch a Hadoop-Spark cluster. For the ease of subsequence exercise, make sure you are at least in a t2.medium instance. 

2. On the Spark cluster master node, check out the following github repo if you have not already.

```bash
$ cd
$ mkdir git
$ cd git
$ git clone https://github.com/sutd50043/cohortclass/
```

if it exists, update

```bash
$ cd git
$ git pull
```

3. Change to the `~/git/cohort_problems/` directory


3. Copy some data into HDFS `/input/` if it is empty, we re-use the data from cc10.

```bash
$ hdfs dfs -mkdir /input/
$ hdfs dfs -rm -r /output
$ hdfs dfs -put ~/git/cohortclass/cc10/data/TheCompleteSherlockHolmes.txt /input/
```


5. Edit the PySpark source code in `cc11/wordcount.py` so that it uses the correct HDFS address (private IP of your master node)!!!


6. Start the job

If you are using the flintrock cluster and did not install yarn: look for the private IP of your master node in the EC2 dashboard and run: 

```bash
$ spark-submit --master spark://<internal-ip-of-spark-master>:7077 cc11/wordcount.py  
```

Otherwise, if you are using the AMI image, or you installed spark: 

```bash
$ spark-submit --master yarn cc11/wordcount.py 
```

Did you get an error? Be sure to check: 
- You have provided the internal IP of the master node inside the `wordcount.py` code. 
- The output folder specified in `wordcount.py` does not yet exist. 


7. Check the output

```bash
$ hdfs dfs -cat /output/*
```


# Exercise 1

Write a PySpark application which takes a (set of) Comma-seperated-value (CSV) file(s) with 2 columns and output a CSV file with first two columns same as the input file, and the third column contains the values obtained by splitting the first column using the second column as delimiter.

For example, given input from a HDFS file: 

```
50000.0#0#0#,#
0@1000.0@,@
1$,$
1000.00^Test_string,^
```


the program should output

```
50000.0#0#0#,#,['50000.0', '0', '0']
0@1000.0@,@,['0', '1000.0', '']
1$,$,['1', '']
1000.00^Test_string,^,['1000.00', 'Test_string']
```

back to the HDFS. 

# Exercise 2 


Write PySpark application which aggregates (counts) a (set of) CSV file(s) with 4 columns based on its third column, the destination IP. 

Given input 

```
05:49:56.604899, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604900, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604899, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604900, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604899, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604900, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604899, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604900, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604899, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604900, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604899, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604900, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604899, 10.0.0.2.54880, 10.0.0.3.5001, 2
05:49:56.604908, 10.0.0.3.5001, 10.0.0.2.54880, 2
05:49:56.604908, 10.0.0.3.5001, 10.0.0.2.54880, 2
05:49:56.604908, 10.0.0.3.5001, 10.0.0.2.54880, 2
05:49:56.604908, 10.0.0.3.5001, 10.0.0.2.54880, 2
05:49:56.604908, 10.0.0.3.5001, 10.0.0.2.54880, 2
05:49:56.604908, 10.0.0.3.5001, 10.0.0.2.54880, 2
05:49:56.604908, 10.0.0.3.5001, 10.0.0.2.54880, 2
```
the program should output

```
 10.0.0.3.5001,13
 10.0.0.2.54880,7
```


# Exercise 3

Given the same input as Exercise 2, write a PySpark application which outputs the following: 

```
05:49:56.604899,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604900,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604899,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604900,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604899,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604900,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604899,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604900,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604899,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604900,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604899,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604900,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604899,10.0.0.2.54880, 10.0.0.3.5001, 2, 13
05:49:56.604908, 10.0.0.3.5001,10.0.0.2.54880, 2, 7
05:49:56.604908, 10.0.0.3.5001,10.0.0.2.54880, 2, 7
05:49:56.604908, 10.0.0.3.5001,10.0.0.2.54880, 2, 7
05:49:56.604908, 10.0.0.3.5001,10.0.0.2.54880, 2, 7
05:49:56.604908, 10.0.0.3.5001,10.0.0.2.54880, 2, 7
05:49:56.604908, 10.0.0.3.5001,10.0.0.2.54880, 2, 7
05:49:56.604908, 10.0.0.3.5001,10.0.0.2.54880, 2, 7
```


In the event the input is very huge with too many unique destination IP values, can your program scale?


The questions were adopted from 

```url
https://jaceklaskowski.github.io/spark-workshop/exercises/
```
