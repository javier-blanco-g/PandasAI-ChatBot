# Importar las bibliotecas necesarias
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai.callbacks import BaseCallback
from pandasai.helpers.openai_info import get_openai_callback
import streamlit as st
import pandas as pd
import os
import re
from CustomPrompt import CustomGeneratePythonCodePrompt
from datetime import datetime

# Variable y callback para guardar el ultimo codigo ejecutado
class SaveLastCodeGeneratedCallback(BaseCallback):
    def on_code(self, response: str):
        # Elimina líneas que contengan únicamente comentarios y líneas vacías
        clean_code = re.sub(r'#.*$', '', response, flags=re.MULTILINE)
        clean_code = re.sub(r'(""".*?""")|(\'\'\'.*?\'\'\')',
                            '', clean_code, flags=re.DOTALL)
        clean_code = "\n".join(
            [line for line in clean_code.splitlines() if line.strip()])
        st.session_state["last_code_generated"] = clean_code


CHARTS_RELATIVE_PATH = "exports/charts/"
# Definir un diccionario de formatos de archivo y las funciones para leerlos
file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}
# Define a dictionary of OpenAI models
models = {
    # "GPT-3": "gpt-3.5-turbo-instruct",
    "GPT-3": "gpt-3.5-turbo",
    "GPT-4": "gpt-4",
    # Han sido deprecados en versiones posteriores de la libreria
    # "HF-Starcoder": "Starcoder",
    # "HF-Falcon": "Falcon",
}


# Limpiar el estado, generar mensaje incial del asistente y borrar graficos
def clear_chat_state():
    st.session_state["messages"] = [
        {"role": "assistant", "content": "¿En qué puedo ayudarte?"}]
    st.session_state["last_code_generated"] = ""
    st.session_state["submit"] = False
    st.session_state["total_cost_conversation"] = 0.0
    # Elimina el contenido de la carpeta de los gráficos
    if os.path.exists(CHARTS_RELATIVE_PATH) and os.path.isdir(CHARTS_RELATIVE_PATH):
        for chart in os.listdir(CHARTS_RELATIVE_PATH):
            ruta_completa = os.path.join(CHARTS_RELATIVE_PATH, chart)
            try:
                if os.path.isfile(ruta_completa):
                    os.remove(ruta_completa)
                    print(f'Archivo eliminado: {ruta_completa}')
            except Exception as e:
                print(f'Ocurrió un error al eliminar {ruta_completa}: {str(e)}')

# Pregunta a pandas y recibe el coste de la llamada OpenAI API
def ask_pandasai(chat_messages) -> (str, float):
    with get_openai_callback() as cb:
        respuesta = sdf.chat(chat_messages)
        return respuesta, cb.total_cost

# Mostrar el código  ejecutado
def show_code_expander(code: str):
    if config_show_executed_code:
        with st.expander("Código ejecutado."):
            st.code(code, language="python")

# Muestra el componente que permite ver los costes
def get_cost_info(cost: float) -> str:
    print(cost)
    new_total_cost_session = float(
        st.session_state["total_cost_session"]) + float(cost)
    new_total_cost_conversation = float(
        st.session_state["total_cost_conversation"]) + float(cost)
    st.session_state["total_cost_session"] = new_total_cost_session
    st.session_state["total_cost_conversation"] = new_total_cost_conversation
    return (
        f"Coste de la respuesta: {str(cost)}$ \n" +
        f"Coste total de la conversación: {str(new_total_cost_conversation)}$ \n" +
        f"Coste total de la sesion: {str(new_total_cost_session)}$ \n"
    )


# Mostrar el coste de la operación
def show_cost_expander(cost_info: float):
    if config_show_operation_cost:
        with st.expander("Información del gasto económico."):
            st.text(cost_info)

# Muestra y guarda las graficas generados del assistente
def show_chart_image(chart_full_name: str):
    saved_chart_name = ""
    chart_path = CHARTS_RELATIVE_PATH+chart_full_name
    if chart_full_name == "temp_chart.png":
        current_datetime = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
        # Crear el nuevo nombre de archivo con la fecha y hora actual
        saved_chart_name = f'{current_datetime}.png'
        # Renombrar el archivo
        try:
            new_path_and_name = CHARTS_RELATIVE_PATH+saved_chart_name
            os.rename(chart_path, new_path_and_name)
            chart_path = new_path_and_name
            print(f'El archivo ha sido renombrado a: {saved_chart_name}')
        except FileNotFoundError:
            print(f'El archivo {chart_path} no existe.')
        except Exception as e:
            print(f'Ocurrió un error al renombrar el archivo: {str(e)}')

    st.image(chart_path, caption='Grafico respuesta',
             use_column_width=True,)
    return saved_chart_name


# Función para cargar datos desde un archivo
@st.cache_data(ttl="2h")
def load_data(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except:
        ext = uploaded_file.split(".")[-1]
    if ext in file_formats:
        return file_formats[ext](uploaded_file)
    else:
        st.error(f"Formato de archivo no admitido: {ext}")
        return None


if "total_cost_session" not in st.session_state:
    st.session_state["total_cost_session"] = 0.0

if "total_cost_conversation" not in st.session_state:
    st.session_state["total_cost_conversation"] = 0.0

# Configurar la página de la aplicación
st.set_page_config(page_title="TFM", page_icon="🐼")
st.subheader("LLM como herramienta de análisis de datos.")
# Permitir a los usuarios cargar un archivo de datos
uploaded_file = st.file_uploader(
    "Cargar un archivo de datos",
    type=list(file_formats.keys()),
    help="Se admiten varios formatos de archivo",
    on_change=clear_chat_state,
)

# Si se ha cargado un archivo, cargarlo como un DataFrame de Pandas
if uploaded_file:
    df = load_data(uploaded_file)

# Contenido de la barra lateral con instrucciones y descripción de la aplicación
with st.sidebar:
    model = st.selectbox(
        "Seleccione el LLM:", options=list(models.keys()), on_change=clear_chat_state)
    if model == "GPT-4":
        openai_use_gpt4_url = "https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4#:~:text=For%20API%20accounts%20created%20after%20August%2018%2C%202023%2C%20you%20can%20get%20instant%20access%20to%20GPT%2D4%20after%20purchasing%20%240.50%20worth%20or%20more%20of%20pre%2Dpaid%20credits.%20You%20can%20read%20about%20prepaid%20billing%20here."
        st.warning(
            f"Para poder usar GPT-4 has de haber realizado un pago mínimo de $0.5 en la [API]({openai_use_gpt4_url}). 🚨")

    with st.sidebar.form(key="config"):
        # Solicitar al usuario que ingrese su clave de API de OpenAI en la barra lateral
        is_openai_model = model in ["GPT-4", "GPT-3"]
        text_model = "OpenAI" if is_openai_model else "HuggingFace"
        openai_signup_url = f"https://platform.openai.com/signup"
        openai_find_APIKey_url = "https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key"
        api_key = st.text_input(f"Clave de API de {text_model}",
                                value="",
                                type="password",
                                placeholder=f"Pegue su clave de API de {text_model} aquí (sk-...)",
                                help=f"Para obtener la API Key de OpenAI primero regístrese en su [pagina web]({openai_signup_url}) y una vez registrado siga los pasos indicados en el siguiente [enlace]({openai_find_APIKey_url})"
                                )
        config_data_description = st.text_area("Introduzca una descripción de los datos (Opcional)",
                                               height=1,
                                               placeholder="Descripción (Opcional)",
                                               help="Es recomendable describir el conjunto de datos para obtener mejores resultados, sobre todo si la opción de forzar privacidad esta activada")
        with st.expander("Opciones avanzadas"):
            config_enforce_privacy = st.checkbox(
                label="Forzar la privacidad de los datos",
                help="Si esta desactivado PandasAI enviará una pequeña muestra de los datos al LLM para mejorar la precisión de los resultados. Si se activa solo enviará metadatos, sin datos reales.",
                value=False)
            config_conversational = st.checkbox(
                label="Hacer el chat conversacional",
                help="Si esta activada los mensajes entre el usuario y el LLM se verán a modo de conversación, adicionalmente estos se enviarán al LLM para que tenga contexto de toda la conversación. Si esta desactivado unicamente se verá una respuesta por parte del LLM y al enviar otro prompt esta última desaparecerá.",
                value=True)
            config_show_executed_code = st.checkbox(
                label="Mostrar el código ejecutado",
                help="Si está activada, despues de mostrar la respuesta por parte del LLM, se verá un un boton desplegable en el que, cuando hagamos click, podremos ver el coste de la respuesta, el coste acumulativo de la conversació y el coste acumulativo de toda la sesión, es decir, desde que se ejecuto el programa.",
                value=True)
            config_show_operation_cost = st.checkbox(
                label="Mostrar el coste de la operación",
                help="Si está activada, despues de mostrar la respuesta por parte del LLM, se verá un un boton desplegable en el que, cuando hagamos click, podremos ver el código que se ha ejecutado internamente para obtener la respuesta mostrada.",
                value=is_openai_model, disabled=(not is_openai_model))
            config_enable_cache = st.checkbox(
                label="Habilitar cache",
                help="Si esta activada se almacenarán los resultados del LLM para mejorar el tiempo de respuesta. Si se desactiva, PandasAI siempre llamará al LLM.",
                value=True)
            config_use_error_correction_framework = st.checkbox(
                label="Corregir posibles errores de código",
                help="Si esta activada PandasAI intentará corregir los errores en el código generado por el LLM con llamadas posteriores al LLM. Si esta desactivada simplemente se mostrará el error por pantalla.",
                value=True)
            config_error_correction_max_retries = st.number_input(
                min_value=1, max_value=5, value=3,
                label="Numero de intentos para corregir errores",
                help="Establece el número máximo de intentos, en el caso de esta la configuración de corregir errores activa, para corregir errores.")

        col1 = st.columns([2, 1])

        with col1[0]:
            st.form_submit_button(on_click=clear_chat_state,
                                  label="Aplicar configuración")
        with col1[1]:
            st.text(body="", help="Al cambiar la configuración pulse este botón para aplicarla. Una vez pulsado adicionalmente se borrará la conservasación actual.")

# Si no existe la clave "messages" en el estado de la sesión, inicializarla con un mensaje del asistente
if "messages" not in st.session_state or st.sidebar.button("Borrar historial de conversación", help="Al pulsarse borrará la conservasación actual.") or not config_conversational:
    clear_chat_state()

# Mostrar el historial de conversación en la interfaz de usuario
for msg in st.session_state.messages:
    if msg["role"] == "assistant_code":
        show_code_expander(msg["content"])
    elif msg["role"] == "assistant_cost":
        show_cost_expander(msg["content"])
    elif msg["role"] == "assistant_chart":
        st.chat_message("assistant").write("Aquí tienes el gráfico:")
        show_chart_image(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

chat_input_msg = "Envia un mensaje" if uploaded_file else "Carge primero los datos"
# Permitir al usuario ingresar una pregunta
if prompt := st.chat_input(placeholder=chat_input_msg, disabled=not uploaded_file):
    if not config_conversational:
        clear_chat_state()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Verificar si se ha proporcionado una clave de API de OpenAI
    if not api_key:
        st.info(f"Agregue su clave de API de {text_model} para continuar.")
        st.stop()

    llm = OpenAI(api_token=api_key, model=models[model])

    # Crear un objeto SmartDataframe usando el DataFrame cargado y la configuración
    sdf = SmartDataframe(df, config={"llm": llm,
                                     "custom_prompts": {"generate_python_code": CustomGeneratePythonCodePrompt()},
                                     "enable_cache": config_enable_cache,
                                     "enforce_privacy":  config_enforce_privacy,
                                     "conversational": config_conversational,
                                     "save_charts_path":  CHARTS_RELATIVE_PATH,
                                     "save_charts": False,
                                     "save_logs": True,
                                     "use_error_correction_framework": config_use_error_correction_framework,
                                     "max_retries": config_error_correction_max_retries,
                                     "callback": SaveLastCodeGeneratedCallback()})
    sdf._table_description = config_data_description
    # Generar una respuesta basada en la pregunta del usuario y mostrarla
    with st.chat_message("assistant"):
        messages = []
        for msg in st.session_state.messages:
            if msg['role'] in ["assistant", "user"]:
                messages.append(msg)
            elif msg['role'] == "assistant_code":
                msg['role'] = "assistant"
                messages.append(msg)
        with st.spinner("Cargando..."):
            response, cost = ask_pandasai(messages)
            if response == None:
                st.write("Aquí tienes el gráfico:")
                saved_chart_name = show_chart_image("temp_chart.png")
                st.session_state.messages.append(
                    {"role": "assistant_chart", "content": saved_chart_name})
            else:
                st.session_state.messages.append(
                    {"role": "assistant", "content": response})
                st.write(response)
            # Mostrar el código  ejecutado
            if config_show_executed_code:
                executed_code = st.session_state["last_code_generated"]
                # executed_code = "Code"
                st.session_state.messages.append(
                    {"role": "assistant_code", "content": executed_code})
                show_code_expander(executed_code)
            # Mostrar el coste de la operación
            if config_show_operation_cost:
                cost_info = get_cost_info(cost)
                st.session_state.messages.append(
                    {"role": "assistant_cost", "content": str(cost_info)})
                show_cost_expander(cost_info)
            print("============================================")
            print("PROMPT ENVIADO AL LLM")
            print(sdf.last_prompt)
