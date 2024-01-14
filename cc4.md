# 50.043 - Cohort Class 4

## Learning Outcomes

By the end of this unit, you should be able to 


* compute the closure of a set of functional dependencies
* compute the canonical cover of a set of functional dependencies
* identify candidate keys from a relation
* apply lossless decomposition to a relation
* verify a relation is in 1NF/2NF/BCNF/3NF
* decompose a relation into 2NF/BCNF/3NF

## Recap Functional Dependencies


Given a FD $X_1,...,X_m \rightarrow Y_1, ..., Y_n$, we conclude that values of $X_1,...,X_m$ functionally determine the values of $Y_1, ..., Y_n$. 

Let $t$ be a tuple, we write $t[X]$ to refer to the value of attribute $X$ in tuple $t$.

Formally speaking, an FD $X_1,...,X_m \rightarrow Y_1, ..., Y_n$ holds in a relation $R$ iff 
$\forall t,t' \in R$ we have  $t[X_1] = t'[X_1] \wedge ... \wedge t[X_m] = t'[X_m]$ implies $t[Y_1] = t'[Y_1] \wedge ... \wedge t[Y_n] = t'[Y_n]$.


For example in the article-book-publisher example, for any tuples `t1` and `t2` in `Publish` table, `t1[book_id] = t2[book_id]`  implies `t1[date] = t2[date]`.


The closure of a set of FDs $F$ (which is $F^+$) is the greatest *superset* $F$ such that $F \equiv F^+$  and for any other $G$ that is $F \equiv G$, we have $G \subseteq F^+$.



To compute $F^+$ we need some rule-based rewriting system. 

#### Reflexivity rule

Let $Y$ and $X$ be sets of attributes, such that $Y \subseteq X$. Then $X \rightarrow Y$.

For instance, \{`date`\} $\subseteq$ \{ `book_id, date` \}, thus we have `book_id,date` $\rightarrow$ `date`


#### Augmentation rule

Let $Y$, $Z$ and $X$ be sets of attributes, such that $X \rightarrow Y$. Then $XZ \rightarrow YZ$. (Note $XZ$ is shorthand for $X\cup Z$). 

For instance, given `book_id` $\rightarrow$ `date`, we have `book_id,publisher_id` $\rightarrow$ `date,publisher`.

#### Transitivity rule

Let $Y$, $Z$ and $X$ be sets of attributes, such that $X \rightarrow Y$ and $Y \rightarrow Z$. Then $X \rightarrow Z$. 



#### Algorithm

1. At the start, let $F^+ = F$.
2. Find pick one of the three Axioms to apply, to generate a FD, let's say $X\rightarrow Y$. Let $F^+ = F^+ \cup \{X\rightarrow Y\}$.
3. repeat step 2 until $F^+$ does not change any more.


## Recap Canonical Cover

A **canonical cover** of $F$ is the smallest possible subset of $F$ such that its closure is $F^+$. 

The above statement is intuitive but not precise. To be precise, we need to define the standard form of FDs. 

### Standard form definition

An FD is in standard form iff its RHS is a single attribute.

It follows that for any set of FDs, we can convert it into an equivalent set with standard form FDs. (Hint: we know $X\rightarrow YZ$ implies $X \rightarrow Y$ and $X \rightarrow Z$ holds.)

### Formal definition
Let $F$ denote a set of FDs, we say $F_c$ is the canonical cover iff 
1. All FDs in $F_c$ are in standard form; and
2. $F_c^+ \subseteq F^+ \wedge F^+ \subseteq F_c^+$; and
3. $\neg \exists G \subset F_c$ such that  $G^+ \subseteq F^+ \wedge F^+ \subseteq G^+$

### Algorithm to compute $F_c$

1. Convert $F$ to standard form.
2. Minimize the lhs of each FD, by applying Reflexitivity, Augmentation and Transitivity.
3. Remove redundant FDs, by applying Reflexitivity, Augmentation and Transitivity.


### Application of canonical cover

Canonical cover is very useful. We can use it to reduce the number of constraints (which is expensive to verified). We leverage on Canonical cover to identify candidate key for a relation.


#### Some extra terminologies - different kinds of keys

In database, we call a set of attribute of a relation as a
* Super key if it functionally determines all other attributes 
* Candidate key if it is a minimal set of attributes that functionally determines all other attributes.
* Primary key if it is one of the candidate key. (We just fix one.)


## Exercise 1

Given the relation $R(A,B,C,D,E)$ with the following FDs:​

$$\{ C \rightarrow E, ​
BD\rightarrow AE​, 
A \rightarrow BC​ \}$$


Find a candidate key.



## Recap 1NF and 2NF and BCNF

### 1NF

A relation is in 1NF iff its schema is flat, (i.e. contains no sub-structure) and there is no repeating group (i.e. there is no repeating column).

### 2NF

A relation is in 2NF iff 

1. it is in 1NF and 
2. all non-key attributes are fully dependent on candidate key. 

In other words, the relation is at least 1NF and there should be no partial dependency.


### Boyd-Codd Normal Form (BCNF)



Given a relation $R$ with FDs $F$, $R$ is in BCNF iff for all non-trivial dependency $X \rightarrow Y \in F^+$, $X$ is a super key. 

An FD is *trivial* iff its lhs is a superset of the rhs.


#### Algorithm to decompose into BCNF

Given a relation $R$ and a set of FDs $F$. The algorithm of decomposing $R$ into BCNF is described as follows. 

1. Compute $F^+$
2. Let $Result = \{R\}$
3. While $R_i \in Result$ not in BCNF, do 
  3.1. Choose $X\rightarrow Y \in F^+$ such that $X$ and $Y$ are attribtues in $R_i$ but $X$ is not a super key of $R_i$.
  3.2. Decompose $R_i$ into $R_{i1}$ $R_{i2}$ with $X\rightarrow Y$.
  3.3. Update $Result = Result - \{ R_i\}  \cup \{ R_{i1}, R_{i2} \}$


#### A slightly more optimized algorithm

1. def $normalize(R)$
    1. Let $C = attr(R)$
    2. find an attribute set $X$ such that $X^+ \neq X$ and $X^+ \neq C$.
        1. if $X$ is not found, then $R$ is in BCNF
        2. else 
            1. decompose $R$ into $R_1(X^+)$ and $R_2(C-X^+ \cup X)$
            2. $normalize(R_1)$
            3. $normalize(R_2)$
2. $normalize(R)$


## Exercise 2

Given the relation $R(A,B,C,D,E)$ with the following FDs:​

$$
\{
A \rightarrow C​,
C \rightarrow DE,
B \rightarrow AE\}
$$

* is $R$ in 2NF?

* is $R$ in BCNF?


## Exercise 3


Given the relation $R(A,B,C,D,E,F,G)$ with the following FDs:​

$$
\{ E \rightarrow C,
G \rightarrow AD,
B \rightarrow E,
C \rightarrow BF \}
$$

Decompose R into BCNF


## Recap 3NF

### 3NF

Given a relation $R$ with FDs $F$, $R$ is in 3NF iff for all non-trivial dependency $X \rightarrow Y \in F^+$, 
1. $X$ is a super key or
2. $Y$ is part of a candidate key



#### Algorithm to compute 3NF 

With that difference in mind, we present the algorithm to compute 3NF as folows. 

1. Apply the BCNF algorithm to decompose $R$, let's say the result is a set of relations $R_1, ..., R_n$.
2. Let $F_1,...,F_n$ be the list of FDs preserved by $R_1, ..., R_n$.
3. Compute $(F_1 \cup ... \cup F_n)^{+}$. Let $\bar{F} = F - (F_1 \cup ... \cup F_n)^{+}$.
4. For each $X_1...,X_n\rightarrow Y \in \bar{F}$, create a new relation $R'(X_1,...,X_n,Y)$


## Exercise 4 ​


Decompose the relation $R$ given in exercise 3 into 3NF.