from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hotel_booking_secret_key_2025'

DATABASE = 'hotel_booking.db'


# ---------------- DATABASE INIT ---------------- #

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create rooms table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT,
        room_type TEXT,
        price INTEGER,
        available INTEGER DEFAULT 1
    )
    """)

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT
    )
    """)

    # Create bookings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        room_id INTEGER,
        check_in TEXT,
        check_out TEXT,
        guests INTEGER,
        total_amount INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(room_id) REFERENCES rooms(id)
    )
    """)

    # Insert default rooms if empty
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO rooms (room_name, room_type, price, available) VALUES ('Deluxe Room', 'Deluxe', 3000, 1)")
        cursor.execute("INSERT INTO rooms (room_name, room_type, price, available) VALUES ('Suite Room', 'Suite', 5000, 1)")
        cursor.execute("INSERT INTO rooms (room_name, room_type, price, available) VALUES ('Standard Room', 'Standard', 2000, 1)")

    conn.commit()
    conn.close()


init_db()


# ---------------- HELPER FUNCTIONS ---------------- #

def get_db():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rooms')
def rooms():
    conn = get_db()
    rooms_list = conn.execute('SELECT * FROM rooms WHERE available = 1').fetchall()
    conn.close()
    return render_template('rooms.html', rooms=rooms_list)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        hashed_password = hash_password(password)

        try:
            conn = get_db()
            conn.execute(
                'INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)',
                (name, email, phone, hashed_password)
            )
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('register'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hash_password(password)

    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE email = ? AND password = ?',
        (email, hashed_password)
    ).fetchone()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        flash('Login successful!', 'success')
        return redirect(url_for('rooms'))
    else:
        flash('Invalid credentials!', 'error')
        return redirect(url_for('register'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/booking/<int:room_id>', methods=['GET', 'POST'])
def booking(room_id):
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('register'))

    conn = get_db()
    room = conn.execute('SELECT * FROM rooms WHERE id = ?', (room_id,)).fetchone()
    conn.close()

    if not room:
        flash('Room not found!', 'error')
        return redirect(url_for('rooms'))

    if request.method == 'POST':
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        guests = int(request.form['guests'])

        date_in = datetime.strptime(check_in, '%Y-%m-%d')
        date_out = datetime.strptime(check_out, '%Y-%m-%d')
        nights = (date_out - date_in).days

        if nights <= 0:
            flash('Invalid dates!', 'error')
            return redirect(url_for('booking', room_id=room_id))

        total = room['price'] * nights

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO bookings (user_id, room_id, check_in, check_out, guests, total_amount) VALUES (?, ?, ?, ?, ?, ?)',
            (session['user_id'], room_id, check_in, check_out, guests, total)
        )
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return redirect(url_for('confirmation', booking_id=booking_id))

    return render_template('booking.html', room=room)


@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('register'))

    conn = get_db()
    booking = conn.execute('''
        SELECT b.*, r.room_name, r.room_type, r.price, u.name, u.email, u.phone
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        JOIN users u ON b.user_id = u.id
        WHERE b.id = ? AND b.user_id = ?
    ''', (booking_id, session['user_id'])).fetchone()
    conn.close()

    if not booking:
        flash('Booking not found!', 'error')
        return redirect(url_for('rooms'))

    return render_template('confirmation.html', booking=booking)


if __name__ == '__main__':
    app.run(debug=False)
