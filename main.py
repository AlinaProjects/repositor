from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = 'your_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

DATABASE = "sqlite.db"


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    if user is not None:
        return User(user[0], user[1], user[2])
    return None


@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(''' 
        SELECT post.id, post.title, post.content, post.author_id, user.username, 
               COUNT(like.id) AS likes 
        FROM post 
        JOIN user ON post.author_id = user.id 
        LEFT JOIN like ON post.id = like.post_id 
        GROUP BY post.id 
    ''')
    result = cursor.fetchall()
    posts = []
    liked_posts = []

    if current_user.is_authenticated:
        likes_result = db.execute('SELECT post_id FROM like WHERE user_id = ?', (current_user.id,)).fetchall()
        liked_posts = [like[0] for like in likes_result]

    for post in reversed(result):
        posts.append({
            'id': post[0],
            'title': post[1],
            'content': post[2],
            'author_id': post[3],
            'username': post[4],
            'likes': post[5],
            'liked': post[0] in liked_posts
        })

    return render_template('blog.html', posts=posts)


@app.route('/add/', methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db = get_db()
        db.execute('INSERT INTO post (title, content, author_id) VALUES (?, ?, ?)',
                   (title, content, current_user.id))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add_post.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    result = db.execute(''' 
        SELECT post.id, post.title, post.content, post.author_id, user.username, 
               (SELECT COUNT(*) FROM like WHERE like.post_id = post.id) AS likes 
        FROM post 
        JOIN user ON post.author_id = user.id 
        WHERE post.id = ? 
    ''', (post_id,)).fetchone()

    if not result:
        return 'Пост не найден', 404

    liked = False
    if current_user.is_authenticated:
        liked = user_is_liking(current_user.id, post_id)

    post_dict = {
        'id': result[0],
        'title': result[1],
        'content': result[2],
        'author_id': result[3],
        'username': result[4],
        'likes': result[5],
        'liked': liked
    }
    return render_template('index.html', post=post_dict)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute('INSERT INTO user (username, password_hash) VALUES (?, ?)',
                       (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', message='Username already exists!')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user:
            user_obj = User(user[0], user[1], user[2])
            if user_obj.check_password(password):
                login_user(user_obj)
                return redirect(url_for('index'))
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM post WHERE id = ?', (post_id,)).fetchone()
    if post and post[3] == current_user.id:
        db.execute('DELETE FROM post WHERE id = ?', (post_id,))
        db.commit()
    return redirect(url_for('index'))


def user_is_liking(user_id, post_id):
    db = get_db()
    like = db.execute('SELECT * FROM like WHERE user_id = ? AND post_id = ?', (user_id, post_id)).fetchone()
    return bool(like)


@app.route('/like/<int:post_id>')
@login_required
def like_post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM post WHERE id = ?', (post_id,)).fetchone()
    if post:
        if user_is_liking(current_user.id, post_id):
            db.execute('DELETE FROM like WHERE user_id = ? AND post_id = ?', (current_user.id, post_id))
            print('You unliked this post.')
        else:
            db.execute('INSERT INTO like (user_id, post_id) VALUES (?, ?)', (current_user.id, post_id))
            print('You liked this post!')
        db.commit()
        return redirect(url_for('index'))
    return 'Post not found', 404


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM post WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    if post is None:
        return "Пост не найден", 404
    if post[3] != current_user.id:
        return "Нет доступа", 403
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute('UPDATE post SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
        db.commit()
        return redirect(url_for('post', post_id=post_id))
    post_dict = {'id': post[0], 'title': post[1], 'content': post[2]}
    return render_template('edit_post.html', post=post_dict)


if __name__ == "__main__":
    app.run(debug=True)