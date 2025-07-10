from flask import Flask, render_template, request, redirect, url_for, flash, session
import database

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

database.init_db() # Initialize the database

# landing page which is user registration page
@app.route('/') 
def home():
    return render_template('register.html')

# user login route which uses POST method and then establishes a session for that user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        success, message = database.verify_user(username, password)

        if success:
            session['username'] = username
            return redirect(url_for('todo_list')) # if they are verified then they are redirected to the todo page
        else:
            flash(message)
    return render_template('login.html')
     
@app.route('/signin')
def signin():
    return render_template('login.html') # tbh I have no idea about this, might need to refactor
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not password.strip():
            flash('Password cannot be empty.')
            return render_template('register.html')

        if len(password) < 8 or not any(char.isdigit() for char in password):
            flash('Password must be at least 8 characters long and contain at least 1 digit.')
            return render_template('register.html')

        success, message = database.register_user(username, password)
        flash(message)
        if success:
            return redirect(url_for('home'))      
    return render_template('register.html')

# todo page route -  incomplete for now
@app.route('/todo')
def todo_list():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('todo.html')

# signout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__': # running the app with debugging on
    app.run(debug=True)
