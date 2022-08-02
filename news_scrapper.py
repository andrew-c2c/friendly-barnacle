from requests_html import HTMLSession
from datetime import date
import psycopg2
import string

session = HTMLSession()

url = 'https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNRGxqTjNjd0VnSmxiaWdBUAE?hl=en-US&gl=US&ceid=US%3Aen'
url_insurance = 'https://news.google.com/search?q=insurance%20when%3A1d&hl=en-US&gl=US&ceid=US%3Aen'

r = session.get(url_insurance)

r.html.render(sleep=1, scrolldown=2)

# print(r.html.html)

articles = r.html.find('article')

n = 1
newslist = {n : {'title': 'Null', 'link': 'Null', 'arc_date': 'Null'}}


for item in articles:
    
    try:
        newsitem = item.find('h3', first=True)
        title = newsitem.text.translate(str.maketrans('', '', string.punctuation))
        link = newsitem.absolute_links.pop()
        archive_date = date.today()
        newsarticle =  {'title': title, 'link': link, 'arc_date': archive_date}
        newslist[n] = (newsarticle)
        n+=1
    except:
        pass



print(newslist)

conn = psycopg2.connect(
        database = 'Project',
        user = 'postgres',
        password = 'owner',
        host = 'localhost',
        port = '5432')
cur = conn.cursor()

id = 1
for articles in newslist:
    if id <=101:
        title = newslist[id]['title']
        link = newslist[id]['link']
        archive_date = newslist[id]['arc_date']
        prim_id = f'{id}_{archive_date}'
        append_article = f"""INSERT INTO articles (title,link,archive_date,id,daily_rank)
                        VALUES ('{title}','{link}','{archive_date}','{prim_id}',{id});"""
        cur.execute(append_article)
        print(title,link,archive_date,prim_id)
        id+=1
        print(id)
    else:
        break

conn.commit()
conn.close()

print('done')

