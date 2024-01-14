# 50.043 Transactions


## Learning Outcomes

1. apply undo, redo, undo/redo logging to recover database from crashes
1. apply undo, redo, undo/redo logging with nonquiescent checkpoints to recover database from crashes.
1. apply conflict serializability check to schedules.
1. apply 2PL to generate conflict serialzable schedules.


## Recap Undo Logging 

The undo logging is governed by the following two rules. 

1. In a transaction `T`, before writing the updated page `X` containing changes `V` to disk, we must append `<T, update, X, V.old_value>` to the log. Note that we use a simplified log entry compared to the notes, we include the object being updated in  the log entry instead of the object's file id, page id and offset.
2. When `T` is being committed, to make sure all log entries are written to disk, all updated pages are written to disk. Then append `<T, commit>` to the log on the disk.

During crash recovery the recovery manager scans the log backwards to look for  transactions that has a `begin` but without `commit` (and without `abort`). Undo the updates belong to these transactions. 

## Exercise 1

Given the initial state A=B=C=0, and 3 transactions T1, T2 and T3

* T1: A=10, B=20
* T2: A=40, C=30, A=50
* T3: B=75


They are executed using *undo logging*, with the log content (on disk) below

```
1.  <T1, BEGIN>​
2.  <T1, A, 0>​
3.  <T1, B, 0>​
4.  <T1, COMMIT>​
5.  <T2, BEGIN>​
6.  <T2, A, XXX>​
7.  <T2, C, 0>​
8.  <T2, A, 40>​
9.  <T2, COMMIT>​
10. <T3, BEGIN>​
11. <T3, B, XXX>
```



* Question 1.1 - Fill in the `XXX` in the log.
* Question 1.2 - The system crashes and recovers. What are values of A,B,C on disk after recovery,
    1. If the log when the crash happened contains line 1-10​
    2. If the log when the crash happened contains line 1-7​


## Recap Redo-logging 

The redo logging is governed by the following rules

1.  In a transaction `T`, before writing the updated page `X` containing changes `V` to disk, we must have appended `<T, update, X, V.new_value>` to the log and appended `<T, commit>` to the log. (i.e. update and commit to log before flushing).
2.  When `T` is being committed, to make sure all log entries are written to disk. Then append `<T, commit>` to the log on the disk.

When recovering from crashes, the recovery manager scans the log from the begining of the log to the end, for every transaction with `begin` and `commit`, apply the redo operation.



## Exercise 2

Given the initial state A=B=C=0, and 3 transactions T1, T2 and T3

* T1: A=10, B=20
* T2: A=40, C=30, A=50
* T3: B=75

They are executed using *redo logging*, with the log content (on disk) above​

```
1.  <T1, BEGIN>​
2.  <T1, A, 10>​
3.  <T1, B, 20>​
4.  <T1, COMMIT>​
5.  <T2, BEGIN>​
6.  <T2, A, XXX>​
7.  <T2, C, 30>​
8.  <T2, A, 50>​
9.  <T2, COMMIT>​
10. <T3, BEGIN>​
11. <T3, B, XXX>​
```

* Question 2.1 - Fill in the `XXX` in the log.
* Question 2.2 - The system crashes. What are values of A,B,C on disk when the crash happened,
    1. If the log when the crash happened contains line 1-10​
    2. If the log when the crash happened contains line 1-3
* Question 2.3 - The system crashes and recovers. What can you say about values of A,B,C on disk after recovery, if​
    1. The log on disk contains line 1-11 when the crash happened.
    2. The log on disk contains line 1-5 when the crash happened.


## Recap non-quiescent checkpoint for redo logging

The main idea is to flush all committed transactions (the dirty pages) during the check point.

1. find all the active (and uncommitted) transactions ids, `T1`, ..., `Tn`.
2. insert a `<start_checkpoint T1,...,Tn>` entry to the log.
3. flush any dirty pages belonging to some committed transactions (committed before the start of the check point.) 
4. insert a `<end_checkpoint T1,...,Tn>`.


During the redo recovery phase, we start from the last completed checkpoint's `start_checkpoint` entry and search for transactions being committed  after this point, and redo these transactions. Note that some of these transactions (to be redone) could have been started before the starting of the check point (but still active during the check point).

## Exercise 3 

Given the initial state A=B=C=0, and 3 transactions T1, T2 and T3

* T1: A=10, B=20
* T2: A=40, C=30, A=50
* T3: B=75

They are executed using *redo logging*, with non-quiescent checkpoints. 

```
1.  <T1, BEGIN>​
2.  <T1, A, 10>​
3.  <T1, B, 20>​
4.  <T1, COMMIT>​
5.  <T2, BEGIN>​
6.  <START CHKPT (T2)>​
7.  <T2, A, 40>​
8.  <T2, C, 30>​
9.  <T2, A, 50>​
10. <END CHKP (T2)>​
11. <T2, COMMIT>​
12. <T3, BEGIN>​
13. <T3, B, 75>​
```
What can you say about values of A,B,C on disk when the crash happened, and:​
* The log on disk contains line 1-7.​
* The log on disk contains line 1-10.

## Exercise 4

```
1. <T1, BEGIN>​
2. <T1, A, 5>​
3. <T2, BEGIN>​
4. <T1, COMMIT>​
5. <T2, B, 10>​
6. <START CHKPT (T2)>​
7. <T2, C, 15>​
8. <T3, BEGIN>​
9. <T3, D, 20>​
10. <END CHKP (T2)>​
11. <T2, COMMIT>​
12. <T3, COMMIT>
```

Consider the above redo log with non-quiescent checkpoints. The system crashed and the log on disk contains line 1-12​

Describe the recovery steps.


## Exercise 5

```
1.  <T1, BEGIN>​
2.  <T1, A, 0>​
3.  <T1, B, 0>​
4.  <T1, COMMIT>​
5.  <T2, BEGIN>​
6.  <T2, A, 10>​
7.  <T2, C, 0>​
8.  <T2, A, 40>
```

Consider the recovery algorithm for undo Logging. Will it be correct if we scan the log forward instead of backward? Explain why.​

## Recap Conflict Serializability 

#### Serial Schedule

A schedule is *serial* iff there is no interleaving.


#### Serializable Schedule

A schedule is serializable if its effect is the same as a serial schedule after execution.

##### Operator Conflict


Two instructions $c_1$ and $c_2$ are conflict iff

* $c_1$ and $c_2$ belong to different transactions and 
* $(c_1 = R(A) \wedge c_2 = W(A))$ or $(c_1 = W(A) \wedge c_2 = R(A))$ or $(c_1 = W(A) \wedge c_2 = W(A))$ for some common object $A$ in the state.


#### Execution Order

Given two instructions, $c_i$ and $c_j$, $c_i \prec c_j$ means $c_i$ is executed before $c_j$ in a schedule $X$.


#### Conflict Equivalence

Given two schedules $X = c_1,...,c_n$ and $X' = c_1',...,c_n'$ are *conflict equivalent* iff

1. both schedules belong to the same set of transactions. 
2. for any pair of conflicting operators $(c_i, c_j)$ in $X$, such that $c_i \prec c_j$, we find $(c_k', c_l')$ in $X'$ such that $c_k' \prec c_l'$ and $c_i = c_k'$ and $c_j = c_l'$.

In other words, the second condition in the above definition says that all conflicting operators in $X$ have the same relative execution order (within the conflicting pair) in $X'$.

#### Conflict Serializable

Given a set of tasks $t_1,...,t_n$, a schedule $X$ is conflict serializable iff it is conflict equivalent to some schedule $X'$ of tasks $t_1,...,t_n$ such that $X'$ is serial.

#### Conflict Serializable Check Algorithm

Two possible approaches.

1. Manually shift non-conflicting operations until we get a serial schedule.
2. Use precedence graph

The precedence graph is generated from a schedule $X$ as follow.

1. For each transaction $t$, create a node $n_t$.
2. For each pair of transactions $t$ and $t'$, if there exists a conflicting pair of operators $t:c \prec t':c'$ in $X$, we draw an directed arc from $n_t$ to $n_{t'}$.

A schedule $X$ is conflict serialzable if its precendence graph is acyclic.

## Exercise 6 


|T1 | T2| T3|
|---|---|---|
|   |   |R(C)|
|R(A)| | |
|W(A)| | |
|R(B)| | |
| |W(B)| |
| |R(C)| |
| |W(C)| |
| |W(A)| |
| |W(D)| |

Given the schedule for T1,T2,T3 above, is this execution conflict serializable?​


## Exercise 7 



|T1 | T2| T3| T4|
|---|---|---|---|
|R(A)| | | |
| |R(A)| | | 
|R(B)| | | |
| |R(B)| | | 
| | | R(A)| |
| | | | R(B)|
|W(A)| | | |
| |W(B)| | |


Given the schedule for T1,T2,T3,T4 above, is this execution conflict serializable?​


## Recap 2PL 

DBMS generate conflict-serializable schedules using 2PL.

2PL, is governed by the following two rules. (First rule is the same as Strict 2PL, the second rule is different).

1. When a transaction needs to read an object $A$, it needs to acquire a shared lock $S(A)$; when it needs to write an object $A$, it needs to aquire an exclusive lock $X(A)$. A shared lock can be shared by multiple reader transactions. An exclusive lock cannot be shared.
2. A transaction releases the lock right after usage. A transaction cannot acquire new lock once it releases some lock.


## Exercise 8 


|T1|T2|
|---|---|
|R(A) | |
|W(A) | |
| |R(A) | 
|R(B)| |
|W(B)| |
| | R(B)|
| | W(B)|
| | W(A)|


Given the schedule for T1,T2 above. Each transaction commits immediately after the last operation. ​
* Is this schedule possible under 2PL? If yes, show where the locks are acquired and released