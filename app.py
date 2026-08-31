from flask import Flask, render_template, request, redirect, session, url_for, send_file
import mysql.connector
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = "expense_tracker"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Arafathali@45",
    database="expense_tracker"
)

@app.route('/')
def home():

    if 'user_id' not in session:
        return redirect('/login')

    category = request.args.get('category')
    search = request.args.get('search')

    query = """
    SELECT * FROM expenses
    WHERE user_id=%s
    """

    values = [session['user_id']]

    if category and category != "All":
        query += " AND category=%s"
        values.append(category)

    if search:
        query += " AND notes LIKE %s"
        values.append(f"%{search}%")

    cursor = db.cursor(dictionary=True)
    cursor.execute(query, tuple(values))

    expenses = cursor.fetchall()

    return render_template(
        'dashboard.html',
        expenses=expenses
    )


@app.route('/add', methods=['POST'])
def add_expense():
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    notes = request.form['notes']

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO expenses(user_id,amount,category,expense_date,notes)
        VALUES(%s,%s,%s,%s,%s)
    """,(session['user_id'],amount,category,date,notes))

    db.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_expense(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=%s",(id,))
    db.commit()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(
            request.form['password']
        )

        cursor = db.cursor()

        cursor.execute("""
        INSERT INTO users
        (username,email,password)
        VALUES(%s,%s,%s)
        """,(username,email,password))

        db.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user and check_password_hash(
            user['password'],
            password
        ):

            session['user_id'] = user['id']
            session['username'] = user['username']

            return redirect('/')

    return render_template('login.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

@app.route('/edit/<int:id>')
def edit_page(id):

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM expenses WHERE id=%s",
        (id,)
    )

    expense = cursor.fetchone()

    return render_template(
        'edit_expense.html',
        expense=expense
    )

@app.route('/update/<int:id>', methods=['POST'])
def update_expense(id):

    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    notes = request.form['notes']

    cursor = db.cursor()

    cursor.execute("""
    UPDATE expenses
    SET amount=%s,
        category=%s,
        expense_date=%s,
        notes=%s
    WHERE id=%s
    """,(amount,category,date,notes,id))

    db.commit()

    return redirect('/')

@app.route('/set_budget', methods=['GET','POST'])
def set_budget():

    month = request.form['month']
    amount = request.form['amount']

    cursor = db.cursor()

    cursor.execute("""
    INSERT INTO budgets(user_id, month, budget_amount)
    VALUES(%s,%s,%s)
    """, (
        session['user_id'],
        month,
        amount
    ))

    db.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

