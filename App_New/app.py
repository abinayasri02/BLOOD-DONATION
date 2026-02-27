from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests
import os

app = Flask(__name__)

# --- SECURE SMS ALERT SYSTEM (Fast2SMS) ---
FAST2SMS_API_KEY = os.environ.get('DoFkHYpPmJf8y4tv5cCn6jMRB0wU7G1aQLus2IxSKzE3hdiXqra47tQIhY25Dde8mLJcjPsKG6fTH90C')

def send_request_sms(donor_phone, patient_data, contact_data):
    """Sends a real SMS using the Fast2SMS Indian Gateway"""
    
    sms_body = (
        f"🚨 URGENT BLOOD NEEDED 🚨\n"
        f"Patient: {patient_data['name']} ({patient_data['blood_group']})\n"
        f"Hospital: {patient_data['hospital']}, {patient_data['locality']}\n"
        f"Please call {contact_data['name']} immediately at {contact_data['phone']}!"
    )
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    querystring = {
        "authorization": FAST2SMS_API_KEY,
        "message": sms_body,
        "language": "english",
        "route": "q",
        "numbers": donor_phone
    }
    
    try:
        response = requests.request("GET", url, params=querystring)
        print("Fast2SMS Server Response:", response.text)
    except Exception as e:
        print(f"SMS failed to send: {e}")

# --- UPGRADED DATABASE HELPER (The Render Fix!) ---
def get_db_connection():
    conn = sqlite3.connect('donors.db')
    conn.row_factory = sqlite3.Row
    
    # This magic block auto-builds the database if Render ever deletes it!
    conn.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            state TEXT NOT NULL,
            district TEXT NOT NULL,
            locality TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    return conn

# --- ROUTES ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO donors (name, blood_group, state, district, locality, phone, email) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (request.form['name'], request.form['blood_group'], request.form['state'], 
             request.form['district'], request.form['locality'], request.form['phone'], request.form['email'])
        )
        conn.commit()
        conn.close()
        return render_template('home.html', message="Registration Successful!")
    return render_template('register.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        blood_group = request.form['blood_group']
        state = request.form['state']
        district = request.form['district']
        locality = request.form['locality']
        
        conn = get_db_connection()
        donors = conn.execute(
            'SELECT * FROM donors WHERE blood_group = ? AND state = ? AND district = ? AND locality = ?',
            (blood_group, state, district, locality)
        ).fetchall()
        conn.close()
        return render_template('search.html', donors=donors, searched=True)
        
    return render_template('search.html', searched=False)

@app.route('/request_donor/<int:donor_id>', methods=['GET', 'POST'])
def request_donor(donor_id):
    conn = get_db_connection()
    donor = conn.execute('SELECT * FROM donors WHERE id = ?', (donor_id,)).fetchone()
    
    if request.method == 'POST':
        patient_data = {
            'name': request.form['patient_name'],
            'blood_group': request.form['patient_blood_group'],
            'district': request.form['district'],
            'locality': request.form['locality'],
            'hospital': request.form['hospital']
        }
        contact_data = {
            'name': request.form['contact_name'],
            'phone': request.form['contact_phone'],
            'message': request.form['message']
        }
        
        # Trigger the SMS!
        send_request_sms(donor['phone'], patient_data, contact_data)
        
        conn.close()
        return render_template('home.html', message="SMS Request sent to donor successfully!")
        
    conn.close()
    return render_template('request_form.html', donor=donor)

if __name__ == '__main__':
    app.run(debug=True)