[from mapreduce import *

# fix path if needed
import os
print(os.getcwd())
dir = '/Users/dorien_herremans/Dropbox/DoBrain/AC/Courses/big data 2023/big data 2023/lab/lab10/ex2/'

def read_db(filename):
    db = []
    with open(filename, 'r') as f:
        for l in f:
            db.append(l)
    f.close()
    return db
            
test_db = read_db(dir + "data/price.csv")

# TODO: FIXME
# the result should contain a list of suppliers, 
# with the average sale price for all items by this supplier.

# result = []

# mapper: 
def m(line):

    return

# reducer: 
def r(p):
    
    return 

m_out  = map(m, test_db)
result = reduceByKey2(r,m_out)

# print the results
for supplier,avg_price in result:
    print(supplier, avg_price)








## mini discussion answer

##  for aggregiation that can be defined using a commutative and associative binary operation, we should use reducebykey2, e.g. calculating median