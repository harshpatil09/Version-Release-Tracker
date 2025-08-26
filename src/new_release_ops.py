from flask import current_app as app
from jsonschema import validate, ValidationError
from modules.Database import queries

q1 = queries.new_release()

class insert:
    def insert_new_release(self, form_data):
        result = q1.insert_new_record(form_data)
        app.logger.debug("New version registration data is sent for inserting ")
        
        return result["message"]

        
class validation:
    schema = {
        "type": "object",
        "properties": {
            "version": {
                "type": "string",
                "pattern": r"^\d{1,2}\.\d{1,2}\.\d{1,2}$"
            }
        },
        "required": ["version"]
    }

    def new_release_data_validate(self, data):
        try:
            # Ensure matching schema key
            validate(instance={"version": data.get('Version')}, schema=self.schema)
            return {"flag": True, "message": "Validation successful"}
        except ValidationError:
            return {"flag": False, "message": "Invalid Version Format! Try again"}
        