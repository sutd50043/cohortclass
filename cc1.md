# 50.043 Cohort class 1

## Learning Outcomes

By this end of this cohort class you should be able to 

1. Design an ER model based on the user requirement


## Recap Data model pipeline

![](../lecture/images/overview-of-data-modelling.png)

ER model is an instance of conceptual modelling. It focuses on describing what data are required by the application.

An ER Diagram may consists of some of the following

1. Entity set. An entity set captures a set of objects or items to be stored. It is represented as a rectangular box with the entity name inside. 
2. Attribute. An attribute describe a property of an entity. An attribute is represented as an oval shape with the attribute name inside. Attribute serves as (part of) the primary key of the entity will be underlined.
3. Relationship. A relationship defines the relationship between entities. It is represented as a diamond shape with the relationship name inside. Relationships are often annotated with cardinality constraints. 

![](../lecture/images/student_class_er.png)

In the enrolled in relationship above, we find that a student may enroll in many classes and a class may have many enrolled students.


## Exercise 1

A new recording studio needs to maintain the following information:​

* Each musician that records at Studify has an SSN, a name, and date of birth. Poorly paid musicians often live together at the same house which also has a phone.​

* Each instrument used for recording at Studify has a unique identification number, a name (e.g., guitar, synthesizer, flute) and a musical key (e.g., C, B-flat, E-flat).​

* Each album recorded has a unique identification number, a title, a copyright date, a format (e.g., CD or MC).​

* Each song recorded has a unique identification number, a title, an author.​

* Each musician may play several instruments, and a given instrument may be played by several musicians.​

* Each album has a number of songs on it, but no song may appear on more than one album.​

* Each song is performed by multiple musicians, and a musician may perform a number of songs.​

* Each album has exactly one musician who acts as its producer. A musician may produce several albums.​


## Exercise 2

You want to manage student clubs at the university. But you need to adhere to the following constraints:​

* Each student has a unique student identification number, a name, and pillar.​

* Each club has a unique name​

* Every year, students can join a club. One student may belong to different clubs in different year, but may belong to at most one club in any given year.​

* Each club may travel to different cities. Every city has a name, and belongs to a country​

* Each club may travel to different cities in different year, but only to one city in any given year.

