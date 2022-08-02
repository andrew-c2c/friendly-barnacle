import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule

from datetime import date, datetime
import time
import psycopg2

conn = psycopg2.connect(
        database = 'Project',
        user = 'postgres',
        password = 'owner',
        host = 'localhost',
        port = '5432')
cur = conn.cursor()

id = 1
search_key = f"""SELECT user_id, email, topic_1, topic_2, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8, topic_9, topic_10
                FROM users;"""
cur.execute(search_key)
user_topics = cur.fetchall()

for users in user_topics:
    user = users[0]
    user_email = users[1]
    user_topics = users[2:]

    topic_num = 0
    topic_articles = ''
    topic_articles_over = ''
    for topics in user_topics:
        if topics != None:
            archive_date = date.today()
            active_topic = topics[0:]
            topic_articles = f'The articles for {topics[0:]} are:\n'
            search_key = f"""SELECT title, link
                FROM articles
                WHERE lower(title) LIKE lower(\'%{active_topic}%\') AND archive_date = \'{archive_date}\';"""
            cur.execute(search_key)
            topic_results = cur.fetchall()

            for articles in topic_results:

                article_add = f'Title: {articles[0]}\nLink: {articles[1]}\n'
                topic_articles = f'{topic_articles}\n{article_add}'

            topic_articles_over = f'{topic_articles_over}\n{topic_articles}'
                
    print(user)
    print(topic_articles_over)

    subject = f'Topics for {user} on {archive_date}'
    body = topic_articles_over
    senders_email = 'teeterand@outlook.com'
    receivers_email = user_email
    password = 'PassOutl1'

    #CREATE MULTIPART MESSAGE AND SET HEADERS
    message = MIMEMultipart()
    message['From'] = senders_email
    message['To'] = receivers_email
    message['Subject'] = subject

    #ADD BODY TO MAIL
    message.attach(MIMEText(body,'plain'))
    text = message.as_string()


    #Log into server using secure conection
    with smtplib.SMTP("smtp.office365.com:587") as server:
        server.starttls()
        server.login(senders_email,password)
        server.sendmail(senders_email,receivers_email,text)
    
    print(f'Email sent to {user}')

cur_time = datetime.now()
print (f'done {cur_time}')




conn.commit()
conn.close()
