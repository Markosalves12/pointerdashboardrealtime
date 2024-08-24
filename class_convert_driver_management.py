import pandas as pd
class ConvertDriverManagement:
    def __init__(self, validation=True):
        self.validation = validation

    def convert_get_drivers(self, json_get_drivers):
        ids = list()
        external_driver_id = list()
        fisrt_name = list()
        middle_name = list()
        last_name = list()
        group_id = list()
        subacount_id = list()
        subacount_name = list()
        ex_subacount_id = list()
        ex_subacount_name = list()
        owner = list()

        values = json_get_drivers['Result']['Drivers']

        for value in values:
            ids.append(value['Id'])
            external_driver_id.append(value['ExternalDriverId'])
            fisrt_name.append(value['FirstName'])
            middle_name.append(value['MiddleName'])
            last_name.append(value['LastName'])
            group_id.append(value['GroupId'])
            owner.append(value['Owner'])

            try:
                subacount_id.append(value['Subaccount']['Id'])
            except:
                subacount_id.append('')

            try:
                subacount_name.append(value['Subaccount']['Name'])
            except:
                subacount_name.append('')

            try:
                ex_subacount_id.append(value['EXSubaccount']['Id'])
            except:
                ex_subacount_id.append('')

            try:
                ex_subacount_name.append(value['EXSubaccount']['Name'])
            except:
                ex_subacount_name.append('')

        convert_get_drivers = pd.DataFrame({'Id': ids, 'ExternalDriverId': external_driver_id,
                                            'FirstName': fisrt_name, 'MiddleName': middle_name,
                                            'LastName': last_name, 'GroupId': group_id,
                                            'Subaccount_id': subacount_id,
                                            'Subaccount_name': subacount_name,
                                            'EXSubaccount_id': ex_subacount_id,
                                            'EXSubaccount_name': ex_subacount_name,
                                            'Owner': owner})

        convert_get_drivers['Nome Motorista'] = (convert_get_drivers['FirstName'] + ' '
                                                 + convert_get_drivers['MiddleName']
                                                 + ' ' + convert_get_drivers['LastName'])
        convert_get_drivers['Nome Motorista'] = convert_get_drivers['Nome Motorista'].astype(str)
        for i in range(0,10):
            convert_get_drivers['Nome Motorista'] = convert_get_drivers['Nome Motorista'].replace(f"{i}","")

        convert_get_drivers['Nome Motorista'] = convert_get_drivers['Nome Motorista'].str.title()
        convert_get_drivers['Nome Motorista'] = convert_get_drivers['Nome Motorista'].str.strip()

        convert_get_drivers['Id'] = convert_get_drivers['Id'].astype(str)
        convert_get_drivers['Id'] = convert_get_drivers['Id'].str.strip()

        return convert_get_drivers

    def convert_get_driver_group(self, json_get_driver_group):
        ids = list()
        names = list()
        description = list()
        is_default = list()

        values = json_get_driver_group['Result']['Groups']

        for value in values:
            ids.append(value['Id'])
            names.append(value['Name'])
            description.append(value['Description'])
            is_default.append(value['IsDefault'])

        convert_get_driver_group = pd.DataFrame({'Id': ids, 'Name': names, 'Description': description,
                                     'IsDefault': is_default})

        return convert_get_driver_group