import pandas as pd
from class_time_format import TimeFormat

class ConvertVehicleManagement:
    def __init__(self, validation=True):
        self.validation = validation

    def convert_get_vehicles(self, json_get_vehicles=dict()):
        VehicleId = list()
        ExternalVehicleId = list()
        LicencePlate = list()
        FleetNumber = list()
        FleetAlias = list()
        UnitSysId = list()
        ColorId = list()
        ProducerId = list()
        ModelId = list()
        GroupId = list()
        IconId = list()
        ConfigurationId = list()
        SAList = list()

        values = json_get_vehicles['Result']['Vehicles']

        for value in values:
            VehicleId.append(value['VehicleId'])
            ExternalVehicleId.append(value['ExternalVehicleId'])
            LicencePlate.append(value['LicencePlate'])
            FleetNumber.append(value['FleetNumber'])
            FleetAlias.append(value['FleetAlias'])
            UnitSysId.append(value['UnitSysId'])
            ColorId.append(value['ColorId'])
            ProducerId.append(value['ProducerId'])
            ModelId.append(value['ModelId'])
            GroupId.append(value['GroupId'])
            IconId.append(value['IconId'])
            ConfigurationId.append(value['ConfigurationId'])
            SAList.append(value['SAList'])

        convert_get_vehicles = pd.DataFrame(
            {'VehicleId': VehicleId, 'ExternalVehicleId': ExternalVehicleId, 'LicencePlate': LicencePlate,
             'FleetNumber': FleetNumber, 'FleetAlias': FleetAlias, 'UnitSysId': UnitSysId,
             'ColorId': ColorId, 'ProducerId': ProducerId, 'ModelId': ModelId, 'GroupId': GroupId,
             'IconId': IconId, 'ConfigurationId': ConfigurationId, 'SAList': SAList})

        convert_get_vehicles['LicencePlate'] = convert_get_vehicles['LicencePlate'].str.strip()
        convert_get_vehicles['LicencePlate'] = convert_get_vehicles['LicencePlate'].str.upper()


        return convert_get_vehicles

    def convert_get_fuel_types(self, json_get_fuel_types=dict()):
        Id = list()
        ExternalId = list()
        Name = list()

        values = json_get_fuel_types['Result']['FuelTypes']

        for value in values:
            Id.append(value['Id'])
            ExternalId.append(value['ExternalId'])
            Name.append(value['Name'])

        convert_get_fuel_types = pd.DataFrame({'Id': Id, 'ExternalId': ExternalId, 'Name': Name})

        return convert_get_fuel_types

    def convert_get_vehicles_info(self, json_get_vehicles_info=list()):
        df_arq_cap = list()
        for v in json_get_vehicles_info:
            values = v['Result']
            if len(values) == 0:
                continue

            for key in v['Result'].keys():
                element = v['Result'][key]

                ExternalId, Direction, AccountID, GroupId, AccountName, UnitID = list(), list(), list(), list(), list(), list()
                LicensePlate, FleetAlias, FleetNumber, FuelType, Manufacturer, Model = list(), list(), list(), list(), list(), list()
                Year, VehicleID, LastMessageTime, LastLocationTime, Lat, Long = list(), list(), list(), list(), list(), list()
                Address, Speed, Battery, Ignition, DriverName, Odometer = list(), list(), list(), list(), list(), list()

                for value in element:
                    ExternalId.append(value['ExternalId'])
                    Direction.append(value['Direction'])
                    AccountID.append(value['AccountID'])
                    GroupId.append(value['GroupId'])
                    AccountName.append(value['AccountName'])
                    UnitID.append(value['UnitID'])
                    LicensePlate.append(value['LicensePlate'])
                    FleetAlias.append(value['FleetAlias'])
                    FleetNumber.append(value['FleetNumber'])
                    FuelType.append(value['FuelType'])
                    Manufacturer.append(value['Manufacturer'])
                    Model.append(value['Model'])
                    Year.append(value['Year'])
                    VehicleID.append(value['VehicleID'])
                    LastMessageTime.append(value['LastMessageTime'])
                    LastLocationTime.append(value['LastLocationTime'])
                    Lat.append(value['Lat'])
                    Long.append(value['Long'])
                    Address.append(value['Address'])
                    Speed.append(value['Speed'])
                    Battery.append(value['Battery'])
                    Ignition.append(value['Ignition'])
                    DriverName.append(value['DriverName'])
                    Odometer.append(value['Odometer'])


                auxiliar_df = pd.DataFrame(
                    {'ExternalId': ExternalId, 'Direction': Direction, 'AccountID': AccountID, 'GroupId': GroupId,
                     'AccountName': AccountName, 'UnitID': UnitID, 'Placa': LicensePlate,
                     'FleetAlias': FleetAlias, 'FleetNumber': FleetNumber, 'Combustivel': FuelType,
                     'Manufacturer': Manufacturer, 'Modelo': Model, 'Year': Year, 'VehicleID': VehicleID,
                     'Ultima Menssagem': LastMessageTime, 'LastLocationTime': LastLocationTime, 'Lat': Lat,
                     'Long': Long, 'Endereco': Address, 'Velocidade': Speed, 'Battery': Battery, 'Ignicao': Ignition,
                     'Motorista': DriverName, 'Odometer': Odometer})


                auxiliar_df = auxiliar_df.assign(origin=key)
                df_arq_cap.append(auxiliar_df)

        convert_get_vehicles_info = pd.concat(df_arq_cap)
        convert_get_vehicles_info['Ignicao'] = convert_get_vehicles_info['Ignicao'].replace(0, 'Desligado')
        convert_get_vehicles_info['Ignicao'] = convert_get_vehicles_info['Ignicao'].replace(1, 'Ligado')


        return convert_get_vehicles_info


    def convert_get_daily_activity(self, json_get_daily_activity=dict()):
        df_arq_cap = list()
        for v in json_get_daily_activity:
            values = v['Result']
            if len(values) == 0:
                continue
            ExternalVehicleId = list()
            VehicleId = list()
            LicensePlate = list()
            FleetAlias = list()
            FleetNumber = list()
            GroupId = list()
            DriverName = list()
            DriverId = list()
            ExternalDriverId = list()
            DateTime = list()
            TotalDistance = list()
            MaxSpeed = list()
            AvgSpeed = list()
            NumberOfGeoFences = list()
            IdlingDuration = list()
            ParkingDuration = list()
            DrivingDuration = list()
            HourMeter = list()

            for value in values:
                ExternalVehicleId.append(value['ExternalVehicleId']),
                VehicleId.append(value['VehicleId']),
                LicensePlate.append(value['LicensePlate']),
                FleetAlias.append(value['FleetAlias']),
                FleetNumber.append(value['FleetNumber']),
                GroupId.append(value['GroupId']),
                DriverName.append(value['DriverName']),
                DriverId.append(value['DriverId']),
                ExternalDriverId.append(value['ExternalDriverId']),
                DateTime.append(value['DateTime']),
                TotalDistance.append(value['TotalDistance']),
                MaxSpeed.append(value['MaxSpeed']),
                AvgSpeed.append(value['AvgSpeed']),
                NumberOfGeoFences.append(value['NumberOfGeoFences']),
                IdlingDuration.append(value['IdlingDuration']),
                ParkingDuration.append(value['ParkingDuration']),
                DrivingDuration.append(value['DrivingDuration']),
                HourMeter.append(value['HourMeter']),

                df = pd.DataFrame({'ExternalVehicleId': ExternalVehicleId, 'VehicleId': VehicleId,
                                   'Placa': LicensePlate, 'FleetAlias': FleetAlias,
                                   'FleetNumber': FleetNumber, 'GroupId': GroupId, 'Motorista': DriverName,
                                   'DriverId': DriverId, 'ExternalDriverId': ExternalDriverId,
                                   'Data Hora': DateTime, 'Distancia': TotalDistance, 'Velocidade Maxima': MaxSpeed,
                                   'Velocidade Média': AvgSpeed, 'NumberOfGeoFences': NumberOfGeoFences,
                                   'IdlingDuration': IdlingDuration, 'ParkingDuration': ParkingDuration,
                                   'Tempo de direcao': DrivingDuration, 'HourMeter': HourMeter})

                df_arq_cap.append(df)

        if len(df_arq_cap) > 0:
            df_arq_cap = pd.concat(df_arq_cap)
            df_arq_cap['Tempo de direcao'] = df_arq_cap['Tempo de direcao'].str.strip()
            df_arq_cap['Segundos de direcao'] = TimeFormat(df_arq_cap['Tempo de direcao']).converte_hh_mm_ss_to_seconds()

            df_arq_cap['Data Hora'] = pd.to_datetime(df_arq_cap['Data Hora'], format='%d/%m/%Y')
            df_arq_cap['dia'] = df_arq_cap['Data Hora'].dt.day
            df_arq_cap['Data Hora'] = df_arq_cap['Data Hora'].dt.strftime('%d/%m/%Y')

            return df_arq_cap

        else:
            df_arq_cap = pd.DataFrame({'ExternalVehicleId': [], 'VehicleId': [],
                          'Placa': [], 'FleetAlias': [],
                          'FleetNumber': [], 'GroupId': [], 'Motorista': [],
                          'DriverId': [], 'ExternalDriverId': [],
                          'Data Hora': [], 'Distancia': [], 'Velocidade Maxima': [],
                          'Velocidade Media': [], 'NumberOfGeoFences': [],
                          'IdlingDuration': [], 'ParkingDuration':[] ,
                          'Tempo de direcao': [], 'HourMeter': []})


            return df_arq_cap

    def convert_get_rout_history(self, list_of_json=list()):
        DriverId = list()
        DateTime = list()
        TxReason = list()
        GroupId = list()
        UnitID = list()
        LicensePlate = list()
        VehicleID = list()
        Lat = list()
        Long = list()
        Address = list()
        Speed = list()
        Ignition = list()
        DriverName = list()


        for json in list_of_json:
            values = json['Result']
            for value in values:
                DriverId.append(value['DriverId'])
                DateTime.append(value['DateTime'])
                TxReason.append(value['TxReason'])
                GroupId.append(value['GroupId'])
                UnitID.append(value['UnitID'])
                LicensePlate.append(value['LicensePlate'])
                VehicleID.append(value['VehicleID'])
                Lat.append(value['Lat'])
                Long.append(value['Long'])
                Address.append(value['Address'])
                Speed.append(value['Speed'])
                Ignition.append(value['Ignition'])
                DriverName.append(value['DriverName'])

        GetVehicleRouteHistoryInfo = pd.DataFrame({'DriverId': DriverId, 'Data Hora': DateTime,
                                                   'Tipo de sinal': TxReason,
                                                   'GroupId': GroupId, 'UnitID': UnitID,
                                                   'Placa': LicensePlate,
                                                   'VehicleID': VehicleID, 'Lat': Lat,
                                                   'Long': Long, 'Endereco': Address,
                                                   'Velocidade': Speed, 'Ignicao': Ignition,
                                                   'Motorista': DriverName}).drop_duplicates()


        GetVehicleRouteHistoryInfo = GetVehicleRouteHistoryInfo[(GetVehicleRouteHistoryInfo['Lat'] != 0)
                                                                & (GetVehicleRouteHistoryInfo['Long'] != 0)]


        GetVehicleRouteHistoryInfo['Data Hora'] = pd.to_datetime(GetVehicleRouteHistoryInfo['Data Hora'], format='%d/%m/%Y %H:%M:%S')
        GetVehicleRouteHistoryInfo['Hora'] = GetVehicleRouteHistoryInfo['Data Hora'].dt.hour
        GetVehicleRouteHistoryInfo['Data Hora'] = GetVehicleRouteHistoryInfo['Data Hora'].dt.strftime('%d/%m/%Y %H:%M:%S')

        GetVehicleRouteHistoryInfo['DriverId'] = GetVehicleRouteHistoryInfo['DriverId'].astype(str)
        GetVehicleRouteHistoryInfo['DriverId'] = GetVehicleRouteHistoryInfo['DriverId'].str.strip()
        GetVehicleRouteHistoryInfo['DriverId'] = GetVehicleRouteHistoryInfo['DriverId'].str.replace(".0","")

        GetVehicleRouteHistoryInfo['Ignicao'] = GetVehicleRouteHistoryInfo['Ignicao'].replace(0, 'Desligado')
        GetVehicleRouteHistoryInfo['Ignicao'] = GetVehicleRouteHistoryInfo['Ignicao'].replace(1, 'Ligado')


        return GetVehicleRouteHistoryInfo