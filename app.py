import sqlite3, os
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__) # gives flask the dunder name to let it know that this is the main application
app.config.from_object('config')

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # path to the current file 
DB_PATH = os.path.join(BASE_DIR, "database.db") # path to the database we want to use

#print(BASE_DIR)
#print(DB_PATH)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH) # sets up the connection to the database we want to use
    conn.row_factory = sqlite3.Row # we want our database to return as the row object, as opposed to tuple which it does atuomatically because having a tuple can cause problems down the line with indexes and readability
    return conn # finally return conn gives the connection to the database and makes sure that the objects are return as row objects and not tuples

def get_post(post_id): #checks posts id # in the database
    conn = get_db_connection() # we connect to the database and set that equal to conn
    post = conn.execute('SELECT * FROM posts WHERE id = ?', # we start we conn.execute which allows us to do the following statement. SELECT * selects all columns in the table, FROM posts tell us which table, and WHERE id = ? tells us which id we want to access, it also tells the code to search every row 
        (post_id,)).fetchone() # we use post_id here to replace the ? and find the post we want to fetch, fetchone simply finds the next available row 
    conn.close() # pretty simple, close the database connectoin
    if post is None: # if there is nothing in the database abort and return a 404 error
        abort(404)
    return post # we want to return the post if found

@app.route('/<int:id>/edit/', methods=('GET', 'POST')) # we set up the route and use get to render the initial edit.html and post to submit changes
def edit(id): # allows you to change the details of the post in the database
    post = get_post(id) # retrieve the post we want to edit with the corresponding id

    if request.method == 'POST': # client is requeseting to send a title and content 
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Question is required!') # if they don't have a title flash this

        elif not content:
            flash('Answer is required!') # if they don't have any content flash this

        else:
            conn = get_db_connection() # if they have both connect to the database and update the posts table by setting the title, content, and id to corresponding parameters
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit() # commit changes and close
            conn.close()
            return redirect(url_for('index')) # return the user back to the home page

    return render_template('edit.html', post=post) # have the results in the table appear on our index.html page

@app.route('/')
def index(): #shows all the posts from the database
    conn = get_db_connection() 
    posts = conn.execute('SELECT * FROM posts').fetchall() # grab all the flashcards and set them equal to posts
    conn.close() # disconnect from the database
    return render_template('index.html', posts=posts) # display the flashcards -- how does render_template work?


@app.route('/create/', methods=('GET', 'POST')) # establishes route and uses get to GET create.html and post will be used to POST our created flashcard to the database
def create(): # allows you to add posts to the database
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

if __name__ == '__main__': # since we intiliaze app = Flask(__name__) in the beginning, it will automactically be read as '__main__' and thus our app will run
    app.run(debug=True)
