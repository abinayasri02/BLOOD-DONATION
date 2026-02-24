# 🩸 BloodToday - Blood Donor Database

Welcome to BloodToday, a lightweight, secure web application designed to help connect blood donors with those in need. This project allows users to easily register as donors and allows hospitals or individuals to search for available donors by blood group and city.

## 🚀 Features

* Donor Registration: A simple, intuitive form for new donors to enter their contact details, blood group, and city.
* Smart Search: Users can filter the database to find exact matches for specific blood groups in specific locations.
* Secure Database: Built with SQLite using parameterized queries to prevent SQL injection attacks.
* Modern UI: A clean, responsive user interface built with HTML5 and custom CSS.

## 🛠️ Tech Stack

* Backend: Python, Flask
* Database: SQLite3
* Frontend: HTML5, CSS3
* Architecture: Client-Server, standard WSGI application

## 📂 Project Structure

`text
Blood-Donation/
│
├── app.py                 # The main Flask application and routing logic
├── donors.db              # The SQLite database (generated automatically)
├── static/                
│   └── bg.jpg             # Custom background image for the UI
└── templates/             
    ├── index.html         # Homepage and registration/search forms
    └── results.html       # Dynamic search results table
