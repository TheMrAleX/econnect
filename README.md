Bienvenido a la documentación de econnect, un módulo de Python para interactuar con el Portal Cautivo de Etecsa hecho en su totalidad con Python puro, un paquete listo para instalar con `pip install` en tu ordenador, te cuento como hacerlo.

![](https://github.com/TheMrAleX/econnect/blob/main/logo.jpeg?raw=true)

# Introducción
El módulo econnect es una herramienta sencilla y eficaz para gestionar la conexión a la red. En esta guía rápida, te mostraremos cómo utilizarlo en tus proyectos.
# Instalación
Primero, instala el módulo con el siguiente comando:<br>
`pip install econnect`<br>
Luego, impórtalo en tu proyecto de la siguiente manera:<br>
`from enet import econnect`<br>
Ahora que has importado correctamente el módulo, puedes empezar a utilizarlo.
# Uso básico
El módulo econnect proporciona una clase llamada "nauta". Para comenzar a utilizarla, simplemente crea una instancia de la clase de la siguiente manera:<br>
`nauta = econnect.nauta()`<br>
Ahora estás listo para utilizar todos los métodos de la clase.
# Flujo de trabajo
Para un funcionamiento adecuado, sigue estos pasos:<br>
- **Verificación de conexión:** Antes de llamar al método `login_net`, asegúrate de verificar la conexión con el método `test_net`. Esto se hace para validar ciertos parámetros y evitar errores. Aquí tienes un ejemplo de implementación: <br>
```
if nauta.test_net():
    nauta.login_net('usuario@nauta.com.cu', 'password_del_usuario')
```
- **Obtención del tiempo disponible:** Para obtener el tiempo disponible, el usuario debe haber iniciado sesión. Puedes ejecutar el método `get_time` de la misma manera que llamamos a otros métodos. Este método devuelve el tiempo disponible y se recomienda almacenarlo en una variable:<br>
`tiempo_disponible = nauta.get_time()`
- **Guardado de datos:** Puedes guardar los datos de inicio de sesión de forma local para poder tener persistencia de ellos y recordar la sesion si se desea, todo esto con el comando `save_data` y darle como argumento la ruta de un archivo json inicializado con {} 2 corchetes<br>`nauta.save_data('datos.json')`
- **Cierre de sesión:** Para finalizar la sesión, simplemente llama al método `logout`:<br>
`nauta.logout()`
- **Cierre de sesión local:** Si haz guardado los datos de tu sesión con el comando `save_data`, tienes la posibilidad de recuperar la sesión con el comando `logout_back` y darle como argumento la ruta del json con la info de la sesión guardada.<br>`nauta.logout_back('datos.json')`
- **Reanudar sesión:** Me gusta llamar el metodo asi porque visualmente hace eso pero simplemente cuando dejamos la sesión abierta y cerramos el programa la sesión sigue abierta, normalmente los programas solo piden el valor del tiempo disponible y lo muestran con un boton de cerrar, este comando recupera el tiempo disponible con los datos locales por si se cierra el programa con la sesión abierta.<br>`nauta.reanude_login('datos.json'`<br>Si quieres implementar un botón de cerrar puede ser asi:<br>
```
def boton_cerrar():
    if nauta.logout():
        print('cierre exitoso')
    else:
        r = nauta.logout_back('datos.json)
        if r:
            print('cierre con archivo local exitoso')
        else:
            print('cierre fallido')
```
# Lista de métodos
A continuación, se presenta una lista de los métodos disponibles en la clase `nauta`:
- **test_net():** Este método devuelve True o False dependiendo de si la conexión con el Portal Cautivo es exitosa. Debe ejecutarse siempre en primer lugar.
- **login_net():** Este método requiere dos parámetros: el nombre de usuario y la contraseña. Inicia sesión en la red si no hay errores.
- **get_time():** Devuelve el tiempo disponible. Se recomienda almacenarlo en una variable para su posterior uso.
- **save_data('datos.json'):** Guarda los datos necesarios para el cierre de sesión usando archivos locales por si el programa no recupera la sesión, hay que darle un parametro y es la ruta de un .json.
- **logout():** Cierra la sesión.
- **logout_back('datos.json'):** Cierra la sesión con los archivos locales guardados con `save_data`, hay que pasar un argumento de la ruta del json
- **reanude_login('datos.json'):** Obtiene el tiempo disponible para recuperar la sesión con los archivos locales guardados con `save_data` hay que pasar un argumento de la ruta del json

# Información
Módulo de Python 3.12, con las bibliotecas httpx, bs4, json, re, desarrollado por TheMrAleX.<br>La idea surgió en mi cabeza con la pregunta, 'porque no existe un programa suficientemente decente para conectarme a la WiFi en pc', y me plantee hacerlo yo mismo, no sabia nada de programación, empece por Python, llevo muchos meses aprendiendo y me asombra ver de lo que soy capaz, seguire desarrollando proyectos para las 3 personas que visiten este GitHub, proximo proyecto...Una GUI para conectarse a la red Nauta utilizando mi propio modulo...
