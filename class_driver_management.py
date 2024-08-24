import requests
import pandas as pd

class DriverManagement:
    def __init__(self, url, rout, token_for_access, verify=False):
        self.url = url
        self.rout = rout
        self.token_for_access = token_for_access
        self.verify = verify

    #função get_drivers testada e funcionando corretamente
    def get_drivers(self, second_rout):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        drivers_management = x.json()

        return drivers_management

    #função get_drivers_management testada e funcionado corretamente
    def get_driver_group(self, second_rout):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        driver_group = x.json()

        return driver_group
