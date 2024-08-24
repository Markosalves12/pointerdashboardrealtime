import datetime
import pandas as pd
#
# class Calendar:
#     def __init__(self, dia=1, mes=1, ano=2024):
#         self.dia = dia
#         self.mes = mes
#         self.ano = ano
#
#     def criar_calendario(self):
#         hoje = datetime.date.today()
#         data_inicial = datetime.date(self.ano, self.mes, self.dia)
#
#         datas = [data_inicial + datetime.timedelta(days=i) for i in range((hoje - data_inicial).days + 1)]
#
#         # Create a pandas DataFrame with columns 'Dia', 'Nome do Dia', 'Mês', 'Número do Mês', 'Número do Dia'
#         calendario = pd.DataFrame({
#             'Dia': datas,
#             'Nome do Dia': [data.strftime('%A') for data in datas],
#             'Mês': [data.strftime('%B') for data in datas],
#             'Número do Mês': [data.strftime('%m') for data in datas],
#             'Número do Dia': [data.strftime('%d') for data in datas],
#             'Tipo de Dia': [data.strftime('%A') for data in datas],
#             'Ano': [data.strftime('%Y') for data in datas]
#         })
#
#         return calendario
#
#     def formatar_calendario(self):
#         calendario = self.criar_calendario()
#
#         # Format day names
#         calendario['Nome do Dia'] = calendario['Nome do Dia'].replace({
#             'Sunday': 'Domingo',
#             'Monday': 'Segunda-Feira',
#             'Tuesday': 'Terça-Feira',
#             'Wednesday': 'Quarta-Feira',
#             'Thursday': 'Quinta-Feira',
#             'Friday': 'Sexta-Feira',
#             'Saturday': 'Sábado'
#         })
#
#         # Format month names
#         calendario['Mês'] = calendario['Mês'].replace({
#             'January': 'Janeiro',
#             'February': 'Fevereiro',
#             'March': 'Março',
#             'April': 'Abril',
#             'May': 'Maio',
#             'June': 'Junho',
#             'July': 'Julho',
#             'August': 'Agosto',
#             'September': 'Setembro',
#             'October': 'Outubro',
#             'November': 'Novembro',
#             'December': 'Dezembro'
#         })
#
#         # Determine day type
#         calendario['Tipo de Dia'] = calendario['Tipo de Dia'].replace({
#             'Segunda-Feira': 'Dia Útil',
#             'Terça-Feira': 'Dia Útil',
#             'Quarta-Feira': 'Dia Útil',
#             'Quinta-Feira': 'Dia Útil',
#             'Sexta-Feira': 'Dia Útil',
#             'Domingo': 'Fim de Semana',
#             'Sábado': 'Fim de Semana'
#         })
#
#         # Format date as string
#         calendario['DateTime'] = calendario['Ano'] + "/" + calendario['Número do Mês'] + "/" + calendario['Número do Dia']
#
#         return calendario.astype(str)

class Calendar:
    def __init__(self, dia=1, mes=1, ano=2024, dia_final=None, mes_final=None, ano_final=None):
        self.data_inicial = datetime.date(ano, mes, dia)
        if dia_final is None or mes_final is None or ano_final is None:
            self.data_final = datetime.date.today()
        else:
            self.data_final = datetime.date(ano_final, mes_final, dia_final)

    def criar_calendario(self):
        datas = [self.data_inicial + datetime.timedelta(days=i) for i in range((self.data_final - self.data_inicial).days + 1)]

        # Create a pandas DataFrame with columns 'Dia', 'Nome do Dia', 'Mês', 'Número do Mês', 'Número do Dia'
        calendario = pd.DataFrame({
            'Dia': datas,
            'Nome do Dia': [data.strftime('%A') for data in datas],
            'Mês': [data.strftime('%B') for data in datas],
            'Número do Mês': [data.strftime('%m') for data in datas],
            'Número do Dia': [data.strftime('%d') for data in datas],
            'Tipo de Dia': [data.strftime('%A') for data in datas],
            'Ano': [data.strftime('%Y') for data in datas]
        })

        return calendario

    def formatar_calendario(self):
        calendario = self.criar_calendario()

        # Format day names
        calendario['Nome do Dia'] = calendario['Nome do Dia'].str.replace("Sunday", "Domingo")
        calendario['Nome do Dia'] = calendario['Nome do Dia'].str.replace("Monday", "Segunda-Feira")
        calendario['Nome do Dia'] = calendario['Nome do Dia'].str.replace("Tuesday", "Terça-Feira")
        calendario['Nome do Dia'] = calendario['Nome do Dia'].str.replace("Wednesday", "Quarta-Feira")
        calendario['Nome do Dia'] = calendario['Nome do Dia'].str.replace("Thursday", "Quinta-Feira")
        calendario['Nome do Dia'] = calendario['Nome do Dia'].str.replace("Friday", "Sexta-Feira")
        calendario['Nome do Dia'] = calendario['Nome do Dia'].str.replace("Saturday", "Sábado")

        # Format month names
        calendario['Mês'] = calendario['Mês'].str.replace("January", "Janeiro")
        calendario['Mês'] = calendario['Mês'].str.replace("February", "Fevereiro")
        calendario['Mês'] = calendario['Mês'].str.replace("March", "Março")
        calendario['Mês'] = calendario['Mês'].str.replace("April", "Abril")
        calendario['Mês'] = calendario['Mês'].str.replace("May", "Maio")
        calendario['Mês'] = calendario['Mês'].str.replace("June", "Junho")
        calendario['Mês'] = calendario['Mês'].str.replace("July", "Julho")
        calendario['Mês'] = calendario['Mês'].str.replace("August", "Agosto")
        calendario['Mês'] = calendario['Mês'].str.replace("September", "Setembro")
        calendario['Mês'] = calendario['Mês'].str.replace("October", "Outubro")
        calendario['Mês'] = calendario['Mês'].str.replace("November", "Novembro")
        calendario['Mês'] = calendario['Mês'].str.replace("December", "Dezembro")

        # Determine day type
        calendario['Tipo de Dia'] = calendario['Nome do Dia']
        calendario['Tipo de Dia'] = calendario['Tipo de Dia'].str.replace("Segunda-Feira", "Dia Útil")
        calendario['Tipo de Dia'] = calendario['Tipo de Dia'].str.replace("Terça-Feira", "Dia Útil")
        calendario['Tipo de Dia'] = calendario['Tipo de Dia'].str.replace("Quarta-Feira", "Dia Útil")
        calendario['Tipo de Dia'] = calendario['Tipo de Dia'].str.replace("Quinta-Feira", "Dia Útil")
        calendario['Tipo de Dia'] = calendario['Tipo de Dia'].str.replace("Sexta-Feira", "Dia Útil")
        calendario['Tipo de Dia'] = calendario['Tipo de Dia'].str.replace("Domingo", "Fim de Semana")
        calendario['Tipo de Dia'] = calendario['Tipo de Dia'].str.replace("Sábado", "Fim de Semana")


        # Format date as string
        calendario['DateTime'] = calendario['Ano'] + "/" + calendario['Número do Mês'] + "/" + calendario['Número do Dia']

        return calendario.astype(str)



def datas_unicas_formato_string(dataframe, datas, mes, ano):
    aux_df = dataframe[(dataframe['Mês']==mes) & (dataframe['Ano']==ano)]
    aux_df[datas] = pd.to_datetime(aux_df[datas])
    datas_unicas = aux_df[datas].unique()
    datas_unicas = sorted(datas_unicas)
    datas_formatadas_daily_activities = [data.strftime('%Y/%m/%d') for data in datas_unicas]
    datas_formatadas_rout_history = [data.strftime('%d/%m/%Y') for data in datas_unicas]
    return datas_formatadas_daily_activities, datas_formatadas_rout_history