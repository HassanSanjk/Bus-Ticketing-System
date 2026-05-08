from flask import render_template, request, redirect, session, Blueprint, url_for, flash
from db import db_connection

admin_bp = Blueprint('admin', __name__)


def admin_required():
    return 'user_id' in session and session.get('role') == 'admin'


@admin_bp.route('/settings')
def settings():
    if not admin_required():
        return redirect('/login')

    return render_template('admin.html', name=session['name'])


@admin_bp.route('/routes')
def routes():
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, start, destination, distance_km, travel_time
        FROM routes
        ORDER BY id DESC
    """)
    routes = cursor.fetchall()

    db.close()

    return render_template('routes.html', routes=routes)


@admin_bp.route('/add_route', methods=['GET', 'POST'])
def add_route():
    if not admin_required():
        return redirect('/login')

    if request.method == 'POST':
        start = request.form['start'].strip()
        destination = request.form['destination'].strip()
        distance = request.form['distance']
        hours = int(request.form.get('duration_hours', 0))
        minutes = int(request.form.get('duration_minutes', 0))

        travel_time = hours * 60 + minutes

        db = db_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO routes (start, destination, distance_km, travel_time)
            VALUES (%s, %s, %s, %s)
        """, (start, destination, distance, travel_time))

        db.commit()
        db.close()

        flash("Route added successfully.", "success")
        return redirect(url_for('admin.routes'))

    return render_template('add_route.html')


@admin_bp.route('/delete_route/<int:route_id>')
def delete_route(route_id):
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM routes WHERE id = %s", (route_id,))
        db.commit()
        flash("Route deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash("Cannot delete this route because it may be linked to existing schedules.", "danger")
        print("Delete route error:", e)
    finally:
        db.close()

    return redirect(url_for('admin.routes'))


@admin_bp.route('/schedules')
def schedules():
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            s.id AS id,
            b.bus_number AS bus_number,
            r.start AS start,
            r.destination AS destination,
            s.departure_time AS departure_time,
            s.arriving_time AS arriving_time,
            s.price AS price
        FROM schedules s
        JOIN buses b ON s.bus_id = b.id
        JOIN routes r ON s.route_id = r.id
        ORDER BY s.departure_time DESC
    """)
    schedules = cursor.fetchall()

    db.close()

    return render_template('schedules.html', schedules=schedules)


@admin_bp.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        bus_id = request.form['bus_id']
        route_id = request.form['route_id']
        departure_time = request.form['departure_time']
        arriving_time = request.form['arriving_time']
        price = request.form['price']

        cursor.execute("""
            INSERT INTO schedules (bus_id, route_id, departure_time, arriving_time, price)
            VALUES (%s, %s, %s, %s, %s)
        """, (bus_id, route_id, departure_time, arriving_time, price))

        db.commit()
        db.close()

        flash("Schedule added successfully.", "success")
        return redirect(url_for('admin.schedules'))

    cursor.execute("""
        SELECT id, bus_number, seats_number
        FROM buses
        ORDER BY bus_number ASC
    """)
    buses = cursor.fetchall()

    cursor.execute("""
        SELECT id, start, destination, distance_km
        FROM routes
        ORDER BY start ASC
    """)
    routes = cursor.fetchall()

    db.close()

    return render_template('add_schedule.html', buses=buses, routes=routes)


@admin_bp.route('/delete_schedule/<int:schedule_id>')
def delete_schedule(schedule_id):
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM schedules WHERE id = %s", (schedule_id,))
        db.commit()
        flash("Schedule deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash("Cannot delete this schedule because it may be linked to existing bookings.", "danger")
        print("Delete schedule error:", e)
    finally:
        db.close()

    return redirect(url_for('admin.schedules'))


@admin_bp.route('/buses')
def buses():
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            b.id AS id,
            b.bus_number AS bus_number,
            b.seats_number AS seats_number,
            b.colour AS colour,
            d.name AS driver_name
        FROM buses b
        LEFT JOIN drivers d ON b.driver_id = d.id
        ORDER BY b.id DESC
    """)
    buses = cursor.fetchall()

    db.close()

    return render_template('buses.html', buses=buses)


@admin_bp.route('/add_bus', methods=['GET', 'POST'])
def add_bus():
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        bus_number = request.form['bus_number'].strip()
        seats_number = request.form['seats_number']
        colour = request.form['colour'].strip()
        driver_id = request.form['driver_id']

        cursor.execute("""
            INSERT INTO buses (bus_number, seats_number, colour, driver_id)
            VALUES (%s, %s, %s, %s)
        """, (bus_number, seats_number, colour, driver_id))

        db.commit()
        db.close()

        flash("Bus added successfully.", "success")
        return redirect(url_for('admin.buses'))

    cursor.execute("""
        SELECT id, name, status
        FROM drivers
        ORDER BY name ASC
    """)
    drivers = cursor.fetchall()

    db.close()

    return render_template('add_buses.html', drivers=drivers)


@admin_bp.route('/delete_bus/<int:bus_id>')
def delete_bus(bus_id):
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM buses WHERE id = %s", (bus_id,))
        db.commit()
        flash("Bus deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash("Cannot delete this bus because it may be linked to existing schedules.", "danger")
        print("Delete bus error:", e)
    finally:
        db.close()

    return redirect(url_for('admin.buses'))


@admin_bp.route('/drivers')
def drivers():
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, license_number, phone, experience, status
        FROM drivers
        ORDER BY id DESC
    """)
    drivers = cursor.fetchall()

    db.close()

    return render_template('drivers.html', drivers=drivers)


@admin_bp.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    if not admin_required():
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name'].strip()
        license_number = request.form['license_number'].strip()
        phone_number = request.form['phone_number'].strip()
        experience = request.form['experience']
        status = request.form['status']

        db = db_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO drivers (name, license_number, phone, experience, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, license_number, phone_number, experience, status))

        db.commit()
        db.close()

        flash("Driver added successfully.", "success")
        return redirect(url_for('admin.drivers'))

    return render_template('add_driver.html')


@admin_bp.route('/delete_driver/<int:driver_id>')
def delete_driver(driver_id):
    if not admin_required():
        return redirect('/login')

    db = db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM drivers WHERE id = %s", (driver_id,))
        db.commit()
        flash("Driver deleted successfully.", "success")
    except Exception as e:
        db.rollback()
        flash("Cannot delete this driver because it may be linked to existing buses.", "danger")
        print("Delete driver error:", e)
    finally:
        db.close()

    return redirect(url_for('admin.drivers'))