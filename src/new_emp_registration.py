from flask import current_app as app, flash, redirect, url_for
from jsonschema import validate as js_validate, ValidationError
from modules.Database import queries
from werkzeug.security import generate_password_hash
from src import extra
q1 = queries.emp_register_query()

class validate:
    registration_schema = {
        "type": "object",
        "properties": {
            "Username": {
                "type": "string",
                "pattern": r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{3,10}$"
            },
            "Role": {
                "type": "string",
                "enum": ["Developer", "Release Manager", "Manager"]
            },
            "password": {
                "type": "string",
                "minLength": 8,
                "pattern": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"
            },
            "conf_password": {
                "type": "string"
            }
        },
        "required": ["Username", "Role", "password", "conf_password"],
        "additionalProperties": False
    }
    def validate_new_register(self, reg_form_data):
        try:
            js_validate(instance={
                "Username": reg_form_data.get('Username'),
                "Role": reg_form_data.get('Role'),
                "password": reg_form_data.get('PasswordHash'),
                "conf_password": reg_form_data.get('confirm_password')
                }, schema=self.registration_schema)
        except ValidationError as e:
            return {"flag": False, "message": f"Invalid : {e.message}"}
        
        # Additional password match check
        if reg_form_data.get("PasswordHash") != reg_form_data.get("confirm_password"):
            return {"flag": False, "message": "Password does not match"}
        
        # Call your existing username check
        results = q1.unique_username(reg_form_data.get('Username'))
        if not results["flag"]:
            return {"flag": False, "message": results["message"]}
        
        # generated_EmpID = extra.generate_emp.generate_unique_empid()
        
        # hashed_password = generate_password_hash(reg_form_data.get("PasswordHash"))
        return {
                "flag": True, 
                "message":"Regisration successfull"
                # "EmpID": generated_EmpID["EmpID"],
                # "PasswordHash": hashed_password
                }


class insert_data:
    def register_new_emp(reg_form_data):
        
        generated_EmpID = extra.generate_emp.generate_unique_empid()
        
        hashed_password = generate_password_hash(reg_form_data.get("PasswordHash"))
        
        data_insert = queries.emp_register_query.insert_new_emp(reg_form_data, generated_EmpID["EmpID"], hashed_password)
        
        if not data_insert["flag"]:
            return {"flag":False, "message":data_insert["message"]}
        
        return {"flag":True, "message":data_insert["message"]}

        