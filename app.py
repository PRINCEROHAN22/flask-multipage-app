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

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except TypeError:
        return "Inputs must be numbers"
    
USERS = {
    "Rohan": {"role": "admin", "city": "Chennai"},
    "Eva": {"role": "guide", "city": "Everywhere"},
}

@app.route('/who/<name>')
def who(name):
    info = USERS.get(name, {"role": "guest", "city": "Unknown"})
    return render_template("user.html", username=f"{name} ({info['role']}, {info['city']})")

@app.route('/divide')
def divide():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    result = safe_divide(a, b)
    return render_template("user.html", username=f"Result: {result}")



if __name__ == '__main__':
    app.run(debug=True)
