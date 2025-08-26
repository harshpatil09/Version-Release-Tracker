from flask import render_template, request, current_app as app, redirect, url_for, session, flash
from modules.Database import queries
from src import new_release_ops, login_employee, new_emp_registration, update_version_records

q1 = queries.version_queries()
q2 = queries.preload_data_new_version()
in1 = new_release_ops.insert()
v1 = new_release_ops.validation()
l1 = login_employee.login()
rv1 = new_emp_registration.validate()
ur1 = update_version_records.update_version_record()

class register_employee_ops:
    def register_emp_func():
        
        if request.method == "POST":
            
            reg_form_data = request.form.to_dict() #store form data
            
            val_result = rv1.validate_new_register(reg_form_data) #validate form data

            if val_result["flag"]:
               
                # insert validated data
               insert_new_emp_result = new_emp_registration.insert_data.register_new_emp(reg_form_data)
               
               if insert_new_emp_result["flag"]:
                   app.logger.info(f"User {reg_form_data.get('Username')} registration successfull, data is stored in Database")
                   flash(insert_new_emp_result["message"])
                   return redirect(url_for('login_landing'))
               else:
                   app.logger.error(f"Something Wrong in the new employee registation data inserting query : {insert_new_emp_result['message']}")
                   flash(insert_new_emp_result["message"])
                   return redirect(url_for('emp_register_form'))

            else:
                app.logger.warning(f"User failed to register : {val_result['message']}")
                flash(f'Try Again : {val_result["message"]}')
                return redirect(url_for('emp_register_form'))

        app.logger.error("Error in data sending in registration form!!")
        flash("Something is wrong in sending data! Try again")
        return redirect(url_for('emp_register_form'))

class login_ops:
    def login_funcs():
        
        if request.method == "POST":
            
            login_creds = request.form.to_dict()
            
            vali_result = l1.login_validation(login_creds)
            if vali_result["flag"]:
                app.logger.info(f"User :{login_creds.get('Username')} Login successful.")
                flash("Login Successfull.")
                
                user_creds = vali_result["user_creds"]
                
                # Assign session
                session['Username'] = user_creds.Username
                session['Role'] = user_creds.Role
                
                return redirect(url_for('home'))
            
            else:
                app.logger.warning("User login failed!")
                flash(vali_result["message"])
                return redirect(url_for('login_landing'))
            
        return render_template("login_page.html", js_alert="Error in sending credentials!")
    
class version_history:

    def version_hist():
        result = q1.fetch_version_hist()
        if result["flag"]:
            app.logger.info("Version History data is fetch successfully from version_release table.")
            app.logger.info("Version History is displayed successfully.")
            return render_template('version_hist.html', data=result["data"])
        else:
            app.logger.error(f"Something went wrong in data retrival version history model :{result['message']}")
            return render_template('home.html', js_alert=result["message"])

class release_ops:

    def release_new_version():

        appl_result = q2.fetch_application()
        mod_result = q2.fetch_modules()
        submod_result = q2.fetch_submodules()

        if not appl_result["flag"] or not mod_result["flag"] or not submod_result["flag"]:
            app.logger.error("Something went wrong in data preloading in new version registration form!!")
            flash("Something went wrong in data retrival")
            return redirect(url_for('home'))  

        app.logger.info("Data is preloaded in the form successful for new version registration.")
        
        if request.method == 'POST':
            form_data = request.form.to_dict()
            
            
            validate_result = v1.new_release_data_validate(form_data)
            
            if not validate_result["flag"]:
                app.logger.warning("User failed validation for registering new verison!!")
                flash(validate_result["message"])
                return render_template("release_new_version.html")

            #Inserting funtion         
            result = in1.insert_new_release(form_data)
            flash(result)
            app.logger.info("New Version Registered Successfully.")
            return redirect(url_for('home'))                
            
        return render_template("release_new_version.html", appl_data = appl_result["appl_data"], mod_data = mod_result["mod_data"], submod_data = submod_result["submod_data"])

class vesion_history_update:
    def update_hist():
        
        if request.method == "POST":
            updated_data = request.form.to_dict()
            app.logger.info("Updated data received at backend")
            u_result = ur1.update_version(updated_data)
            
            if u_result["flag"]:
                flash("Record is updated successfully.")
                app.logger.info(f"Record is updated for ReleaseID : {updated_data.get('ReleaseID')}.")
                return redirect(url_for('version_history'))
            else:
                flash("Can't Update the record something went wrong!")
                return  redirect(url_for('version_history'))
            
        app.logger.info("data is not in post but enter into def")
        flash("data nahi milala")
        return render_template("home.html")
    
# change the return type to dic and write the logs
class delete_hist_record_op:
    def delete_record(ReleaseID):
        delete_record_result = queries.delete_version_record_query.delete_record_q(ReleaseID)
        if delete_record_result:
            app.logger.warning(f"User deleted record of ReleaseID : {ReleaseID}")
            flash("Record deleted successfully.")
            return redirect(url_for('version_history'))
        else:
            flash("Something went wrong in deleting record.")
            return redirect(url_for('version_history'))