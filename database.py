import sqlite3
import bcrypt

# Creating the database using some flask syntax
def init_db():
    try:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        # Creating the users table       
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
        
        if len(password) < 8 or not any(char.isdigit() for char in password):
            return False, "Password must be at least 8 characters long and contain at least 1 digit." # makes sure the password is strong
        
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
    try:
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (name,))
        user = cursor.fetchone()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user[0]):
                return True, "Login successful!"
            else:
                return False, "Invalid password, check your password and try again."
        else:
            return False, "Username not found, please register first."
    finally:
        conn.close()