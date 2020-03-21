from flask import Flask, render_template, request, redirect
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainers.db'
db = SQLAlchemy(app)  # link the app to the db


class TrainerPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    data_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):  # print out whenever we creat a new post
        return 'Blog post ' + str(self.id)


all_trainers = [
    {
        'name': 'ali',
        'type': 'tennis'
    },
    {
        'name': 'saud',
        'type': 'soccer'
    }
]


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/trainers', methods=['GET', 'POST'])
def trainers():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = TrainerPost(
            title=post_title, content=post_content, author='Saud the ONE')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/trainers')
    else:
        all_trainers = TrainerPost.query.order_by(TrainerPost.data_posted)
        return render_template("trainers.html", trainers=all_trainers)


# trying to read JSON file -- NOTE: the following function reads only one json obj, not an array !


def getJSON(filePathAndName):
    with open(filePathAndName, 'r') as fp:
        return json.load(fp)


if __name__ == "__main__":
    app.run(debug=True)
