from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DATABASE = 'donors.db'

# --------------------------
# DATABASE HELPER
# --------------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn

# --------------------------
# DATABASE INITIALIZATION
# --------------------------
def init_db():
    try:
        with get_db_connection() as conn: 
            conn.execute('''
                CREATE TABLE IF NOT EXISTS donors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    blood_group TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    city TEXT NOT NULL
                )
            ''')
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

init_db()

# --------------------------
# HOME PAGE
# --------------------------
@app.route('/')
def home():
    return render_template('index.html')

# --------------------------
# REGISTER DONOR
# --------------------------
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name', '').strip()
    blood_group = request.form.get('blood_group', '').strip().upper()
    phone = request.form.get('phone', '').strip()
    city = request.form.get('city', '').strip().title()

    if not all([name, blood_group, phone, city]):
        return render_template('index.html', message="Error: All fields are required!")

    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO donors (name, blood_group, phone, city) VALUES (?, ?, ?, ?)",
                      (name, blood_group, phone, city))
        return render_template('index.html', message="Donor Registered Successfully!")
    
    except sqlite3.Error as e:
        return render_template('index.html', message=f"Database error: {e}")

# --------------------------
# SEARCH DONOR
# --------------------------
@app.route('/search', methods=['GET'])
def search():
    blood_group = request.args.get('blood_group', '').strip().upper()
    city = request.args.get('city', '').strip().title()

    if not blood_group or not city:
        return render_template('results.html', donors=[], message="Please provide both blood group and city.")

    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT name, blood_group, phone, city FROM donors WHERE blood_group=? AND city=?",
                (blood_group, city)
            )
            results = cursor.fetchall()
        
        return render_template('results.html', donors=results)
        
    except sqlite3.Error as e:
        return render_template('results.html', donors=[], message=f"Database error: {e}")

# --------------------------
# RUN APP
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)