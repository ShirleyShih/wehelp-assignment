Task 2
---
* Create a new database named website.</br>
![](images/2-1.png)

* Create a new table named member, in the website database, designed as below:</br>
![](images/2-2.png)

Task 3
---
* INSERT a new row to the member table where name, username be set to test. INSERT additional 4 rows with arbitrary data.</br>
![](images/3-1.png)

* SELECT all rows from the member table.</br>
![](images/3-2.png)

* SELECT all rows from the member table, in descending order of time.</br>
![](images/3-3.png)

* SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.</br>
![](images/3-4.png)

* SELECT rows where username equals to test.</br>
![](images/3-5.png)

* SELECT rows where name includes the es keyword.</br>
![](images/3-6.png)

* SELECT rows where both username and password equal to test.
![](images/3-7.png)

* UPDATE data in name column to test2 where username equals to test.
![](images/3-8.png)

Task 4
---
* SELECT how many rows from the member table.
![](images/4-1.png)
* SELECT the sum of follower_count of all the rows from the member table.
![](images/4-2.png)
* SELECT the average of follower_count of all the rows from the member table.
![](images/4-3.png)
* SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
![](images/4-4.png)

Task 5
---
* Create a new table named message, in the website database. designed as below:
![](images/5-1.png)

* SELECT all messages, including sender names. We have to JOIN the member table to get that.
![](images/5-2-1.png)
![](images/5-2-2.png)

* SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
![](images/5-3.png)

* Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
![](images/5-4.png)

* Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
![](images/5-5.png)