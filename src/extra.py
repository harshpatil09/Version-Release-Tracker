import random
from modules.Database import queries
from flask import flash
q1 = queries.emp_register_query()
class generate_emp:
    

    def generate_unique_empid():
        for _ in range(10):  
            new_id = f"EMP{random.randint(1, 999):03}"
            result = q1.unique_empid_query(new_id)
            if result:
                return {"EmpID":new_id}
        return None  
