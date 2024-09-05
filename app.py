from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == "user@example.com" and password == "password":
            flash('Sign in successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('signin'))
    return render_template('signin.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password == confirm_password:
            flash('Account created successfully! Please sign in.', 'success')
            return redirect(url_for('signin'))
        else:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
