# Bus Ticketing System

A full-stack bus booking system built with Flask and MySQL. The system allows users to browse schedules, select seats, and receive QR-based tickets, while admins manage routes, buses, and schedules.

---

## Features

- User authentication (login/register) with role-based access (admin / passenger)  
- Browse available routes and upcoming schedules  
- Interactive seat selection with real-time availability  
- Booking validation to prevent duplicate seat reservations  
- QR code generation for each ticket  
- Email confirmation with QR ticket attachment  
- Route visualization using Google Maps  

---

## Tech Stack

- **Backend:** Python (Flask)  
- **Database:** MySQL  
- **Frontend:** HTML, CSS, Bootstrap, Jinja2  
- **Integrations:** Google Maps API, Flask-Mail  

---

## How It Works

- Users select a route and schedule  
- Seats are generated dynamically based on bus capacity (e.g. A1, A2, B1...)  
- Reserved seats are blocked from selection  
- Once booked:
  - Data is stored in the database  
  - A QR ticket is generated  
  - A confirmation email is sent  

---

## Project Structure


project/
│
├── app.py
├── db.py
├── views.py
├── auth.py
├── admin.py
├── templates/
├── static/
└── extensions.py


---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/bus-ticketing-system.git
cd bus-ticketing-system
2. Install dependencies
pip install -r requirements.txt
3. Configure environment variables

Create a .env file:

SECRET_KEY=your_secret_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_email_password
GOOGLE_MAPS_API_KEY=your_api_key

4. Run the application
python app.py
Notes
Make sure MySQL is running and the database schema is created
Email functionality requires valid SMTP credentials
Google Maps API must have Maps JavaScript and Directions APIs enabled
Future Improvements
Online payment integration
Enhanced seat layout visualization
Booking history and ticket downloads
Admin dashboard analytics