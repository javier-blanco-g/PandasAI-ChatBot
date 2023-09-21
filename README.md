# PandasAI ChatBot - Javier Blanco

ChatBot creado con Streamlit por Javier Blanco que permite utilizar PandasAI ofreciendo diversas configuraciones para adaptar su funcionamiento según las necesidades del usuario. Estas configuraciones incluyen la capacidad de forzar la privacidad de los datos, un modo de chat conversacional que mantiene el contexto de la conversación, mostrar el código ejecutado y su costo, el almacenamiento en caché para mejorar el tiempo de respuesta, corregir posibles errores de código generados por el LLM, y definir el número máximo de intentos para corregir errores en el código.
![Alt text](/images/ChatBotView.png)
## ¿Cómo uso la aplicación?

La aplicación actualmente es compatible únicamente con los Large Language Models de OpenAI, como Gpt-3 y GPT-4. Para utilizarla, es necesario contar con una API Key de OpenAI. Si es la primera vez que la utilizas y te registras, recibirás un crédito de $5, lo cual es más que suficiente para realizar numerosas pruebas. Una vez que dispongas de la API Key, podrás experimentar con el ChatBot sin necesidad de realizar ninguna instalación en tu ordenador, simplemente a través de Google Colab haciendo click en el siguiente botón:
[![Abrir aplicación en google colab](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/drive/1HcrsiIYKHlXncsfvPNyeddaWbatQaa9e?usp=drive_link)
Una vez te encuentres en Google Colab, simplemente ejecuta la aplicación en su totalidad y sigue las instrucciones proporcionadas en el propio entorno de Google Colab.

<details>
  <summary> <b> Click para tutorial de Google Colab </b></summary>

Google Colab (Colaboratory) es una plataforma en línea gratuita proporcionada por Google que te permite ejecutar y escribir código en Python en un entorno de Jupyter Notebook sin necesidad de configuración o instalación en tu propio ordenador. Esta herramienta te permite ejecutar cuadernos de Jupyter Notebook de forma sencilla a través de un enlace compartido. Sigue estos pasos para aprovecharlo:

### Paso 1: Abre el enlace de Google Colab

1. Al pulsar el boton se abrirá un enlace de Google Colab que te llevará a un cuaderno alojado en Google Colab.

2. Si no tienes una cuenta de Google, crea una cuenta o inicia sesión con tus credenciales.

### Paso 2: Abre el archivo de Google Colab

1. Una vez que hayas iniciado sesión, se abrirá el archivo de Google Colab.

2. Si el archivo no se abre automáticamente, haz clic en "Archivo" en la barra de menú superior y selecciona "Abrir cuaderno".

3. Selecciona el archivo que deseas abrir.

### Paso 3: Ejecuta el código

1. Una vez que el archivo se haya cargado, puedes ejecutar el código haciendo clic en el botón "Ejecutar" en la barra de herramientas superior o presionando "Ctrl + Enter" en tu teclado.

2. Si el archivo requiere permisos adicionales, sigue las instrucciones que se te proporcionen.

Este tutorial te guía a través de los pasos simples para abrir y ejecutar un cuaderno en Google Colab. ¡Disfruta programando en un entorno colaborativo y basado en la nube!

  </details>

<details>
  <summary>
  <b> Click para ver el tutorial sobre cómo obtener una API key de OpenAI</b>
  </summary>

### Paso 1: Crear una cuenta de OpenAI

1. Visita el sitio web de la plataforma OpenAI en [platform.openai.com](https://platform.openai.com).

2. Si no tienes una cuenta, haz clic en "Registrarse" y sigue las instrucciones para crear una.

3. Si ya tienes una cuenta, haz clic en "Iniciar sesión" e ingresa tus credenciales.

### Paso 2: Acceder a la sección de claves API

1. Después de iniciar sesión, haz clic en tu icono de perfil ubicado en la esquina superior derecha de la página.

2. Selecciona "View API Keys" en el menú desplegable.

### Paso 3: Generar una nueva clave API

1. En la sección de claves API, haz clic en el botón "Create new secret key".

2. Se generará una nueva clave API. Asegúrate de copiarla y guardarla en un lugar seguro, ya que no podrás verla de nuevo.

### Paso 4: Usar tu clave API

Ahora que tienes tu clave API, puedes usarla en el ChatBot. Recuerda mantener tu clave API segura y nunca compartirla públicamente ni subirla a un repositorio público.

Para obtener más información sobre cómo usar la API de OpenAI, consulta la [documentación de la API de OpenAI](https://docs.openai.com).

</details>
   <details>
  <summary>
  <b> Click para mas información acerca de las configuraciones de la del ChatBot</b>
  </summary>

- **Forzar la privacidad de los datos**: Si esta desactivado PandasAI enviará una pequeña muestra de los datos al LLM para mejorar la precisión de los resultados. Si se activa solo enviará metadatos, sin datos reales.
- **Hacer el chat conversacional**: Si esta activada los mensajes entre el usuario y el LLM se verán a modo de conversación, adicionalmente estos se enviarán al LLM para que tenga contexto de toda la conversación. Si esta desactivado unicamente se verá una respuesta por parte del LLM y al enviar otro prompt esta última desaparecerá.
- **Mostrar el código ejecutado**: Si está activada, despues de mostrar la respuesta por parte del LLM, se verá un un boton desplegable en el que, cuando hagamos click, podremos ver el coste de la respuesta, el coste acumulativo de la conversació y el coste acumulativo de toda la sesión, es decir, desde que se ejecuto el programa.
- **Mostrar el coste de la operación**: Si está activada, despues de mostrar la respuesta por parte del LLM, se verá un un boton desplegable en el que, cuando hagamos click, podremos ver el código que se ha ejecutado internamente para obtener la respuesta mostrada.
- **Habilitar cache**: Si esta activada se almacenarán los resultados del LLM para mejorar el tiempo de respuesta. Si se desactiva, PandasAI siempre llamará al LLM.
- **Corregir posibles errores de código**: Si esta activada PandasAI intentará corregir los errores en el código generado por el LLM con llamadas posteriores al LLM. Si esta desactivada simplemente se mostrará el error por pantalla.
- **Numero de intentos para corregir errores**: Establece el número máximo de intentos, en el caso de esta la configuración de corregir errores activa, para corregir errores.
</details>
