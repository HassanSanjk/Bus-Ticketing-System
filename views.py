from flask import Flask, app, render_template, redirect, session, Blueprint, request, url_for, flash
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
                    where bk.user_id = %s and s.departure_time > NOW()
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
    cursor.execute("""select b.bus_number as bus_number, s.id as schedule_id,
                    r.id as route_id, r.start as start, r.destination as destination,
                    s.id as schedule_id, s.departure_time as departure_time,
                    s.arriving_time as arriving_time,
                    s.price as price from routes r 
                    join schedules s on s.route_id = r.id
                    join buses b on s.bus_id = b.id
                    where s.departure_time > NOW();""")
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
        cursor = db.cursor()
        cursor.execute("SELECT s.id FROM schedules s WHERE s.id = %s AND s.departure_time > NOW()", (schedule_id,))
        schedule = cursor.fetchone()
        if not schedule:
            db.close()
            flash("Invalid schedule or schedule has already departed.", "danger")
            return redirect(url_for('views.add_booking'))
        
        valid_seats = generate_seat_labels(schedule['seats_number'])
        if seat_number not in valid_seats:
            db.close()
            flash("invalid seat selected!", "danger")
            return redirect(url_for('views.add_booking'), schedule_id=schedule_id)

        cursor.execute("SELECT id FROM bookings WHERE schedule_id = %s AND seat_number = %s", (schedule_id, seat_number))
        existing_booking = cursor.fetchone()

        if existing_booking:
            db.close()
            flash("Seat already booked. Please choose another seat.", "danger")
            return redirect(url_for('views.add_booking'))
        
        cursor.execute("INSERT INTO bookings (user_id, schedule_id, seat_number, status, booking_time) VALUES (%s, %s, %s,%s, NOW())", (session['user_id'], schedule_id, seat_number, 'booked'))
        db.commit()
        db.close()

        flash("Booking created successfully.", "success")
        return redirect(url_for('views.bookings'))
    
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""select b.bus_number as bus_number, s.id as schedule_id,
                    r.id as route_id, r.start as start, r.destination as destination,
                    s.id as schedule_id, s.departure_time as departure_time,
                    s.arriving_time as arriving_time,
                    s.price as price from routes r 
                    join schedules s on s.route_id = r.id
                    join buses b on s.bus_id = b.id
                    where s.departure_time > NOW()
                    ORDER BY s.departure_time ASC;
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
            WHERE s.id = %s AND s.departure_time > NOW()
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

def generate_seat_labels(total_seats, seats_per_row=4):
    seats = []
    for i in range(total_seats):
        row_letter = chr(ord('A') + (i // seats_per_row))
        seat_number = (i % seats_per_row) + 1
        seats.append(f"{row_letter}{seat_number}")
    return seats