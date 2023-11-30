import httpx
import re
import json
from bs4 import BeautifulSoup as bs

# clase principal del modulo, interactua con el portal cautivo
class nauta():
    # funcion de inicializacion de la clase
    def __init__(self):
    # variables necesarias para el funcionamiento del modulo
        self.close_data = None
        self.data_time = None
        self.attribute_uuid = None
        self.attribute_uuid_patron = None
        self.error = None
        self.errors = None
        self.data_log = None
        self.password = None
        self.username = None
        self.login_dat = None
        self.response = None
        self.soup = None
        self.token_csrf = None
        self.wlanuserip = None
        self.logger_id = None
        # guardamos en cada variable las respectivas urls que utilizaremos
        self.url = 'https://secure.etecsa.net:8443'
        self.url_login = 'https://secure.etecsa.net:8443/LoginServlet'
        self.url_logout = 'https://secure.etecsa.net:8443/LogoutServlet'
        self.url_query = 'https://secure.etecsa.net:8443/EtecsaQueryServlet'
        # headers para que las peticiones http sean correctas
        self.headers = {
            "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64; rv: 117.0.1)"
        }
        # aqui inicializamos la sesion que usaremos a lo largo del uso del modulo
        self.cliente = httpx.Client()
        
    # funcion para verificar si hay conexion con la web de secure.etecsa.net:8443 (El portal cautivo)
    def test_net(self):
        try:
            # intentamos realizar una solicitud http a la url
            self.response = self.cliente.get(self.url, timeout=5)
            # si la solicitud va bien lo parseamos en bs4
            if self.response.status_code == 200:
                self.soup = bs(self.response.content, 'html.parser')
                return True
            else:
                return False
        except httpx.TimeoutException as e:
            print(f'Error: {e}')
            return False
        except httpx.ConnectError as e1:
            print(f'Error: {e1}')
            return False
        
    # funcion para loguearnos en la red
    def login_net(self, username, password):
        try:
            # buscamos parametros necesarios para el inicio de sesion
            self.token_csrf = self.soup.find('input', {'name': 'CSRFHW'}).get('value')
            self.logger_id = self.soup.find('input', {'name': 'loggerId'}).get('value')
            self.wlanuserip = self.soup.find('input', {'name': 'wlanuserip'}).get('value')
            # creamos un diccionario con todos los datos para el login
            self.login_dat = {
                'loggerId': self.logger_id,
                'wlanuserip': self.wlanuserip,
                'CSRFHW': self.token_csrf,
                'username': username,
                'password': password
            }
            # guardamos el usuario y el password en variables para otras peticiones
            self.username = username
            self.password = password
            # enviamos una solicitud POST para iniciar sesion con la informacion adecuada, si hay algun error lo detectamos y aislamos en una variable con expresiones regulares
            self.data_log = self.cliente.post(self.url_login, data=self.login_dat, timeout=5, follow_redirects=True)
            errors = re.compile(r'alert\((.*?)\)')
            error = re.findall(errors, self.data_log.text)
            '''Si no hay errores la pagina nos devolvera una lista con todos los errores posibles
            por ende si hay 12 elementos en la lista no habra ningun error al iniciar sesion
            Aqui verificamos si la longitud de los errores es == 12 y si es True buscamos el dato 
            ATTRIBUTE_UUID necesario para obtener tiempo disponible y cerrar sesion posteriormente.'''
            if len(error) == 12:
                self.attribute_uuid_patron = r'ATTRIBUTE_UUID=([A-F0-9]+)'
                self.attribute_uuid = re.findall(self.attribute_uuid_patron, self.data_log.text)
                self.attribute_uuid = self.attribute_uuid[1]
                 # si todo va bien retornamos True
                return True
            else:
                # si no va bien, retornamos el error
                return error[2]
        except Exception as e:
            return e
        
    # funcion para guardar los datos necesarios para cerrar la sesion en caso de que se cierre el programa
    def save_data(self, ruta):
        try:
            # creamos un diccionario con la estructura necesaria para el cierre de sesion
            datos_para_cerrar = {
                'ATTRIBUTE_UUID': self.attribute_uuid,
                'loggerId': self.logger_id,
                'wlanuserip': self.wlanuserip,
                'CSRFHW': self.token_csrf,
                'username': self.username,
                'password': self.password,
                'remove': 1
            }
            # creamos un fichero json en la ruta especificada y guardamos los datos en el
            with open(ruta, 'w') as archivo:
                json.dump(datos_para_cerrar, archivo)
            # si todo va bien retornamos true
            return True
        except:
            # si hay alguna excepcion retornamos False
            print('El archivo tiene que ser json, y tiene que existir en tu disco duro dentro de el al menos deben haber {} 2 corchetes y ya')
            return False
        
    # funcion para cargar los archivos guardados y los retorna a una variable
    def load_data(self, ruta):
        try:
            # abrimos un archivo que haya sido guardado con la funcion save_data en una ruta especificada por el usuario
            with open(ruta, 'r') as archivo:
                # cargamos la informacion de ese diccionario en una variable
                datos_cargados = json.load(archivo)
            # si todo va bien retornamos esa variable
            return datos_cargados
        except:
            # si hay alguna excepcion retornamos error_cargar_datos
            return 'error_cargar_datos'
        
    # funcion para obtener el tiempo disponible despues de haber iniciado sesion
    def get_time(self):
        # creamos un diccionario con los datos necesarios para obtener el tiempo disponible
        self.data_time = {
            'op': 'getLeftTime',
            'ATTRIBUTE_UUID': self.attribute_uuid,
            'CSRFHW': self.token_csrf,
            'wlanuserip': self.wlanuserip,
            'logger_id': self.logger_id + f' {self.username}',
            'username': self.username
        }
        try:
            # ahora realizamos una solicitud POST a la web de etecsa.query para que devuelva el tiempo disponible
            time = self.cliente.post(self.url_query, data=self.data_time, timeout=5)
            # si todo va bien retornamos el valor del tiempo
            return time.text
        except:
            # si algo va mal retornamos False
            return False
        
    # funcion para cerrar sesion
    def logout(self):
        # creamos un diccionario con los datos necesarios para cerrar la sesion
        close_data = {
            'ATTRIBUTE_UUID': self.attribute_uuid,
            'CSRFHW': self.token_csrf,
            'wlanuserip': self.wlanuserip,
            'loggerId': self.logger_id + f'{self.username}',
            'username': self.username,
            'remove': 1
        }
        try:
            # para cerrar la sesion hacemos una solicitud POST con los datos de cierre y esperar que sea OK
            self.cliente.post(self.url_logout, data=close_data, timeout=5, follow_redirects=True)
            # si todo va bien retornamos True
            return True
        except:
            # si algo va mal retornamos False
            return False
    
    # funcion para cerrar la sesion si el usuario cerro el programa pero se lograron guardar los datos
    def logout_back(self, ruta):
        try:
            # cargamos los datos con la funcion load_data y hacemos la peticion POST con esos datos
            data = self.load_data(ruta)
            self.cliente.post(self.url_logout, data=data, timeout=5, follow_redirects=True)
            # si todo va bien retornamos True
            return True
        except:
            # si algo va mal retornamos False
            return False
        
    '''cuando el usuario cierra el programa sin cerrar sesion y quiere recuperar la sesion,
    podemos hacerlo pero hay que volver a obtener el tiempo restante, esta funcion hace ese
    trabajo'''
    def reanude_login(self, ruta):
        try:
            # cargamos los datos con la funcion load_data
            datos = self.load_data(ruta)
            # borramos estos datos del diccionario ya que no lo necesitamos
            del datos['password']
            del datos['remove']
            # agregamos el dato op que si es necesario
            datos['op'] = 'getLeftTime'
            time = self.cliente.post(self.url_query, data=datos, timeout=5)
            # si todo va bien retornamos el tiempo disponible
            return time.text
        except:
            # si algo va mal retornamos False
            return False

'''# este es un bloque de codigo para ejecutar las funciones del modulo
nauta = nauta()
# nauta.logout_back('d.json')
nauta.test_net()
nauta.test_net()
nauta.login_net('leonel.perez77@nauta.com.cu', 'UpaNvbr8.1212')
import time
nauta.save_data('d.json')
'''


# ya funciona wiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
