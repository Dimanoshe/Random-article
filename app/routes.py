from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    index = "No topic selected"
    if request.method == "POST":
        index = request.form['index']
    return render_template("main.html", index=index)



@app.route('/result')
def result():
    return render_template("result.html")


if __name__ == '__main__':
    app.run(debug=True)
