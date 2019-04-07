#!/usr/bin/env python2.7
# Udacity Log Analysis Project

# importing the PostgreSQL library
import psycopg2

# Requires that the view views_per_article from the README has been created
question_1 = "What are the most popular three articles of all time? (Most popular article listed first)"
q1_query = """select * from views_per_article limit 3"""

# Requires that the view views_per_article from the README has been created
question_2 = "Who are the most popular article authors of all time? (Most popular author listed first)"
q2_query = """select authors_articles.author, sum(vpa.views) as views
              from views_per_article as vpa, (select authors.name as author, articles.title
                                           from authors, articles
                                           where authors.id = articles.author) as authors_articles
              where authors_articles.title = vpa.title
              group by authors_articles.author
              order by views
              desc"""

# Requires that the views errors_per_day and total_req_per_day from the README have been created
question_3 = "On which days did more than 1% of requests lead to errors?"
q3_query = """select epd.day, round((epd.num_errors * 100.0 / trpd.num_requests), 2) as errors
              from errors_per_day as epd, total_req_per_day as trpd
              where epd.day = trpd.day
              and round((epd.num_errors * 100.0 / trpd.num_requests), 2) >= 1.0"""


class Log_Analysis:
    def db_results(self, query):
        # Connect to database
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
        # executing query and getting all results
        c.execute(query)
        db_res = c.fetchall()
        # closing connection
        db.close()
        return db_res

    def print_results(self, question, query, desc="views"):
        # get the resuls from the query
        results = self.db_results(query)
        # print out the question
        print(question)
        # go through the rows and format the results
        for row in results:
            print('\t' + str(row[0]) + ' - ' + str(row[1]) + ' ' + desc)
        print


if __name__ == '__main__':
    log_analysis = Log_Analysis()
    log_analysis.print_results(question_1, q1_query)
    log_analysis.print_results(question_2, q2_query)
    # description of results for q3 is errors not views
    log_analysis.print_results(question_3, q3_query, "errors")
