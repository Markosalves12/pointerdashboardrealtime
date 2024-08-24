# import email, smtplib, ssl
#
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# subject = "An email with attachment from Python"
# body = "This is an email with attachment sent from Python"
# sender_email = "markosapereira@gmail.com"
# receiver_email = "markosapereira@gmail.com"
# password = "velpnahununuevlh"
#
# # Create a multipart message and set headers
# message = MIMEMultipart()
# message["From"] = sender_email
# message["To"] = receiver_email
# message["Subject"] = subject
# message["Bcc"] = receiver_email  # Recommended for mass emails
#
# # Add body to email
# message.attach(MIMEText(body, "plain"))
#
# filename = "class_send_email.py"  # In same directory as script
#
# # Open PDF file in binary mode
# with open(filename, "rb") as attachment:
#     # Add file as application/octet-stream
#     # Email client can usually download this automatically as attachment
#     part = MIMEBase("application", "octet-stream")
#     part.set_payload(attachment.read())
#
# # Encode file in ASCII characters to send by email
# encoders.encode_base64(part)
#
# # Add header as key/value pair to attachment part
# part.add_header(
#     "Content-Disposition",
#     f"attachment; filename= {filename}",
# )
#
# # Add attachment to message and convert message to string
# message.attach(part)
# text = message.as_string()
#
# # Log in to server using secure context and send email
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, text)

import random
import string
from routs import senha_smtp, email_smtp
# from Back_End.Class_Image.class_image import Image
import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from dash import html

class SendEmail:
    def __init__(self, para, de=email_smtp):
        self.de = de
        self.para = para

    def create_codigo(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        random_code = ''.join(random.choice(characters) for _ in range(15))
        return random_code

    codigo = 0
    def create_mensagem(self):
        global codigo
        codigo = self.create_codigo()
        # mensagem = html.Div(
        #     [
        #         html.Div(
        #             [
        #                 html.Iframe(
        #                     srcDoc=Image(path_svg=".\logo facilities.svg").open_image(),
        #                     style={'display': 'block', 'margin': 'auto'},
        #                     width=f"100%", height=f"110%"
        #                 ),
        #                 html.H4('Código de verificação do sistema de telemetria',
        #                         style={'text-align': 'center', 'font-weight': 'bold'}),
        #                 html.H6('O código é:', style={'text-align': 'center'}),
        #                 html.H2(f'{codigo}', style={'text-align': 'center', 'font-weight': 'bold'}),
        #             ]
        #         )
        #     ]
        # )

        html = f"""<!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Código de Verificação</title>
        </head>
        <body>
            <div style="text-align: center;">
                 <p style="font-size: 25px; color: #003366; font-family: Arial, sans-serif; font-weight: bold;">Facilities Suzano</p>
            </div>
            <div style="margin-top: 20px; text-align: center;">
                <h2 style="font-size: 18px; color: #000; font-family: Arial, sans-serif;">Código de verificação do sistema de telemetria</h2>
                <p style="font-size: 15px; color: #000; font-family: Arial, sans-serif;">O código é:</p>
                <p style="font-size: 25px; color: #003366; font-family: Arial, sans-serif; font-weight: bold;">{codigo}</p>
            </div>
        </body>
        </html>"""

        return html

    def send_email(self):
        global codigo
        mensagem = MIMEMultipart()
        mensagem['Subject'] = "Código de verifição"
        mensagem['From'] = self.de
        mensagem['To'] = self.para
        mensagem['Body'] = self.create_mensagem()
        mensagem.attach(MIMEText(mensagem['Body'], 'html'))


        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=contexto) as servidor:
            servidor.login(mensagem['From'], password=senha_smtp)
            servidor.sendmail(
                mensagem['From'], mensagem['To'], mensagem.as_string()
            )

        return codigo


