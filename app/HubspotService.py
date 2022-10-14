import requests
import json

class HubspotCompaniesService():

    def __init__(self,access_token: str) -> None:
        
        self.access_token = access_token
        self.base_url = 'https://api.hubapi.com/crm/v3'

    def _make_request_(self, path, data):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        url = self.base_url + path

        data = json.dumps(data)

        return requests.post(url,data,headers=headers)


    def merge_companies(self,primary_object_id: int, object_id_to_merge: int):
        path = "/objects/companies/merge"

        data = {
            "primaryObjectId": int(primary_object_id),
            "objectIdToMerge": int(object_id_to_merge)
        }
        
        
        response = self._make_request_(path,data)

        return response

