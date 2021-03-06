# Log Analysis Project

## Project Description
In this project, my task was to be able to answer the following three questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

To do this, I was to create an internal reporting tool that would gather the information from the `news` database.

This database contains three tables:  
* `articles`: stores article information such as the author and title.
* `authors`: stores information about the authors such as their name and their author id.
* `logs`: stores information on when articles were accessed such as date and request response.

## Set Up

1. Install the Linux-based virtual machine. This will require installing [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
  - To ensure that the same working environment is used, make sure to use [this vagrantfile](Vagrantfile)
  - After installing or if you simply need to bring the vm back online, use the commands `vagrant up` followed by `vagrant ssh`
2. Download the necessary data from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
  - Unzip the file and move the `newsdata.sql` file to the `vagrant` directory.
  - Go to the `vagrant` directory and load the data using the following command: `psql -d news -f newsdata.sql`
3. Create the necessary `Views`:
  - Required for question 1 and question 2.
  ```
  create view views_per_article as
  select a.title, count(l.id) as views
  from articles as a, log as l
  where CONCAT('/article/', a.slug) = l.path
  group by a.title
  order by views
  desc;
  ```
  - Required for question 3:
  ```
  create view errors_per_day as
  select Date(time) as day, count(status) as num_errors
  from log
  where status != '200 OK'
  group by day;
  ```

  ```
  create view total_req_per_day as
  select Date(time) as day, count(status) as num_requests
  from log
  group by day;
  ```
4. Use the `\q` command to quit `psql`
5. Run the script to get the answers to the questions using `python log_analysis.py`

## Description of `log_analysis.py`
- `question_1, question_2, question_3`: The three questions that need to be answered. Will be used to print out in the console when the script is run.
- `q1_query, q2_query, q3_query`: The `SQL` queries that will retrieve the necessary data from the `news` database so that we may answer the questions.
- `db_results()`: Function in `Log_Analysis` class that will connect to the database, execute the given query, and will return the results from the query.
- `print_results`: Function in `Log_Analysis` class that will print out the question being answered and the formatted results retrieved from the database.
- `__main__`: Main method that will call the `print_results` function from the `Log_Analysis` class to print the results to each question.

## Description of Views
- `views_per_article`: This view is a table containing the number of views that each article has received.
- `errors_per_day`: This view is a table containing the number of errors per day when loading a page.
- `total_req_per_day`: This view is a table containing the total number of requests made per day.

## Author
Adilene Pulgarin
