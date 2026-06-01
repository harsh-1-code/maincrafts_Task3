from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "secure-secret-key"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# TASK 2: AUTHENTICATION ROUTES
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        db = get_db()
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        db.commit()
        return redirect('/login')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", 
            (username,)
        ).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            return redirect('/dashboard')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# ==========================================
# TASK 3: CRUD ROUTES (STUDENT MANAGEMENT)
# ==========================================

# 1. CREATE: Add a new student
@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect('/login')
        
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        
        db = get_db()
        db.execute(
            "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
            (name, email, course)
        )
        db.commit()
        return redirect('/students')
        
    return render_template('add_student.html')

# 2. READ: View all students
@app.route('/students')
def students():
    if 'user' not in session:
        return redirect('/login')
        
    db = get_db()
    data = db.execute("SELECT * FROM students").fetchall()
    return render_template('students.html', students=data)

# 3. UPDATE: Edit a student's details
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user' not in session:
        return redirect('/login')
        
    db = get_db()
    student = db.execute(
        "SELECT * FROM students WHERE id = ?", (id,)
    ).fetchone()
    
    if request.method == 'POST':
        db.execute(
            "UPDATE students SET name=?, email=?, course=? WHERE id=?",
            (
                request.form['name'],
                request.form['email'],
                request.form['course'],
                id
            )
        )
        db.commit()
        return redirect('/students')
        
    return render_template('edit_student.html', student=student)

# 4. DELETE: Remove a student
@app.route('/delete/<int:id>')
def delete_student(id):
    if 'user' not in session:
        return redirect('/login')
        
    db = get_db()
    db.execute("DELETE FROM students WHERE id=?", (id,))
    db.commit()
    return redirect('/students')

@app.route('/')
def home():
    return redirect('/register')


if __name__ == '__main__':
    app.run(debug=True)