from flask import current_app as app, session
from modules.Database.db_con import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash

class emp_register_query:
    def unique_username(self, Username):
        try:
            sql = text("SELECT * FROM employee_details WHERE (Username = :Username)")
            query_result = db.session.execute(sql,{
                'Username': Username
            }).fetchone()
            
            if query_result:
                return {"flag":False, "message":"Username is already taken!"}
            else:
                return {"flag":True, "message":"Username is granted"}   
        except SQLAlchemyError as e:
            return {"flag":False, "message":f"Database error: {str(e)}"}
        
    def unique_empid_query(self, Empid):
        try:
            sql = text("SELECT * FROM employee_details WHERE (Empid = :Empid)")
            query_result = db.session.execute(sql,{
                "Empid" : Empid
            }).fetchone()
            
            if not query_result:
                return {"flag":True}
            else:
                return {"flag":False}
        except SQLAlchemyError as e:
            return {"success":False, "message":f"Database error: {str(e)}"}
        
    def insert_new_emp(from_data, EmpID, PasswordHash):

        try:
            sql = text("""
                INSERT INTO employee_details (EmpID, Fullname, Username, Role, PasswordHash)
                VALUES (:EmpID, :Fullname, :Username, :Role, :PasswordHash)
            """)

            db.session.execute(sql, {
                'EmpID': EmpID,
                'Fullname': from_data.get('Fullname'),
                'Username': from_data.get('Username'),
                'Role': from_data.get('Role'),
                'PasswordHash': PasswordHash
            })
            db.session.commit()
            return {"flag" :True, "message":f"User Registration sucessful. Your Registered Employeeid : {EmpID}"}
        except SQLAlchemyError as e:
            app.logger.critical("Database connection failed. Cannot proceed.")

            return {"flag":False, "message":f"Database error: {str(e)}"}

class login_query:
    def login_valid_query(self, login_creds):
        
        try:
            sql = text("SELECT * FROM employee_details WHERE (Username = :Username)")
            query_result = db.session.execute(sql,{
                "Username": login_creds.get('Username'),
            }).fetchone()
            
            if query_result:
                
                return {"flag":True, "user_creds":query_result}
            else:
                return {"flag":False, "message":"Invalid Username ! Try again!"}
        except SQLAlchemyError as e:
            return {"flag":False, "message":f"Database error: {str(e)}"}
        
class version_queries:
    def fetch_version_hist(self):
        try:
            sql = text("SELECT * FROM version_release ORDER BY ReleaseID DESC")
            result = db.session.execute(sql).fetchall()
            
            if result:
                app.logger.info("Data retrival successfull - versin history module")
                return {"flag":True, "data":result}
            else:
                app.logger.warning("Data is not found in the database - version_release for Display all history version records!!")
                return {"flag":False, "message":"Data not found!!"}
        except SQLAlchemyError as e:
            app.logger.critical("Error exception in database - Module(Fetching version History)")
            return {"flag":False, "message":"Error in Database!{e}"}

class preload_data_new_version:
    def fetch_application(self):
        try:
            a_sql = text("SELECT Application FROM applications")
            appl_result = db.session.execute(a_sql).fetchall()
            
            if appl_result:
                return {"flag":True, "appl_data":appl_result}
            else:
                app.logger.warning("No data found in Application Table.")
                return {"flag":False, "message":"Data not found in Application Table!!"}
        
        except SQLAlchemyError as e:
            app.logger.critical(f"Error exception in database retrival in Application table {e}")
            return {"flag":False, "message":"Error in Database!{e}"}
        
    def fetch_modules(self):
        try:
            m_sql = text("SELECT DISTINCT Module FROM modules")
            mod_result = db.session.execute(m_sql).fetchall()
            
            if mod_result:
                return {"flag":True, "mod_data":mod_result}
            else:
                app.logger.warning("No data found in Module Table.")
                return {"flag":False, "message":"Data not found in Module Table!!"}
        
        except SQLAlchemyError as e:
            app.logger.critical(f"Error exception in database retrival in Module table {e}")
            return {"flag":False, "message":"Error in Database!{e}"}
        
    def fetch_submodules(self):
        try:
            m_sql = text("SELECT DISTINCT Submodule FROM modules")
            submod_result = db.session.execute(m_sql).fetchall()
            
            if submod_result:
                return {"flag":True, "submod_data":submod_result}
            else:
                app.logger.warning("No data found in Submodule Table.")
                return {"flag":False, "message":"Data not found in Submodule Table!!"}
        
        except SQLAlchemyError as e:
            app.logger.critical(f"Error exception in database retrival in Submodule table {e}")
            return {"flag":False, "message":"Error in Database!{e}"}
        
class new_release:
    def insert_new_record(self, data):
        try:
            
            sql = text("""
                INSERT INTO version_release (
                    Username, Role, Application, Module, Submodule, ENV, Technology,
                    VersionType, Version, VersionStatus, BugID, TicketID, ReleaseDate, Description
                )
                VALUES (
                    :Username, :Role, :Application, :Module, :Submodule, :ENV, :Technology,
                    :VersionType, :Version, :VersionStatus, :BugID, :TicketID, :ReleaseDate, :Description
                )
            """)

            insert_new_release_result = db.session.execute(sql, {
                'Username': data.get('Username'),
                'Role': data.get('Role'),
                'Application': data.get('Application'),
                'Module': data.get('Module'),
                'Submodule': data.get('Submodule'),
                'ENV': data.get('ENV'),
                'Technology': data.get('Technology'),
                'VersionType': data.get('VersionType'),
                'Version': data.get('Version'),
                'VersionStatus': data.get('VersionStatus'),
                'BugID': data.get('BugID'),
                'TicketID': data.get('TicketID'),
                'ReleaseDate': data.get('ReleaseDate'),
                'Description': data.get('Description')
            })
            db.session.commit()
            if insert_new_release_result.rowcount>0:
                app.logger.info("New Version registered successfully in - version_release table")
                session['VersionStatus'] = data.get('VersionStatus')
                return {"flag":True, "message":"New Version registered successfully."}
            else:
                app.logger.warning("Something is with inserting new version query!")
                return {"flag":False, "message":"Something went wrong in data inserting"}
        except SQLAlchemyError as e:
            app.logger.critical(f"Error execption in database retrival in Submodule table {e}")
            return {"flag":False, "message":"Error in Database!{e}"}

class update_records_query:
    def update_version_record_q(updated_data):
        try:
            u_sql = text("""
                UPDATE version_release
                SET 
                    Version = :Version, 
                    VersionStatus = :VersionStatus, 
                    BugID = :BugID, 
                    TicketID = :TicketID, 
                    ReleaseDate = :ReleaseDate,
                    Description = :Description
                WHERE ReleaseID = :ReleaseID
            """)

            update_record_result = db.session.execute(u_sql, {
                'Version': updated_data.get('Version'),
                'VersionStatus': updated_data.get('VersionStatus'),
                'BugID': updated_data.get('BugID'),
                'TicketID': updated_data.get('TicketID'),
                'ReleaseDate' : updated_data.get('ReleaseDate'),
                'Description': updated_data.get('Description'),
                'ReleaseID': updated_data.get('ReleaseID')  
            })

            db.session.commit()
            if update_record_result:
                return {"flag":True, "message":"Record updated successfully."}
            else:
                return {"flag":False, "message":"Cant Update record!!"}
        except Exception as e:
            db.session.rollback()
            return {"flag":False, "message":"Error in updating record: {e}"}
        
class delete_version_record_query:
    def delete_record_q(ReleaseID):
        try:
            d_sql = text("DELETE FROM version_release WHERE ReleaseID = :ReleaseID")
            delete_record_result = db.session.execute(d_sql,{
                'ReleaseID' : ReleaseID
            })
            db.session.commit()
            
            if delete_record_result.rowcount > 0:
                return True
            else:
                return False
        except SQLAlchemyError as e:
            return {"flag":False, "message":"Error in deleting record: {e}"}