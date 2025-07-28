from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)


def init_db():
    with sqlite3.connect('students.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                gender TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()


init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        with sqlite3.connect('students.db') as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO students (first_name, last_name, email, phone, gender, password)
                VALUES (?, ?, ?, ?, ?, ?)""",
                      (first_name, last_name, email, phone, gender, hashed_password))
            conn.commit()
        return redirect(url_for('view_students'))
    return render_template('add_student.html')


@app.route('/students')
def view_students():
    with sqlite3.connect('students.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        students = c.fetchall()
    return render_template('view_students.html', students=students)


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    with sqlite3.connect('students.db') as conn:
        c = conn.cursor()
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            gender = request.form['gender']

            c.execute("""
                UPDATE students
                SET first_name=?, last_name=?, email=?, phone=?, gender=?
                WHERE id=?""",
                      (first_name, last_name, email, phone, gender, id))
            conn.commit()
            return redirect(url_for('view_students'))
        else:
            c.execute("SELECT * FROM students WHERE id=?", (id,))
            student = c.fetchone()
    return render_template('edit_student.html', student=student)


@app.route('/delete_student/<int:id>')
def delete_student(id):
    with sqlite3.connect('students.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('view_students'))


if __name__ == '__main__':
    app.run(debug=True)
