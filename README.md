# 🌐 Flask Multipage Web App

A simple multi-page Flask application that demonstrates routing, templates, and dynamic URLs.

## 🚀 Features

- Home page and About page
- Dynamic user profile page (`/user/<username>`)
- Jinja2 templating
- Easy to extend and deploy

## 🧪 How to Run

```bash
python app.py

Then visit:

Home: http://127.0.0.1:5000/

About: http://127.0.0.1:5000/about

User Profile: http://127.0.0.1:5000/user/YourName

📁 Folder Structure
arduino
Copy
Edit
flask-multipage-app/
├── app.py
├── templates/
│   ├── home.html
│   ├── about.html
│   └── user.html
└── README.md

🧠 Built With
Python 3

Flask

HTML + Jinja2 Templates

## 🔗 Live Demo

👉 [View Website](https://flask-multipage-app-vi7o.onrender.com/)

## ✨ New Features
- Base layout + clean styling
- Greeting form → `/greet?name=YourName`
- User info route → `/who/<name>` (role + city demo)

## 🗒️ Guestbook (SQLite)
- Route: `/guestbook`
- Features: Add name + message, list recent entries
- Tech: Python `sqlite3`, simple DAO in `database.py`

## ✨ Guestbook Pro Features
- Create, **Edit**, **Delete** entries
- **Search** by name/message (`?q=term`)
- **Pagination** (`?page=1&limit=5`)
- **Export CSV**: `/guestbook/export`
