from datetime import datetime, time

class TimeFormat:
    def __init__(self, times):
        self.times = times

    # def converte_hh_mm_ss_to_seconds(self):
    #     segundos_totais = self.times.apply(lambda x: time.strptime(x, '%H:%M:%S').second +
    #                                                    time.strptime(x, '%H:%M:%S').minute * 60 +
    #                                                    time.strptime(x, '%H:%M:%S').hour * 3600)
    #     return segundos_totais

    def converte_hh_mm_ss_to_seconds(self):
        tempos_em_segundos = []
        for tempo in self.times:
            horas, minutos, segundos = map(int, tempo.split(':'))
            total_segundos = horas * 3600 + minutos * 60 + segundos
            tempos_em_segundos.append(total_segundos)

        return tempos_em_segundos

def converte_to_seconds__hh_mm_ss(seconds):
    horas = seconds // 3600
    minutos = (seconds % 3600) // 60
    segundos = seconds % 60

    return f'{horas:02d}:{minutos:02d}:{segundos:02d}'

