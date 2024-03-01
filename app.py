from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='hospital'
    )
    return conn

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Patient Section
@app.route('/patient')
def patient_operations():
    return render_template('patient_operations.html')

# Add a new patient
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        patient_name = request.form['Pat_Fname']
        patinet_lname = request.form['Pat_Lname']
        patinet_id = request.form['Pat_ID']
        patinet_phone = request.form['Pat_Phone']
        discharge_date = request.form['Discharge_Date']
        admission_date = request.form['Admission_Date']
        ward_no = request.form['Ward_No']
        patinet_dob = request.form['Pat_DOB']

        try:
            cursor.execute('INSERT INTO Patient (Pat_ID, Pat_Fname, Pat_Lname, Pat_Phone, Discharge_Date, Admission_Date, Ward_No, Pat_DOB) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                           (patinet_id, patient_name, patinet_lname, patinet_phone, discharge_date, admission_date, ward_no, patinet_dob))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('patient_operations'))

    return render_template('add_patient.html')

# Delete a patient
@app.route('/delete_patient', methods=['GET', 'POST'])
def delete_patient():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        patinet_id = request.form['Pat_ID']

        try:
            cursor.execute('DELETE FROM Patient WHERE Pat_ID = %s', (patinet_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('patient_operations'))

    return render_template('delete_patient.html')

# Update a patient
@app.route('/find_patient', methods = ['GET', 'POST'])
def find_patient():
    if request.method == 'POST': 
        find_pat_id = request.form['Pat_ID']
        global patinet2_id
        patinet2_id = int(find_pat_id)
        return redirect(url_for('update_patient'))
    return render_template('find_patient.html')

@app.route('/update_patient', methods=['GET', 'POST'])
def update_patient():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patient')
    patient_data = cursor.fetchall()

    if request.method == 'POST':
        
        updated_name = request.form.get('Pat_Fname')
        updated_lname = request.form.get('Pat_Lname')
        updated_phone = request.form.get('Pat_Phone')
        try:
            cursor.execute('UPDATE Patient SET Pat_Fname = %s, Pat_Lname = %s, Pat_Phone = %s WHERE Pat_ID = %s',
                           (updated_name, updated_lname, updated_phone, patinet2_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('patient_operations'))
    return render_template('update_patient.html', patient_data = patient_data, patinet2_id = patinet2_id)

# Fetch all patients
@app.route('/get_all_patients')
def get_all_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM Patient')
        patients = cursor.fetchall()
        return jsonify({"patients": patients})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"patients": []})
    finally:
        cursor.close()
        conn.close()

# Employee Section
@app.route('/employee')
def employee_operations():
    return render_template('employee_operations.html')

# Add a new employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        employee_name = request.form['Emp_Fname']
        employee_last_name = request.form['Emp_Lname']
        employee_id = request.form['Emp_ID']
        employee_phone = request.form['Emp_Phone']
        employee_gender = request.form['Emp_Gender']
        employee_DOB = request.form['Emp_DOB']
        role_ID = request.form['Role_ID']
        add_ID = request.form['Add_ID']

        try:
            cursor.execute('INSERT INTO Employee (Emp_ID, Emp_Fname, Emp_Lname, Emp_Phone, Emp_Gender, Emp_DOB, Role_ID, Add_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                           (employee_id, employee_name, employee_last_name, employee_phone, employee_gender, employee_DOB, role_ID, add_ID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('employee_operations'))

    return render_template('add_employee.html')

# Delete an employee
@app.route('/delete_employee', methods=['GET', 'POST'])
def delete_employee():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        employee_id = request.form['Emp_ID']

        try:
            cursor.execute('DELETE FROM Employee WHERE Emp_ID = %s', (employee_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('employee_operations'))

    return render_template('delete_employee.html')

# Update an employee
@app.route('/find_employee', methods = ['GET', 'POST'])
def find_employee():
    if request.method == 'POST': 
        find_emp_id = request.form['Emp_ID']
        global emp_id
        emp_id = int(find_emp_id)
        return redirect(url_for('update_employee'))
    return render_template('find_employee.html')

@app.route('/update_employee', methods=['GET', 'POST'])
def update_employee():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Employee')
    employee_data = cursor.fetchall()

    if request.method == 'POST':

        updated_name = request.form['Emp_Name']
        updated_last_name = request.form['Emp_Lname']
        updated_phone = request.form['Emp_Phone']
        updated_role_ID = request.form['Role_ID']

        try:
            cursor.execute('UPDATE Employee SET Emp_Fname = %s, Emp_Lname = %s, Emp_Phone = %s, Role_ID = %s WHERE Emp_ID = %s',
                           (updated_name, updated_last_name, updated_phone, updated_role_ID, emp_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('employee_operations'))

    return render_template('update_employee.html', employee_data=employee_data, emp_id = emp_id)

@app.route('/get_all_employees')
def get_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM Employee')
        employees = cursor.fetchall()
        return jsonify({"employees": employees})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"employees": []})
    finally:
        cursor.close()
        conn.close()

# Appointment Section
@app.route('/appointment')
def appointment_operations():
    return render_template('appointment_operations.html')

# Add a new employee
@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        appointment_id = request.form['Appointment_ID']
        app_date = request.form['App_Date']
        app_type = request.form['App_Type']
        employ_id = request.form['Emp_ID']
        pati_id = request.form['Pat_ID']

        try:
            cursor.execute('INSERT INTO Appointment VALUES (%s, %s, %s, %s, %s)', 
                           (appointment_id, app_date, app_type, employ_id, pati_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('appointment_operations'))

    return render_template('add_appointment.html')

# Delete an appointment
@app.route('/delete_appointment', methods=['GET', 'POST'])
def delete_appointment():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        appointment_id = request.form['App_ID']

        try:
            cursor.execute('DELETE FROM Appointment WHERE App_ID = %s', (appointment_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('appointment_operations'))

    return render_template('delete_appointment.html')

# Update an appointment
@app.route('/find_appointment', methods = ['GET', 'POST'])
def find_appointment():
    if request.method == 'POST': 

        find_app_id = request.form['App_ID']
        global app_id
        app_id = int(find_app_id)

        return redirect(url_for('update_appointment'))
    return render_template('find_appointment.html')

@app.route('/update_appointment', methods=['GET', 'POST'])
def update_appointment():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Appointment')
    app_data = cursor.fetchall()
    global appo_id
    if request.method == 'GET':
        for i in range(0, len(app_data)):
            if app_id == app_data[i][0]: 
                appo_id = app_data.index(app_data[i])

    if request.method == 'POST':

        u_app_date = request.form['App_Date']
        u_app_type = request.form['App_Type']
        u_employ_id = request.form['Emp_ID']

        try:
            cursor.execute('UPDATE Appointment SET App_Date = %s, App_Type = %s, Emp_ID = %s WHERE App_ID = %s',
                           (u_app_date, u_app_type, u_employ_id, appo_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('appointment_operations'))

    return render_template('update_appointment.html', app_data = app_data, app_id = appo_id)

@app.route('/get_all_appointments')
def get_all_appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT * FROM Appointment')
        appointments = cursor.fetchall()
        return jsonify({"appointments": appointments})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"appointments": []})
    finally:
        cursor.close()
        conn.close()

@app.route('/patients_with_appointment')
def patients_with_appointment():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute('SELECT Patient.*, Appointment.App_ID, Appointment.App_Date, Appointment.App_Type FROM Patient JOIN Appointment ON Patient.Pat_ID = Appointment.Pat_ID')
        patient_data = cursor.fetchall()
    except Exception as e:
        print(f"Error: {str(e)}")
        patient_data = []

    finally:
        cursor.close()
        conn.close()

    return render_template('patients_with_appointment.html', patient_data=patient_data)

if __name__ == '__main__':
    app.run(debug=True)
