from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import *
import sqlite3
from sqlalchemy import create_engine

# conn = sqlite3.connect('books-coll.db')
# c = conn.cursor()
# c.execute("""CREATE TABLE books
#             (id INTEGER PRIMARY KEY ASC,
#             name string(200) NOT NULL)
#         """)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
db = SQLAlchemy(app)
#db.create_all()
#db.session.commit()

# metadata = MetaData()
# book = Table(
#     "book", metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String),
#     Column('author', String),
#     Column('datatime', default=datetime.utcnow)
# )
# book.create(bind=engine)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    note = db.Column(db.String(400))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __int__(self, author, name, publisher, note):
        self.name = name
        self.author = author
        self.publisher = publisher
        self.note=note


    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_author = request.form['author']
        task_name = request.form['name']
        task_publisher = request.form['publisher']
        task_note = request.form['note']

        new_task = Todo(author=task_author, name=task_name, publisher=task_publisher, note=task_note)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        #task.content = request.form['content']
        task.author = request.form['author']
        task.name = request.form['name']
        task.publisher = request.form['publisher']
        task.note = request.form['note']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)
    




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
