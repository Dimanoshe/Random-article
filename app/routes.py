from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from pip._vendor import requests
import re

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

    topic_list = []
    page = 'https://en.wikipedia.org/wiki/Main_Page'
    r = requests.get(page)
    soup = BeautifulSoup(r.text, 'html.parser')
    for i in soup.find(id="mp-portals"):
        if i.find('a') != -1:
            topic = i.find('a')
            topic = topic['title']
            topic_list.append(topic[7:])
    topic_list.pop()
    print(topic_list)

    return render_template("main.html", index=index, topic_list=topic_list)


@app.route('/result')
def result():
    text = Article.query.all()
    return render_template("result.html", index=text[-1])


if __name__ == '__main__':
    app.run(debug=True)
