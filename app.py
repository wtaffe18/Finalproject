import sqlite3
from flask import Flask, render_template, request, redirect, g

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

DATABASE = 'reservation.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create the reservations table if it doesn't exist
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                check_in DATE,
                check_out DATE,
                room_type TEXT
            )
        ''')
        db.commit()

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form['name']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        room_type = request.form['room_type']

        conn = sqlite3.connect('reservation.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reservations (name, check_in, check_out, room_type) VALUES (?, ?, ?, ?)', (name, check_in, check_out, room_type))
        conn.commit()
        conn.close()

        return render_template('confirmation.html', name=name, check_in=check_in, check_out=check_out)

    return render_template('reservation.html')

@app.route('/reservation_list')
def reservation_list():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name, check_in, check_out, room_type FROM reservations')
    reservations = cursor.fetchall()

    return render_template('reservation_list.html', reservations=reservations)

if __name__ == '__main__':
    init_db()
    app.run()

