
import qrcode
import os
from flask import Flask, app, render_template, redirect, session, Blueprint, request, url_for, flash
from extentions import mail
from flask_mail import Message
from db import db_connection
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')


@views_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""select r.start as start,
                    r.destination as destination,
                    s.departure_time as departure_time,
                    b.bus_number as bus_number,
                    bk.seat_number as seat_number,
                    bk.status as status
                    from bookings bk
                    join schedules s on bk.schedule_id = s.id
                    join routes r on s.route_id = r.id
                    join buses b on s.bus_id = b.id
                    where bk.user_id = %s
                    order by s.departure_time;""" , (session["user_id"],))
    upcoming_bookings = cursor.fetchall()
    db.close()

    return render_template('dashboard.html', name = session['name'], upcoming_bookings = upcoming_bookings)



@views_bp.route('/bookings')
def bookings():
    if 'user_id' not in session:
        return redirect('/login')
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""SELECT bk.id AS id,
                b.bus_number AS bus_number,
                r.start AS start, r.destination AS destination,
                s.departure_time AS departure_time,
                s.arriving_time AS arriving_time, s.price AS price
            FROM bookings bk JOIN schedules s ON bk.schedule_id = s.id
            JOIN routes r ON s.route_id = r.id
            JOIN buses b ON s.bus_id = b.id
            WHERE bk.user_id = %s
            ORDER BY s.departure_time;
            """, (session['user_id'],))
    bookings = cursor.fetchall()
    db.close()

    return render_template('bookings.html', bookings=bookings)

@views_bp.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        schedule_id = request.form['schedule_id']
        seat_number = request.form['seat_number'].strip().upper()
        db = db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT s.id, b.seats_number FROM schedules s JOIN buses b ON s.bus_id = b.id WHERE s.id = %s", (schedule_id,))
        schedule = cursor.fetchone()
        if not schedule:
            db.close()
            flash("Invalid schedule or schedule has already departed.", "danger")
            return redirect(url_for('views.add_booking', schedule_id=schedule_id))
        
        valid_seats = generate_seat_labels(schedule['seats_number'])
        if seat_number not in valid_seats:
            db.close()
            flash("invalid seat selected!", "danger")
            return redirect(url_for('views.add_booking', schedule_id=schedule_id))

        cursor.execute("SELECT id FROM bookings WHERE schedule_id = %s AND seat_number = %s", (schedule_id, seat_number))
        existing_booking = cursor.fetchone()

        if existing_booking:
            db.close()
            flash("Seat already booked. Please choose another seat.", "danger")
            return redirect(url_for('views.add_booking', schedule_id=schedule_id))
        
        cursor.execute("INSERT INTO bookings (user_id, schedule_id, seat_number, status, booking_time) VALUES (%s, %s, %s,%s, NOW())", (session['user_id'], schedule_id, seat_number, 'booked'))
        db.commit()
        booking_id = cursor.lastrowid

        qr_data = f"Booking ID: {booking_id}\nUser: {session['name']}\nSchedule ID: {schedule_id}\nSeat: {seat_number}"
        qr_path = f"static/qr_codes/booking_{booking_id}.png"
        qr = qrcode.QRCode()
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image()
        if not os.path.exists('static/qr_codes'):
            os.mkdir('static/qr_codes')
        img.save(qr_path)

        cursor.execute("""
            SELECT u.name, u.email,
                r.start, r.destination,
                s.departure_time, s.arriving_time,
                b.bus_number, bk.seat_number, s.price
            FROM bookings bk
            JOIN users u ON bk.user_id = u.id
            JOIN schedules s ON bk.schedule_id = s.id
            JOIN routes r ON s.route_id = r.id
            JOIN buses b ON s.bus_id = b.id
            WHERE bk.id = %s
        """, (booking_id,))
        data = cursor.fetchone()

        msg = Message(
            subject="Booking Confirmation",
            recipients=[data['email']]
        )

        msg.body = f"""
        Hello {data['name']},

        Your booking has been confirmed.

        Route: {data['start']} → {data['destination']}
        Departure: {data['departure_time']}
        Arrival: {data['arriving_time']}
        Bus: {data['bus_number']}
        Seat: {data['seat_number']}
        Price: RM{data['price']}

        Your QR ticket is attached.

        Thank you.
        """

        # attach QR file
        with open(qr_path, 'rb') as f:
            msg.attach(
                filename=f"booking_{booking_id}.png",
                content_type="image/png",
                data=f.read()
            )

        try:
            mail.send(msg)
            flash("email sent successfully.", "success")
        except Exception as e:
            print("Email failed:", e)

        db.close()

        flash("Booking created successfully.", "success")
        return redirect(url_for('views.ticket', booking_id=booking_id))
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
            SELECT 
                b.bus_number AS bus_number,
                s.id AS schedule_id,
                r.id AS route_id,
                r.start AS start,
                r.destination AS destination,
                s.departure_time AS departure_time,
                s.arriving_time AS arriving_time,
                s.price AS price
            FROM routes r
            JOIN schedules s ON s.route_id = r.id
            JOIN buses b ON s.bus_id = b.id
            ORDER BY s.departure_time ASC
        """)
    schedules = cursor.fetchall()

    selected_schedule_id = request.args.get('schedule_id', type=int)

    seat_labels = []
    reserved_seats = []
    selected_schedule = None

    if selected_schedule_id:
        cursor.execute("""
            SELECT s.id AS schedule_id,
                   b.bus_number AS bus_number,
                   b.seats_number AS seats_number,
                   r.start AS start,
                   r.destination AS destination,
                   s.departure_time AS departure_time,
                   s.arriving_time AS arriving_time,
                   s.price AS price
            FROM schedules s
            JOIN buses b ON s.bus_id = b.id
            JOIN routes r ON s.route_id = r.id
            WHERE s.id = %s
        """, (selected_schedule_id,))
        selected_schedule = cursor.fetchone()

        if selected_schedule:
            seat_labels = generate_seat_labels(selected_schedule['seats_number'])

            cursor.execute("""
                SELECT seat_number
                FROM bookings
                WHERE schedule_id = %s
            """, (selected_schedule_id,))
            reserved_rows = cursor.fetchall()
            reserved_seats = [row['seat_number'] for row in reserved_rows]

    db.close()

    return render_template(
        'add_booking.html',
        schedules=schedules,
        selected_schedule_id=selected_schedule_id,
        selected_schedule=selected_schedule,
        seat_labels=seat_labels,
        reserved_seats=reserved_seats
    )

@views_bp.route('/delete_booking/<int:booking_id>')
def delete_booking(booking_id):
    if 'user_id' not in session:
        return redirect('/login')
    db = db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = %s AND user_id = %s", (booking_id, session['user_id']))
    db.commit()
    return redirect(url_for('views.bookings'))

@views_bp.route('/ticket/<int:booking_id>')
def ticket(booking_id):
    if 'user_id' not in session:
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.start, r.destination,
               s.departure_time,
               b.bus_number,
               bk.seat_number
        FROM bookings bk
        JOIN schedules s ON bk.schedule_id = s.id
        JOIN routes r ON s.route_id = r.id
        JOIN buses b ON s.bus_id = b.id
        WHERE bk.id = %s AND bk.user_id = %s
    """, (booking_id, session['user_id']))

    booking = cursor.fetchone()
    db.close()

    if not booking:
        return "Booking not found"

    return render_template('ticket.html', booking=booking, booking_id=booking_id)

@views_bp.route('/route_map/<int:booking_id>')
def route_map(booking_id):
    if 'user_id' not in session:
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT bk.id,
               r.start,
               r.destination
        FROM bookings bk
        JOIN schedules s ON bk.schedule_id = s.id
        JOIN routes r ON s.route_id = r.id
        WHERE bk.id = %s AND bk.user_id = %s
    """, (booking_id, session['user_id']))

    booking = cursor.fetchone()
    db.close()

    if not booking:
        return "Booking not found"

    location_addresses = {
        "APU": "Asia Pacific University of Technology & Innovation, Kuala Lumpur, Malaysia",
        "KL Sentral": "KL Sentral, Kuala Lumpur, Malaysia",
        "KLCC": "Petronas Twin Towers, Kuala Lumpur, Malaysia",
        "Sunway Pyramid": "Sunway Pyramid, Selangor, Malaysia",
        "Kuala Lumpur": "Kuala Lumpur, Malaysia",
        "Ipoh": "Ipoh, Perak, Malaysia"
    }

    start_address = location_addresses.get(booking['start'])
    destination_address = location_addresses.get(booking['destination'])

    if not start_address or not destination_address:
        return "Map addresses not available for this route"

    return render_template(
        'route_map.html',
        booking=booking,
        start_address=start_address,
        destination_address=destination_address,
        google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY")
    )

def generate_seat_labels(total_seats, seats_per_row=4):
    seats = []
    for i in range(total_seats):
        row_letter = chr(ord('A') + (i // seats_per_row))
        seat_number = (i % seats_per_row) + 1
        seats.append(f"{row_letter}{seat_number}")
    return seats