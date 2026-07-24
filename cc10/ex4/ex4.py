from functools import reduce


class Tree:
    def __init__(self,value,left=None,right=None):
        self.value = value
        self.left = left
        self.right = right
    def __str__(self):
        return "{value:%s, left:%s, right:%s}" %(str(self.value), str(self.left), str(self.right))
    
mytree = Tree(17, Tree(11, Tree(4), Tree(13)), Tree(5, None, Tree(30)))
print(mytree)

# fix me
def tmap(func, tree):
    new_value = None
    new_left = None
    new_right = None
    return Tree(new_value, new_left, new_right)

print(tmap(lambda x: x + 1, mytree))

# fix me
def treduce(func, tree, acc):
    return acc

print(treduce(lambda x, y: x + y, mytree, 0))

####################################
myllist = [ ["one", "two", "two", "three", "three", "three"], 
           ["four", "four", "four", "four", "five"], 
		   ["five", "five", "five", "five"] ]

# fix me
def llmap(func, ll):
    pass

ll1 = llmap(lambda w:1, myllist)
print(ll1)

# fix me
def llreduce(func, ll, acc):
    return acc
ll2 = llreduce(lambda x, y: x + y, ll1, 0)
print(ll2)