from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from pip._vendor import requests
from random import choice

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Artikle %r>" % self.id


@app.route('/', methods=['POST', 'GET'])
def main():
    index = "No topic selected"
    if request.method == "POST":
        index = request.form['index']

        text = Article(text=index)
        db.session.add(text)
        db.session.commit()
    #print(type(index))
    topic_list = []
    page_topic = 'https://en.wikipedia.org/wiki/Main_Page'
    r_topic = requests.get(page_topic)
    soup = BeautifulSoup(r_topic.text, 'html.parser')
    for i in soup.find(id="mp-portals"):
        if i.find('a') != -1:
            topic = i.find('a')
            topic = topic['title']
            topic_list.append(topic[7:])
    topic_list.pop()

    article_list = []
    page_article = 'https://en.wikipedia.org/wiki/Portal:%s/Recognized_content' % index
    print(page_article)
    r_article = requests.get(page_article)
    soup = BeautifulSoup(r_article.text, 'html.parser')
    cont = soup.find_all("div", {"class": "div-col"})
    for i in cont[0].find_all('a'):
        name_artlicle = i['title']
        article_list.append(name_artlicle)
    #print(article_list)
    article = choice(article_list)
    #print(article)
    article = article.split(" ")
    article = '_'.join(article)
    #print(article)


    article_page = 'https://en.wikipedia.org/wiki/%s' % article
    #print(article_page)
    r_article_text = requests.get(article_page)
    soup = BeautifulSoup(r_article_text.text, 'html.parser')
    cont = []
    for link in soup.find_all("div", {"class": "mw-parser-output"}, 'p'):
        for i in link.find_all('p'):
            i = i.get_text().replace('\n', '')
            for del_num in range(100):
                i = i.replace('[{}]'.format(del_num), '')
            if i != '' and i[-1] != '.':
                i = i[:-1] + '.'
            cont.append(i)
    cont = '$$$'.join(cont)
    text = Article(text=cont)
    db.session.add(text)
    db.session.commit()

    return render_template("main.html", index=index, topic_list=topic_list)


@app.route('/result')
def result():

    text = Article.query.all()[-1]
    text = str(text.text).split('$$$')
    #print(text)

    return render_template("result.html", index=text)


if __name__ == '__main__':
    app.run(debug=True)
