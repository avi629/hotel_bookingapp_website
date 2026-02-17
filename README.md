# HOTEL BOOKING PROJECT

A full-stack hotel booking web application built with Flask, HTML, CSS, and SQLite.

## 📁 Project Structure

```
HOTEL_BOOKING_PROJECT/
│
├── app.py                      # Flask backend application
├── requirement.txt             # Python dependencies
├── hotel_booking.db           # SQLite database
│
├── static/
│   ├── style.css              # Main stylesheet
│   └── images/                # Image folder (for future use)
│
└── templates/
    ├── index.html             # Home page
    ├── rooms.html             # Available rooms page
    ├── register.html          # Registration & Login page
    ├── booking.html           # Room booking page
    └── confirmation.html      # Booking confirmation page
```

## ✨ Features

✓ **User Registration & Login**
  - Secure password hashing (SHA-256)
  - Email validation
  - Session management

✓ **Room Management**
  - View available rooms
  - Room details with pricing
  - Amenities information

✓ **Booking System**
  - Date selection (check-in/check-out)
  - Guest count validation
  - Automatic price calculation
  - Instant booking confirmation

✓ **Secure Transactions**
  - Password encryption
  - SQL injection prevention
  - Session-based authentication

✓ **Responsive Design**
  - Mobile-friendly interface
  - Modern gradient UI
  - Clean and intuitive layout

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
cd HOTEL_BOOKING_PROJECT
pip install -r requirement.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Access the Website
Open your browser and go to:
```
http://localhost:5000
```

## 📊 Database Structure

### Users Table
- id (Primary Key)
- name
- email (Unique)
- phone
- password (SHA-256 hashed)
- created_at

### Rooms Table
- id (Primary Key)
- room_name
- room_type
- price
- capacity
- amenities
- available

### Bookings Table
- id (Primary Key)
- user_id (Foreign Key)
- room_id (Foreign Key)
- check_in
- check_out
- guests
- total_amount
- status
- created_at

## 🎯 How to Use

1. **Register/Login**
   - Go to Register/Login page
   - Create a new account or login with existing credentials

2. **Browse Rooms**
   - Click on "Rooms" in navigation
   - View all available rooms with details

3. **Book a Room**
   - Click "Book Now" on your preferred room
   - Select check-in and check-out dates
   - Enter number of guests
   - Confirm booking

4. **View Confirmation**
   - Get instant booking confirmation
   - View all booking details
   - Receive booking ID for reference

## 🏨 Sample Rooms

The database comes pre-loaded with 5 rooms:

1. **Deluxe Single Room** - ₹2,000/night (1 person)
2. **Standard Double Room** - ₹3,500/night (2 persons)
3. **Family Suite** - ₹6,000/night (4 persons)
4. **Executive Suite** - ₹8,000/night (3 persons)
5. **Premium King Room** - ₹5,000/night (2 persons)

## 🔒 Security Features

- Password hashing using SHA-256
- Parameterized SQL queries to prevent SQL injection
- Session-based authentication
- Login-protected booking pages
- Secure user data handling

## 🎨 Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3
- **Database**: SQLite3
- **Security**: Hashlib (SHA-256)

## 📱 Responsive Design

The website is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🛠️ Troubleshooting

**Issue: Port already in use**
```python
# In app.py, change the port number:
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Issue: Database not found**
- Make sure hotel_booking.db is in the project root directory
- The database is created automatically on first run

**Issue: Template not found**
- Verify all HTML files are in the templates/ folder
- Check file names match exactly

## 📝 Portfolio Description

"Full-stack hotel booking web application with user authentication, room search functionality, and secure booking system. Features include password encryption, SQLite database integration, responsive design, and real-time booking confirmation. Built with Flask (Python), HTML, CSS, and SQLite."

## 🎓 Learning Outcomes

- Flask web framework
- Database design and SQL
- User authentication
- Session management
- Security best practices
- Frontend-backend integration
- Responsive web design

## 📄 License

Created for educational and portfolio purposes.

## 👤 Author

Your Name

## 🌟 Future Enhancements

- Payment gateway integration
- Email confirmation system
- Admin dashboard
- Room availability calendar
- Booking cancellation feature
- User profile management
- Review and rating system

---

**Grand Hotel** - Your comfort is our priority! 🏨
