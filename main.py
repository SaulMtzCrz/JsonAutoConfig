import streamlit as st
import json
import pandas as pd

def json_editor(data, path="root", label=None):

    # =========================
    # Diccionario
    # =========================

    if isinstance(data, dict):

        result = {}

        for key, value in data.items():

            current_path = f"{path}.{key}"

            if isinstance(value, dict):

                with st.expander(
                    key,
                    expanded=True
                ):
                    result[key] = json_editor(
                        value,
                        current_path
                    )

            elif isinstance(value, list):

                with st.expander(
                    key,
                    expanded=False
                ):
                    result[key] = json_editor(
                        value,
                        current_path
                    )

            else:

                result[key] = json_editor(
                    value,
                    current_path,
                    label=key
                )

        return result

    # =========================
    # Lista
    # =========================

    elif isinstance(data, list):

        result = []

        for i, value in enumerate(data):

            current_path = f"{path}[{i}]"

            result.append(
                json_editor(
                    value,
                    current_path,
                    label=f"[{i}]"
                )
            )

        return result

    # =========================
    # Boolean
    # =========================

    elif isinstance(data, bool):

        return st.checkbox(
            label,
            value=data,
            key=path
        )

    # =========================
    # Integer
    # =========================

    elif isinstance(data, int):

        return st.number_input(
            label,
            value=data,
            step=1,
            key=path
        )

    # =========================
    # Float
    # =========================

    elif isinstance(data, float):

        return st.number_input(
            label,
            value=data,
            key=path
        )

    # =========================
    # None
    # =========================

    elif data is None:

        st.text_input(
            label,
            value="null",
            disabled=True,
            key=path
        )

        return None

    # =========================
    # String
    # =========================

    else:

        return st.text_input(
            label,
            value=str(data),
            key=path
        )


st.set_page_config(page_title="Conversor Hex a Text", page_icon="🔤", layout="centered")

st.title("🔤 Conversor Hexadecimal a Texto")
st.write("Ingresa una cadena en formato Hexadecimal para obtener su representación en texto.")

#entrada de datos exadecimales
hex_input = st.text_area(
    "Escribe tu comentario",
    value="0800000000000774520000007b224d4f44554c45223a22434f4e4649474d4f44454c222c224f5045524154494f4e223a22474554222c22504152414d45544552223a7b224d445652223a7b224d434d53223a7b224d223a372c225350223a5b7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a35363031342c224353223a226476723030322e62696764617461746d2e696e666f222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a312c2245544c53223a302c224750534558223a342c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a33303030302c224d53223a226d6564613030322e62696764617461746d2e696e666f222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a33373130312c224353223a2233352e3139372e33342e3135222c224354504f5254223a363535362c224355504f5254223a353535362c22454e223a302c2245544c53223a302c224750534558223a342c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a33373130322c224d53223a2233352e3139372e33342e3135222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a33373030302c224353223a22647672312e6e61616e69782e636f6d222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a312c2245544c53223a302c224750534558223a342c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a33373035302c224d53223a2263616d30302e6e61616e69782e636f6d222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a35363031342c224353223a226476723030322e62696764617461746d2e696e666f222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a302c2245544c53223a302c224750534558223a342c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a33303030302c224d53223a226d6564613030322e62696764617461746d2e696e666f222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a35353030332c224353223a2233352e3139372e33342e3135222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a302c2245544c53223a302c224750534558223a302c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a35353030332c224d53223a2233352e3139372e33342e3135222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a353535362c224353223a223139322e3136382e312e35222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a302c2245544c53223a302c224750534558223a302c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a353535362c224d53223a223139322e3136382e312e35222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d5d7d7d7d2c2253455353494f4e223a223030303030303045393041453731383535383733363838393141443344443232227d0a"
    )

# # Opciones de procesamiento
col1, col2 = st.columns(2)
with col1:
    encoding = st.selectbox("Codificación:", ["utf-8", "ascii", "latin-1"])
with col2:
    ignore_errors = st.checkbox("Ignorar errores de bytes irreconocibles", value=False)

if st.button("Convertir a Texto", type="primary"):
    if not hex_input.strip():
        st.warning("Por favor, ingresa una cadena hexadecimal.")
    else:
        # Limpieza básica de la entrada
        cleaned_hex = (
            hex_input.replace("0x", "")
            .replace("\\x", "")
            .replace(" ", "")
            .replace("\n", "")
            .replace(",", "")
            .replace(":", "")
        )
        
        try:
            # Conversión de Hex a Bytes y luego a String
            bytes_data = bytes.fromhex(cleaned_hex)
            errors_strategy = "ignore" if ignore_errors else "strict"
            decoded_text = bytes_data.decode(encoding, errors=errors_strategy)

            #eliminar el header
            posicion = decoded_text.find('{')
            if posicion != -1:
                NewString = decoded_text[posicion:]
            else:
                NewString = decoded_text

            st.text_area("Resultado:", value=NewString, height=120)

            #parsear json
            djson = json.loads(NewString)
            st.json(djson,expanded=False)
                
        except ValueError:
            st.error(" Error de formato: Asegúrate de ingresar una cadena hexadecimal válida (solo caracteres 0-9, A-F y longitud par).")
        except UnicodeDecodeError:
            st.error(f" Error de decodificación: Los bytes no corresponden a texto válido en {encoding}. Intenta marcar 'Ignorar errores' o cambiar la codificación.")