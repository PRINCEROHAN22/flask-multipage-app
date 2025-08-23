from flask import Flask, render_template, request, redirect, url_for, Response
from flask import jsonify
import random
from utils_text import summarize  # add at top with other imports
from utils_sentiment import sentiment_label
from database import (
    init_db, add_entry, get_entries, get_entries_paged,
    count_entries, get_entry, update_entry, delete_entry
)

app = Flask(__name__)
init_db()  # create table if not exists when app starts

QUOTES = [
    "Keep going. Your future self is watching.",
    "Tiny steps daily beat bursts of effort.",
    "Ship. Learn. Iterate. Win.",
    "Energy > intensity. Consistency wins.",
    "Build quietly. Let results make the noise."
]


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user/<username>')
def user_profile(username):
    return render_template("user.html", username=username)


@app.route('/greet', methods=['GET', 'POST'])
def greet():
    name = request.values.get('name', 'Friend')
    return render_template("user.html", username=name)


USERS = {
    "Rohan": {"role": "admin", "city": "Chennai"},
    "Eva": {"role": "guide", "city": "Everywhere"},
}

@app.route('/who/<name>')
def who(name):
    info = USERS.get(name, {"role": "guest", "city": "Unknown"})
    return render_template("user.html", username=f"{name} ({info['role']}, {info['city']})")


@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    error = None
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        message = (request.form.get('message') or '').strip()
        if not name or not message:
            error = "Name and message are required."
        else:
            add_entry(name, message)
            return redirect(url_for('guestbook'))

    # query params for search & pagination
    q = (request.args.get('q') or '').strip()
    page = max(1, int(request.args.get('page', 1)))
    limit = max(1, int(request.args.get('limit', 5)))

    total = count_entries(q=q if q else None)
    total_pages = max(1, (total + limit - 1) // limit)
    page = min(page, total_pages)

    entries = get_entries_paged(page=page, limit=limit, q=q if q else None)

    return render_template(
        'guestbook.html',
        entries=entries, error=error,
        q=q, page=page, total_pages=total_pages, limit=limit
    )


@app.route('/guestbook/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_entry_route(item_id):
    row = get_entry(item_id)
    if not row:
        return redirect(url_for('guestbook'))
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        message = (request.form.get('message') or '').strip()
        if name and message:
            update_entry(item_id, name, message)
            return redirect(url_for('guestbook'))
    # row: (id, name, message, created_at)
    return render_template('edit.html', item=row)


@app.route('/guestbook/<int:item_id>/delete', methods=['POST'])
def delete_entry_route(item_id):
    delete_entry(item_id)
    return redirect(url_for('guestbook'))


@app.route('/guestbook/export')
def export_csv():
    # export all (ignoring pagination/search for simplicity)
    rows = get_entries()  # (name, message, created_at)
    import csv, io
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['name', 'message', 'created_at'])
    for r in rows:
        writer.writerow([r[0], r[1], r[2]])
    csv_data = buf.getvalue()
    buf.close()
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=guestbook.csv'}
    )

@app.route('/summarize', methods=['GET', 'POST'])
def summarize_view():
    # accept from form (POST) or query string (GET)
    text = (request.values.get('text') or "").strip()
    k_raw = request.values.get('k', 2)
    try:
        k = int(k_raw)
    except (TypeError, ValueError):
        k = 2

    result = summarize(text, max_sentences=k) if text else None
    return render_template('summarize.html', text=text, result=result)

@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment_view():
    text = (request.values.get('text') or "").strip()
    label = score = None
    if text:
        label, score = sentiment_label(text)
    return render_template('sentiment.html', text=text, label=label, score=score)

@app.route('/lab')
def lab():
    return render_template('lab.html')

@app.route("/api/quote")
def api_quote():
    return jsonify({"quote": random.choice(QUOTES)})


if __name__ == '__main__':
    app.run(debug=True)