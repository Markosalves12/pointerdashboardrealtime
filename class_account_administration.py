import requests
import pandas as pd

class AccountAdministration:
    def __init__(self, verify=False, url=str(), rout=str(), token_for_access=str()):
        self.url = url
        self.rout = rout
        self.token_for_access = token_for_access
        self.verify = verify

    # função get accounts testada e funcionando corretamente
    def get_accounts(self, second_rout=str()):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        get_accounts = x.json()

        return get_accounts

    # função get_account apresenta erros, rever a consulta da API
    def get_account(self, second_rout=str()):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        get_account = x.json()

        return get_account

    def get_sub_account(self, second_rout=str()):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        get_sub_account = x.json()

        return get_sub_account

    # função get_vehicle_groups testada e funcionando corretamente
    def get_vehicle_groups(self, second_rout=str()):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        get_vehicle_groups = x.json()

        return get_vehicle_groups





