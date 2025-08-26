from flask import current_app as app
from modules.Database import queries
from werkzeug.security import check_password_hash

q1 = queries.login_query()
class login:
    def login_validation(self, login_creds):
        
        q_result = q1.login_valid_query(login_creds)
        
        if q_result["flag"]:
            
            user_creds = q_result["user_creds"]
            
            if check_password_hash(user_creds.PasswordHash, login_creds.get('PasswordHash')):
                return {"flag":True, "user_creds":user_creds}
            
            else:
                
                return {"flag":False, "message":"Invalid Password"}
        
        return {"flag": False, "message":q_result["message"]}
        

        
         
        