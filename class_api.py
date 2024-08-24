import requests

class ApiPointer:
    def __init__(self, url, user_name, password, verify=False):
        self.url = url
        self.user_name = user_name
        self.password = password
        self.verify = verify

    # função login testada e funcionando, retornando o token de acesso corretamente
    def login(self, rout):
        url_for_requisition = self.url+rout+f"username={self.user_name}&password={self.password}"
        x = requests.get(url_for_requisition, verify=self.verify)
        y = x.json()
        token = y['Result']['Token']

        return token


