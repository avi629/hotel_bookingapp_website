from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hotel_booking_secret_key_2025'

DATABASE = 'hotel_booking.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
            conn.execute('INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)',
                        (name, email, phone, hashed_password))
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
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                       (email, hashed_password)).fetchone()
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

        try:
            date_in = datetime.strptime(check_in, '%Y-%m-%d')
            date_out = datetime.strptime(check_out, '%Y-%m-%d')
            nights = (date_out - date_in).days

            if nights <= 0:
                flash('Invalid dates!', 'error')
                return redirect(url_for('booking', room_id=room_id))

            total = room['price'] * nights

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO bookings (user_id, room_id, check_in, check_out, guests, total_amount) VALUES (?, ?, ?, ?, ?, ?)',
                          (session['user_id'], room_id, check_in, check_out, guests, total))
            booking_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return redirect(url_for('confirmation', booking_id=booking_id))
        except Exception as e:
            flash(f'Booking error: {str(e)}', 'error')
            return redirect(url_for('booking', room_id=room_id))

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
    app.run(debug=True, host='0.0.0.0', port=5000)
