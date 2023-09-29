"""Esta es una libreria de Python hecha para ayudar a los desarrolladores cubanos a interactuar con la red
Nauta de Etecsa, las utilidades son simples, es un cliente para conectarse desde consola a la red, puedes implementarlo
en una GUI si deseas, al fin y al cabo es Open Source:

#Caracteristicas:
-puedes verificar si estas conectado con la funcion 'verify_connection, devuelve True, False dependiendo la conexion'.
-puedes iniciar sesion con la funcion 'loggin_net, hay que darle el usuario y contrasena para que inicie sesion y
retorna True, False en consecuencia si fue exitosa la operacion o no'.
-puedes obtener el tiempo disponible con la funcion 'get_time_remaining', retorna el valor del tiempo disponible y
si hay algun error imprime en consola la excepcion.
-puedes cerrar sesion con la funcion 'close_connection', lo mismo que en get_time_remaining.

#Desarrollado por TheMrAleX"""

import requests
from bs4 import BeautifulSoup as bs
import re


class nauta:
    def __init__(self):
        # variables abajo
        self.close_data = None
        self.data_time = None
        self.attribute_uuid = None
        self.attribute_uuid_patron = None
        self.error = None
        self.errors = None
        self.data_logged = None
        self.password = None
        self.username = None
        self.data_for_login = None
        self.response = None
        self.soup = None
        self.token_csrf = None
        self.wlanuserip = None
        self.logger_id = None
        # variables arriba
        # url que usaremos para trabajar
        self.url = 'https://secure.etecsa.net:8443'
        self.url_login = 'https://secure.etecsa.net:8443/LoginServlet'
        self.url_logout = 'https://secure.etecsa.net:8443/LogoutServlet'
        self.url_query = 'https://secure.etecsa.net:8443/EtecsaQueryServlet'

    def verify_connection(self):
        try:
            # intentamos hacer una peticion POST a la url de Etecsa.
            self.response = requests.get(self.url)
            # Si la peticion va bien lo pasamos por BeautifulSoup y retornamos True.
            if self.response.status_code == 200:
                self.soup = bs(self.response.content, 'html.parser')
                return True
        # Si algo va mal retornamos False.
        except Exception as exception:
            print(f'Error: {exception}')
            return False

    def login_net(self, username, password):
        try:
            # Intentamos buscar parametros necesarios para el inicio de sesion.
            self.token_csrf = self.soup.find('input', {'name': 'CSRFHW'}).get('value')
            self.logger_id = self.soup.find('input', {'name': 'loggerId'}).get('value')
            self.wlanuserip = self.soup.find('input', {'name': 'wlanuserip'}).get('value')
            # Creamos un diccionario con los datos utiles para la solicitud POST que haremos posteriormente para
            # iniciar sesion.
            self.data_for_login = {
                'loggerId': self.logger_id,
                'wlanuserip': self.wlanuserip,
                'CSRFHW': self.token_csrf,
                'username': username,
                'password': password
            }
            self.username = username
            self.password = password

            # Enviamos la solicitud POST con los datos del diccionario y buscamos si hay algun error con 're'
            self.data_logged = requests.post(self.url_login, data=self.data_for_login)
            self.errors = re.compile(r'alert\((.*?)\)')
            self.error = re.findall(self.errors, self.data_logged.text)

            '''Si no hay errores la pagina nos devolvera una lista con todos los errores posibles
            por ende si hay 12 elementos en la lista no habra ningun error al iniciar sesion
            Aqui verificamos si la longitud de los errores es == 12 y si es True buscamos el dato 
            ATTRIBUTE_UUID necesario para obtener tiempo disponible y cerrar sesion posteriormente.'''
            if len(self.error) == 12:
                self.attribute_uuid_patron = r'ATTRIBUTE_UUID=([A-F0-9]+)'
                self.attribute_uuid = re.findall(self.attribute_uuid_patron, self.data_logged.text)
                self.attribute_uuid = self.attribute_uuid[1]

                return True
            else:
                print(f'Error: {self.error}')

        except Exception as e1:
            print(f'Error: {e1}')

    def get_time_remaining(self):
        self.data_time = {
            'op': 'getLeftTime',
            'ATTRIBUTE_UUID': self.attribute_uuid,
            'CSRFHW': self.token_csrf,
            'wlanuserip': self.wlanuserip,
            'logger_id': self.logger_id + f' {self.username}',
            'username': self.username
        }
        try:
            '''Para obtener el tiempo disponible creamos el diccionario de arriba que contiene los datos necesarios
            y hacemos una solicitud POST a la web de etecsa.query para consultar el tiempo disponible.'''
            time_remaining = requests.post(self.url_query, data=self.data_time)
            return time_remaining.text
            # return True
        except Exception as e2:
            print(f'Error al obtener el tiempo de la cuenta: {e2}')

    def close_connection(self):
        self.close_data = {
            'ATTRIBUTE_UUID': self.attribute_uuid,
            'CSRFHW': self.token_csrf,
            'wlanuserip': self.wlanuserip,
            'loggerId': self.logger_id + f'{self.username}',
            'username': self.username,
            'remove': 1
        }
        try:
            # Para cerrar sesion lo mismo que para conseguir el valor de tiempo disponible :).
            requests.post(self.url_logout, data=self.close_data)
            return True
        except Exception as e3:
            print(f'No fue posible cerrar la sesion: {e3}')
            return False


if __name__ == '__main__':
    print('Bienvenido, inicia sesion aqui\n')
    econnect = nauta()

    if econnect.verify_connection():

        while True:
            usernames = input('Usuario: ')
            passwords = input('Password: ')

            if econnect.login_net(usernames, passwords):
                break
            else:
                pass

        print(f'\nTiempo disponible: {econnect.get_time_remaining()}')

        while True:
            try:
                a = int(input('Ingrese #1 para cerrar la sesion: '))
                if a == 1:
                    if econnect.close_connection():
                        print('\nSesion cerrada con exito')
                        break
                    else:
                        print('Ingresa el #1 por favor')
            except ValueError as e:
                print('Ingresa el #1 por favor')
