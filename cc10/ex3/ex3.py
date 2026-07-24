from mapreduce import flatMap, reduceByKey2, shuffle

##########################
# copied from exercise2 and lab10 ex3 hints
def read_db(filename):
    db = []
    with open(filename, 'r') as f:
        for l in f:
            db.append(l)
    f.close()
    return db

test_db = read_db("./data/price.csv")
priceTable = map(lambda ln:ln.strip().split(','),test_db)
# priceTable is a generator, can only be iterated once
#print("Price Table:", list(priceTable))

# mapper for projection
def get_supplierID(cols): return cols[1]
# projection supplierID
projection_result = map(get_supplierID, priceTable)
#print("Projection result:", list(projection_result)[:20])
# alternative
projection_result = map(lambda x:x[1], priceTable)

# selection price>800
def get_price(cols):return float(cols[2])
filter_result = filter(lambda x:get_price(x) > 800, priceTable)
#print("Filter result:", list(filter_result))
##########################



######### join #########

# Step 1: Read and parse stock data
test_db = read_db("./data/price.csv")
priceTable = map(lambda ln:ln.strip().split(','),test_db)
test_db2 = read_db("./data/stock.csv")
stockTable = map(lambda ln:ln.strip().split(','),test_db2)

# Step 2: Tag and emit keyed tuples
# input: a row in a table, e.g., [productID, supplierID, price]
# output: key-value pair (productID, (tag, row)) tag = 'price' or 'stock'

def tag_price(line):
    pass
def tag_stock(line):
    pass

mapped_price = map(tag_price, priceTable)
mapped_stock = map(tag_stock, stockTable)
# Step 3: Shuffle to group by productID

# Step 4: filter out records only appear in one table

# Step 5: Flattern results
# output: (pId, [pId, sId, price, stock])
# use map

joined_result = None
print("Joined Result:")
print(list(joined_result))