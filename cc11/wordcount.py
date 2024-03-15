import sys
from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("Wordcount Application")
sc = SparkContext(conf=conf)

name_node = "localhost" # fixme

text_file = sc.textFile("hdfs://{}:9000/input/".format(name_node))
counts = text_file.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("hdfs://{}:9000/output/".format(name_node))
sc.stop()
