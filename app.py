import sqlite3, os
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kip$iTh_bokopRo_o#ekuBOpHEsp*_roJopHokiquqe8&*iTIs=@S*U53&*ANLf='

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
def get_post(post_id): #checks posts id # in the database
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id): # allows you to change the details of the post in the database
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Question is required!')

        elif not content:
            flash('Answer is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
@app.route('/')
def index(): #shows all the posts from the database
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/create/', methods=('GET', 'POST'))
def create(): #allows you to add posts to the database
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Question is required!')
        elif not content:
            flash('Answer is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/about')
def about(): 
    return render_template('about.html')

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id): #allows you to delete the post and flashes and message to let you know that it is deleted
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/study')
def study(): #displays the database on the study page and allows you to study them
    conn = get_db_connection()
    cur = conn.execute('SELECT id, title AS question, content AS answer FROM posts')
    flashcards = cur.fetchall()
    conn.close()
    return render_template('study.html', flashcards=flashcards)

if __name__ == '__main__':
    app.run(debug=True)
