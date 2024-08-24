import requests
from class_multiple_requisition import MultipleRequisition

class VehicleManagement:
    def __init__(self, url, rout, token_for_access, verify=False):
        self.url = url
        self.rout = rout
        self.token_for_access = token_for_access
        self.verify = verify

    def get_vehicles(self, second_rout):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        get_vehicles = x.json()

        return get_vehicles


    def get_fuel_types(self, second_rout):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        get_fuel_types = x.json()

        return get_fuel_types


    def get_vehicles_type(self, second_rout):
        url_for_requisition = self.url+self.rout+second_rout+self.token_for_access
        x = requests.get(url_for_requisition, verify=self.verify)
        get_vehicles_type = x.json()

        return get_vehicles_type


    def get_daily_activity(self, second_rout, licenseplate, vehicleids, dates):
        url_for_requisitions = list()

        for date in dates:
            url_for_requisition = (self.url+self.rout+second_rout+self.token_for_access+
                                   "&StartDate="+date+"&EndDate="+date+"&LicensePlate="
                                   +licenseplate+"&VehicleIds="+vehicleids)
            url_for_requisitions.append(url_for_requisition)

        requisitions = MultipleRequisition(url_for_requisitions)
        list_of_json = requisitions.make_requisitions()

        return list_of_json

    def get_route_history(self, second_rout, licenseplate, vehicleids, dates, hour1 = int(), hour2=int()):
        url_for_requisitions = list()
        if hour1 < 9:
            hour1 = f'0{hour1}'
        else:
            hour1 = f'{hour1}'

        if hour2 < 9:
            hour2 = f'0{hour2}'
        else:
            hour2 = f'{hour2}'


        for date in dates:
            url_for_requisition = (self.url+self.rout+second_rout+self.token_for_access+
                                   "&StartDate="+date+f" {hour1}:00:00&EndDate="+date+
                                   f" {hour2}:59:59&LicensePlate="+licenseplate+"&VehicleIds="+vehicleids)
            url_for_requisitions.append(url_for_requisition)


        requisitions = MultipleRequisition(url_for_requisitions)
        list_of_json = requisitions.make_requisitions()

        return list_of_json

    def get_vehicle_info(self, second_rout, licenseplate, vehicleids):
        url_for_requisitions = list()
        for position in range(0, len(vehicleids)):
            url_for_requisition = (self.url+self.rout+second_rout+self.token_for_access+
                                   "&LicensePlates="+licenseplate[position]+"&VehicleIds="+vehicleids[position])
            url_for_requisitions.append(url_for_requisition)

        requisitions = MultipleRequisition(url_for_requisitions)
        list_of_json = requisitions.make_requisitions()

        return list_of_json

