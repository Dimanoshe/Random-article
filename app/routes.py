from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

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
        print(text)
        db.session.add(text)
        db.session.commit()

    return render_template("main.html", index=index)


@app.route('/result')
def result():
    text = Article.query.all()
    return render_template("result.html", index=text[-1])


if __name__ == '__main__':
    app.run(debug=True)
