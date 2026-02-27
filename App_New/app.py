from flask import Flask, render_template, request
import sqlite3
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# --- EMAIL ALERT SYSTEM ---
SENDER_EMAIL = "onef6rall@gmail.com"
SENDER_PASSWORD = "krshtziiezyhfxnh"  # Look! No spaces!

def send_request_email(donor_email, patient_data, contact_data):
    try:
        msg = EmailMessage()
        msg['Subject'] = "🚨 URGENT: Blood Request via BloodToday"
        msg['From'] = SENDER_EMAIL
        msg['To'] = donor_email
        
        body = f"""
        URGENT BLOOD REQUEST
        
        Patient Details:
        - Name: {patient_data['name']}
        - Blood Group: {patient_data['blood_group']}
        - Location: {patient_data['locality']}, {patient_data['district']}
        - Hospital: {patient_data['hospital']}
        
        Contact Details:
        - Contact Name: {contact_data['name']}
        - Phone Number: {contact_data['phone']}
        - Message: {contact_data['message']}
        
        Please contact them immediately if you can donate!
        """
        msg.set_content(body)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email failed to send: {e}")

# --- UPGRADED DATABASE HELPER ---
def get_db_connection():
    conn = sqlite3.connect('donors.db')
    conn.row_factory = sqlite3.Row
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
        conn = get_db_connection()
        donors = conn.execute(
            'SELECT * FROM donors WHERE blood_group = ? AND state = ? AND district = ? AND locality = ?',
            (request.form['blood_group'], request.form['state'], request.form['district'], request.form['locality'])
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
        contact_data = {'name': request.form['contact_name'],
            'phone': request.form['contact_phone'],
            'message': request.form['message']
        }
        
        # Trigger the Email!
        send_request_email(donor['email'], patient_data, contact_data)
        
        conn.close()
        return render_template('home.html', message="Alert sent to donor successfully!")
        
    conn.close()
    return render_template('request_form.html', donor=donor)

if __name__ == '__main__':

    app.run(debug=True)
