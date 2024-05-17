from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# User model example
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# User storage (for example purposes)
users = {
    'user1': User('1', 'user1', 'password1'),
    'user2': User('2', 'user2', 'password2')
}

def verify_user(username, password):
    if username in users and users[username].password == password:
        return users[username]
    return None

# Flask app and LoginManager setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

# Registration route (example)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists.')
        else:
            user_id = str(len(users) + 1)
            users[username] = User(user_id, username, password)
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

# Home route
@app.route('/home')
@login_required
def home():
    return f'Hello, {current_user.username}! Welcome to the Neighborhood Safety App.'

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)