import sqlite3
import bcrypt

# Creating the database using some flask syntax
def init_db():
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL
        ) 
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        if conn:
            conn.close()

# Registering a user
def register_user(name, password):
    try:
        if not password.strip():
            return False, "Password cannot be empty." # check if password is empty
        
        conn = sqlite3.connect('todo.db')    
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (name,)) # Checks so that the username doesn't exist already and registers
        if cursor.fetchone():
            return False, "Username already exists, choose a new name."
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (name, hashed_password)) # stores the hashed password for the respective user
        conn.commit()
        conn.close()
        return True, "User registered successfully!"
    
    except sqlite3.Error as e:
        return False, f"Error registering user: {e}"
    except Exception as e:
        return False, f"General Error: {e}"

# Verifying a user exists and logging them in
def verify_user(name, password):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (name,))
    user = cursor.fetchone()
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user[0]):
            return True, "Login successful!"
    else:
        return False, "Invalid username or password!"
    conn.close()