from flask import current_app as app
from modules.Database import queries
class update_version_record:
    def update_version(self,updated_data):
        if updated_data:
           u_result = queries.update_records_query.update_version_record_q(updated_data)
           if u_result["flag"]:
               return {"flag":True}
           else:
               return {"flag":False}
           