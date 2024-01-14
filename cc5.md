# 50.043 - Cohort Class 5

## Learning Outcomes

By the end of this unit, you should be able to 


1. Explain the roles and functionality of a disk manager
2. Explain the roles and functionality of a Buffer Pool
3. Explain the LRU and Clock Replacement Policy
4. Explain the different collision handling mechanisms of Hash Table
5. Explain the structure of a B+ Tree
6. Explain the lookup / insert / delete operations over a B+ Tree.


## Recap Disk Manager and Buffer Pool

* Disk manager maps tables to data files
* Each data file contains a collection of pages (pages vs block)
* Each page contains a collection of tuples, header and indices.
* Buffer Pool serves as a middle man between DB operation and the physical disk, it is a cache. 
    * Buffer pool contains a set of frames

The Buffer Pool maintains the following information,

1. Page to frame mapping
2. Whether a page is *pinned*. A page is pinned means it is being accessed currently. When a data operation (query/insert/update/delete) is performed it will pin all the required pages. When the operation is completed, the pages are unpinned. Note that in a full scale system, we might see concurrent accesses to pages, thus, in most of the situation, the Buffer Pool maintains a pin counter per slot.
3. Whether a page is dirty.
4. Extra information to support the eviction policy.

## Recap on Eviction Policy

#### LRU Policy

The Least Recently Used (LRU) Policy works as follows,

1. pinned frames should not be evicted
2. keep track of the timestamp when frame's pin was set to 0. 
3. evict the page in the frame with the smallest (oldest) timestamp.

In details steps.

Initialize all frames to be empty with pincount 0

1. when a page is being pinned
    1. if the page is already in the pool, increase the pincount, return the page in the frame.
    2. otherwise, 
        1. find the frames with 0 pincount, find the one oldest timestamp, write it to disk if it is dirty.
        2. load the new page to this vacant frame, set pincount = 1
1. when a page is being unpinned, decrease the pincount and update the timestamp to the current time.

## Exercise 1

You have 4 frames in the buffer pool. Given this access pattern (buffer is empty at start)

A B C D A F A D G D G E D F​

1. What is the hit rate if you use LRU policy? Show the final state of the buffer pool.​ (Hit rate is the number of page hits / total page pin requests)
2. Same question, but for MRU policy.​
3. When would MRU be better than LRU?




## Recap Bucket Hashing 

The idea behind Bucket Hashing (a.k.a extensible hashing) is to 
* store hashed values in buckets (relative small fixed size arrays, so that the sequential search is not expensive). All buckets have the same size.
* use a $n$ least significant bits (LSB) of the hashed value to decide in  which bucket it should be placed.
* increase $n$ and add new bucket gradually as some bucket becomes full.

The Bucket Hashing algorithm starts with a global slot array, a bucket.
It maintains a set of integer values of $n$ LSB. $G$ denotes the global value of $n$ LSB, there is one and only one. $L$ denotes the local values of $n$ LSB, there is one $L$ per bucket. For all buckets, $L \leq G$. The algorithm start with some small numbers of $G$ and $L$. 


##### Bucket Hashing Insertion
To insert a value $X$ (for simplicity, we treat $X$ same as $hash(X)$)

1. lookup the bucket for $X$ based on the last $G$ bits of $X$.
    1. if the bucket $i$ is not full, insert $X$ there.
    2. otherwise
        1. if the bucket $i$ having $L < G$
            1. add a new bucket $j$ having same $L$ as $i$, 
            2. redistribute data from $i$ to $i$ and $j$. 
            3. increase $L$ for both buckets $i$ and $j$.
            4. update the slot array
        2. otherwise
            1. double the slot array
            2. add a new bucket $j$ having same $L$ as $i$
            3. redistribute data from $i$ to $i$ and $j$. 
            4. increase $L$ for both buckets $i$ and $j$.
            5. increase $G$ 
            6. update the slot array

## Exercise 2

Consider an extendible hashing scheme (Bucket Hashing):​
* Hash function is the binary representation of the key​, e.g. H(3) = 000011​
* Starting from an empty table, insert 15,3,7,14​
* Draw the final table hash table, including the slot array​
* Size of each bucket is 2​


## Recap B+ Tree

A B+ Tree is a generalization of a perfect balanced binary search tree, with the following adjustment

1. Let $d$ denotes the order.
2. The root node may have $1$ to $2*d$ entries.
3. Each non-root node may have $d$ to $2*d$ entries (half-full).
4. The each in a node consist of a key and a value, except for the first entry i.e. $v_1, (k_2, v_2), (k_2, v_2), ... , (k_{n}, v_n)$. 
5. The values in non-leaf nodes are reference to the children.
6. The values in the leaf nodes are reference to records in the data file/page/block.
7. Given two consecutive entries $(k_i, v_i), (k_{i+1}, v_{i+1})$, where $v_{i}$ is a reference to a subtree, for all values in subtree, their index values must be in between $k_i$ and $k_{i+1}$. For the first entry, its lower bound is definedby the key coming from the parent. (Similar observation applies to the last entry.)
8. All the leaf nodes for a doublely linked list, which enables the range search operation.

##### Look-up

To search for a value with key $k$ in a B+ Tree, we start from the root node

1. find the value $v$ between $k_1$ and $k_2$ such that $k_1 \leq k < k_2$. Note that $k_1$ might not exist if $k_2$ is the first entry's key, $k_2$ might not exist if $k_1$ is the last entry's key.
    1. if the current node is a non-leaf node, we move the current node to the node pointed by $v$, we repeat the process recursively
    1. if the current node is a leaf node, we return the disk data pointed by $v$.

It is clear that the time complexity is $O(log(N))$

##### Insertion

To insert a value with key $k$ into a B+ Tree, we follow the algorithm as follows

1. find the leaf node $L$ with the current interval where $k$ should fit, (same as the look-up operation). 
2. insert_to_leaf($L$, $k$)
3. def insert_to_leaf($L$,k)
    1. if $L$ is not full, just insert, we are done!
    2. otherwise
        1. create a new node $L'$. 
        2. (update linked list, only for leaf node), let $L'' = succ(L)$,  then $succ(L) = L'$ and $succ(L') = L''$.
        3. redistribute entries evenly between $L$ and $L'$. 
        4. copy up the middle key, with the value as a pointer to $L'$, that is to insert a new data entry in the parent node. insert_to_nonleaf(parent($L$), middle_key)
4. def insert_to_nonleaf($N$, k)
    1. if $N$ is not full, just insert, we are done!
    2. otherwise
        1. create a ne wnode $N'$.
        2. redistribute entries evenly between $N$ and $N'$.
        3. push up (note, not copy) the middle key, with the value as a pointer to $N'$. 
            1. if $N$ is not a root node, insert_to_nonleaf(parent(N), middle_key)
            2. otherwise, create an empty node as the new root node, insert_to_nonleaf(parent(N), middle_key)


##### Deletion 

Given a node $N$, let $|N|$ denote the number of entries in $N$.

To delete a value with key $k$ from a B+ Tree, we follow the algorithm as follows

1. find the leaf node $L$ with the current interval where $k$ should fit, (same as the look-up operation). 
2. delete_from_leaf($L$, $k$)
3. def delete_from_leaf($L$, $k$)
    1. remove the entry with $k$
        1. if $L$ is at least half-full (i.e. $|L -\{k\}| \geq d$), we are done!
        2. otherwise
            1. if $L$ has a sibling $L'$, and $k'$ is the key from the parent that divides $L$ and $L'$, such that $|L \cup \{k'\} \cup L'-\{k\}| \geq 2*d$
                1. find the new middle key in $L \cup \{k'\} \cup L'-\{k\}$, say $k''$, replace $k'$ by $k''$ in $parent(L)$
                2. if $|L \cup \{k'\} \cup L'-\{k\}|-1 \geq 2*d$
                    1. re-distribute $L \cup \{k'\} \cup L' - \{k,k''\}$ among the two leaf nodes.
                    2. otherwise, re-distribute $L \cup \{k'\} \cup L'- \{k\}$ among the two leaf nodes, i.e. $k''$ is copied up.
            2. otherwise
                1. merge $L$ with its sibling $L'$ into a new node as $L \cup \{k'\} \cup L' - \{k\}$, where $k'$ is the key from the parent dividing $L$ and $L'$.
                2. delete_from_nonleaf($parent(L)$, $k'$)

4. def delete_from_nonleaf($N$, $k$)
    1. remove the entry with $k$
    2. if $N$ is a root node and $|N -\{k\}| > 0$, we are done!
    3. if $N$ is a root node and $|N -\{k\}| == 0$, we remove $N$ entirely.
    4. if $N$ is not a root node and $N$ is at least half full, we are done.
    5. otherwise
        1. if $N$ has a sibling $N'$, and $k'$ is the key from the parent that divides $N$ and $N'$, such that $|N \cup N' - \{k\}| \geq 2*d$, 
            1. find the new middle key in $N \cup \{k'\} \cup N'$, say $k''$, replace $k'$ by $k''$ in $parent(N)$, redistribute $|N \cup N' - \{k\}|$ among the two nodes. 
        2. otherwise
            1. merge $N$ with its sibling $N'$ into a new node as $N \cup \{k'\} \cup N' - \{k\}$, where $k'$ is the key from the parent dividing $N$ and $N'$.
            2. delete_from_nonleaf($parent(N)$, $k'$)


## Exercise 3

Given the following B+ Tree with $d = 2$

![](./images/cc5_bplus.png)

1. Draw the tree after inserting 13, 15, 18, 25, 4 then deleting 4, 25, 18, 15, 13​
2. What did you observe?​
