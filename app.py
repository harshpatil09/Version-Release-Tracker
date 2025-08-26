from flask import Flask, render_template, redirect, flash, session, url_for, request
import logging.config
from modules.Database.db_con import mysqlDB_conn
import service_mpl 
from config import secret_key_config

# Init the log file
logging.config.fileConfig('logging.cfg')

# Create app
app = Flask(__name__)

# Secrete key config
app.config.from_object(secret_key_config)

# Connect the database
mysqlDB_conn(app)
app.logger.info("The DB connectivity is done.")

# Routes
@app.route('/', methods=["POST","GET"])
def login_landing():
    app.logger.info("User entered Login page")
    return render_template('login_page.html')

@app.route("/logout")
def logout():
    app.logger.warning(f"User : {session['Username']} logged out successfully!")
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("login_landing"))

@app.route('/employee/registration', methods=["POST","GET"])
def emp_register_form():
    app.logger.info("User entered page to register new employee.")
    return render_template("new_registration.html")

@app.route('/registration_ops',methods=["POST","GET"])
def emp_register():
    return service_mpl.register_employee_ops.register_emp_func()

@app.route('/employee/login', methods=["POST", "GET"])
def login_emp():
    return service_mpl.login_ops.login_funcs()

@app.route('/home', methods=['POST','GET'])
def home():
    app.logger.info("User entred home page!")   
    return render_template('home.html')

# @app.route('/version/new/form', methods=["POST","GET"])
# def release_version_form():
#     return render_template("release_new_version.html")

@app.route('/version/new', methods=['POST','GET'])
def release_version():
    return service_mpl.release_ops.release_new_version()

@app.route('/version/history')
def version_history():
    return service_mpl.version_history.version_hist()

@app.route('/update_release', methods=['POST','GET'])
def update_release():
    return service_mpl.vesion_history_update.update_hist()

@app.route('/delete_record/<ReleaseID>', methods=['POST', 'GET'])
def delete_version_record(ReleaseID):
    return service_mpl.delete_hist_record_op.delete_record(ReleaseID)

if __name__ == '__main__':
    app.run(debug=True, port=9000)