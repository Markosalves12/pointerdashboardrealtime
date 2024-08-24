import pandas as pd
import json
class ConvertAccountAdministration:
    def __init__(self, validation=True):
        self.validation = validation

    def convert_get_accounts(self, json_get_accounts=dict()):
        ids = list()
        external_id = list()
        name = list()

        values = json_get_accounts['Result']['Accounts']

        for value in values:
            ids.append(value['Id'])
            external_id.append(value['ExternalId'])
            name.append(value['Name'])

        convert_get_accounts = pd.DataFrame({'Id': ids, 'ExternalId': external_id, 'Name': name})

        return convert_get_accounts

    def convert_get_vehicle_groups(self, json_get_vehicle_groups=dict()):
        ids = list()
        external_ids = list()
        names = list()

        values = json_get_vehicle_groups['Result']['Groups']

        for value in values:
            ids.append(value['Id'])
            external_ids.append(value['ExternalId'])
            names.append(value['Name'])

        convert_get_vehicle_groups = pd.DataFrame({'Id': ids, 'ExternalId': external_ids, 'Name': names})

        return convert_get_vehicle_groups



