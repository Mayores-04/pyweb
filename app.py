from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['YourDatabaseName']  # Make sure to replace with your actual database name
collection = db['Employees']

@app.route('/')
def index():
    # Fetch all employee data for admin interface
    employees = list(collection.find())
    return render_template('index.html', employees=employees)

@app.route('/home')
def home():
    # Fetch all employee data for user interface
    employees = list(collection.find())
    return render_template('home.html', employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    # Get data from form and insert into MongoDB
    new_employee = {
        "employeeName": request.form['name'],
        "employeeEmail": request.form['email'],
        "employeePassword": request.form['password'],
        "employeeProfilePic": request.form['profile_pic']
    }
    collection.insert_one(new_employee)
    return redirect(url_for('index'))

@app.route('/update/<employee_id>', methods=['POST'])
def update_employee(employee_id):
    # Update employee information in MongoDB
    updated_employee = {
        "employeeName": request.form['name'],
        "employeeEmail": request.form['email'],
        "employeePassword": request.form['password'],
        "employeeProfilePic": request.form['profile_pic']
    }
    collection.update_one(
        {"_id": ObjectId(employee_id)},
        {"$set": updated_employee}
    )
    return redirect(url_for('index'))

@app.route('/delete/<employee_id>', methods=['POST'])
def delete_employee(employee_id):
    # Delete employee from MongoDB
    collection.delete_one({"_id": ObjectId(employee_id)})
    return redirect(url_for('index'))

@app.route('/api/employees', methods=['GET'])
def get_employees():
    # API endpoint to fetch all employees for real-time updates in user interface
    employees = list(collection.find())
    for employee in employees:
        employee['_id'] = str(employee['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(employees)

if __name__ == '__main__':
    app.run(debug=True)
