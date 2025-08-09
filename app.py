from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
