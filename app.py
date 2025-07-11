from flask import Flask, render_template, request, redirect, url_for, flash, session
import database

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
            return redirect(url_for('home'))
    return render_template('login.html')
    

# register route which uses POST to register a user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        success, message = database.register_user(username, password)
        flash(message)
        if success:
            return redirect(url_for('todo_list')) # if registration is successful then they are redirected to the todo page
        else:
            return redirect(url_for('home')) # else prompted to register again     
    return render_template('register.html')

# todo page route -  incomplete for now
@app.route('/todo')
def todo_list():
    if 'username' not in session:
        return redirect(url_for('home'))   
    tasks = database.get_user_tasks(session['username'])
    return render_template('todo.html', tasks=tasks) # getting the tasks from the get_user_tasks function and passing into todo.html


@app.route('/add_task', methods=['POST']) # retrieves the name, task, and due date and passed into the add_task function
def add_task():
    if 'username' not in session:
        return redirect(url_for('home'))
    else:
        name = session['username']
    task = request.form['task']
    due_date = request.form['due_date'] 
    database.add_task_to_table(name, task, due_date)
    return redirect(url_for('todo_list'))

@app.route('/remove_task', methods=['POST']) # retrieves the task and passed into the remove_task function
def remove_task():
    if 'username' not in session:
        return redirect(url_for('home'))
    else:
        name = session['username']
    task = request.form['task']
    database.remove_task_from_table(name, task)
    return redirect(url_for('todo_list'))

@app.route('/update_task', methods=['POST']) # retrieves the task and passed into the update_task function
def update_task():
    if 'username' not in session:
        return redirect(url_for('home'))
    else:
        name = session['username']

    task = request.form['task']
    due_date = request.form['due_date']
    done = request.form['done']
    database.update_task_in_table(name, task, due_date, done)
    return redirect(url_for('todo_list'))


# signout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__': # running the app with debugging on
    app.run(debug=True)
