Bienvenido a la documentación de econnect, un programa para interactuar con el Portal Cautivo de Etecsa hecho en su totalidad con Python puro, un paquete listo para instalar con `pip install` en tu ordenador, te cuento como hacerlo.

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
- **Verificación de conexión:** Antes de llamar al método `login_net`, asegúrate de verificar la conexión con el método `verify_connection`. Esto se hace para validar ciertos parámetros y evitar errores. Aquí tienes un ejemplo de implementación: <br>
```
if nauta.verify_connection():
    nauta.login_net('usuario@nauta.com.cu', 'password_del_usuario')
```
- **Obtención del tiempo disponible:** Para obtener el tiempo disponible, el usuario debe haber iniciado sesión. Puedes ejecutar el método `get_time_remaining` de la misma manera que llamamos a otros métodos. Este método devuelve el tiempo disponible y se recomienda almacenarlo en una variable:<br>
`tiempo_disponible = nauta.get_time_remaining()`
- **Cierre de sesión:** Para finalizar la sesión, simplemente llama al método `close_connection`:<br>
`nauta.close_connection()`
# Lista de métodos
A continuación, se presenta una lista de los métodos disponibles en la clase `nauta`:
- **verify_connection():** Este método devuelve True o False dependiendo de si la conexión con el Portal Cautivo es exitosa. Debe ejecutarse siempre en primer lugar.
- **login_net():** Este método requiere dos parámetros: el nombre de usuario y la contraseña. Inicia sesión en la red si no hay errores.
- **get_time_remaining():** Devuelve el tiempo disponible. Se recomienda almacenarlo en una variable para su posterior uso.
- **close_connection():** Cierra la sesión.
