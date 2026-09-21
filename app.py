import streamlit as st
import json
import pandas as pd

DEFAULT_NESTED_JSON = {
    "empresa": "ExampleCorp",
    "activo": True,
    "servidores": [
        {
            "id": "SRV-01",
            "ip": "192.168.1.10",
            "configuracion": {
                "so": "Linux",
                "puertos_abiertos": [80, 443, 8080],
                "recursos": {"cpu_cores": 8, "ram_gb": 32}
            }
        },
        {
            "id": "SRV-02",
            "ip": "192.168.1.11",
            "configuracion": {
                "so": "Windows Server",
                "puertos_abiertos": [3389, 445],
                "recursos": {"cpu_cores": 16, "ram_gb": 64}
            }
        }
    ],
    "contacto": {
        "admin": {"nombre": "Saúl", "email": "admin@techcorp.com"},
        "soporte": {"telefono": "+52 555 000 0000"}
    }
}

st.set_page_config(page_title="Editor Json")
example_hex = "0800000000000774520000007b224d4f44554c45223a22434f4e4649474d4f44454c222c224f5045524154494f4e223a22474554222c22504152414d45544552223a7b224d445652223a7b224d434d53223a7b224d223a372c225350223a5b7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a35363031342c224353223a226476723030322e62696764617461746d2e696e666f222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a312c2245544c53223a302c224750534558223a342c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a33303030302c224d53223a226d6564613030322e62696764617461746d2e696e666f222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a33373130312c224353223a2233352e3139372e33342e3135222c224354504f5254223a363535362c224355504f5254223a353535362c22454e223a302c2245544c53223a302c224750534558223a342c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a33373130322c224d53223a2233352e3139372e33342e3135222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a33373030302c224353223a22647672312e6e61616e69782e636f6d222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a312c2245544c53223a302c224750534558223a342c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a33373035302c224d53223a2263616d30302e6e61616e69782e636f6d222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a35363031342c224353223a226476723030322e62696764617461746d2e696e666f222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a302c2245544c53223a302c224750534558223a342c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a33303030302c224d53223a226d6564613030322e62696764617461746d2e696e666f222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a35353030332c224353223a2233352e3139372e33342e3135222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a302c2245544c53223a302c224750534558223a302c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a35353030332c224d53223a2233352e3139372e33342e3135222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d2c7b2243414d54223a302c2243415354223a342c224350223a302c2243504f5254223a353535362c224353223a223139322e3136382e312e35222c224354504f5254223a363535362c224355504f5254223a363232322c22454e223a302c2245544c53223a302c224750534558223a302c2247505353223a302c224c474b223a302c224c504f5254223a353036352c224d504f5254223a353535362c224d53223a223139322e3136382e312e35222c224d54504f5254223a363535362c224d55504f5254223a363131312c224e4242223a312c224e5754223a302c22525546223a302c22534950505744223a22222c225349505245414c4d223a22222c22534950534944223a22222c22534950554944223a22222c22534b50223a307d5d7d7d7d2c2253455353494f4e223a223030303030303045393041453731383535383733363838393141443344443232227d0a"

def initSystem():
    #inicializar variables
    if "inputHex" not in st.session_state:
        st.session_state.inputHex = ""
    if "json_data" not in st.session_state:
        st.session_state.json_data = DEFAULT_NESTED_JSON
    if "current_path" not in st.session_state:
        st.session_state.current_path = []

def parseHexToJson(hex_string):
    try:
        # Convertir el HEX a bytes
        bytes_data = bytes.fromhex(hex_string)
        decode_text = bytes_data.decode('utf-8')

        #retirar el header si existe, buscando el primer '{' y tomando desde ahí
        pos = decode_text.find('{')
        if pos != -1:
            decode_text = decode_text[pos:]

        # Intentar decodificar los bytes a UTF-8 y luego cargarlo como JSON
        json_data = json.loads(decode_text)
        return json_data
    except Exception as e:
        st.error(f"Error al convertir HEX a JSON: {e}")
        return None

def dashboard():
    st.sidebar.header("⚙️ Configuración & Carga")
    fuente = st.sidebar.radio("Fuente:",["Pegar HEX","Pegar Json"])

    if fuente == "Pegar HEX":
        # col1,col2 = st.sidebar.columns(2)
        # checkHedaer = col1.checkbox("Nivel Header",value=True)
        # valueHeader = col2.number_input("Valor Header:",value=12)

        raw_text = st.sidebar.text_area("Pega tu HEX aquí:", height=180,value=example_hex)
        if st.sidebar.button("Validar HEX",type="primary"):
            try:
                #limpiar el input de HEX y guardarlo en la variable de sesión
                cleaned_hex = (
                    raw_text.replace("0x", "")
                    .replace("\\x", "")
                    .replace(" ", "")
                    .replace("\n", "")
                    .replace(",", "")
                    .replace(":", "")
                )
                #intentar parsear el HEX a JSON y guardarlo en la variable de sesión
                st.session_state.json_data = parseHexToJson(cleaned_hex)
                st.session_state.current_path = []
                # st.session_state.inputHex = raw_text
                #st.toast("HEX cargado correctamente", icon="✅")
                st.sidebar.success("HEX cargado correctamente", icon="✅")
            except Exception as e:
                st.sidebar.error(f"HEX inválido: {e}")

    elif fuente == "Pegar Json":
        raw_text = st.sidebar.text_area("Pega tu JSON aquí:", height=180)
        if st.sidebar.button("Validar JSON",type="primary"):
            try:
                st.session_state.json_data = json.loads(raw_text)
                st.session_state.current_path = []
                st.sidebar.success("JSON cargado correctamente", icon="✅")
            except Exception as e:
                st.sidebar.error(f"JSON inválido: {e}")

    # puerto = st.sidebar.text_input("Puerto:",label_visibility="collapsed",value="8080")
    # address = st.sidebar.text_input("Dirección IP:",label_visibility="collapsed",value="0.0.0.0")

    #pestañas de visualización y edición
    tab_arbol,tab_navegador,tab_editor = st.tabs([
    "🌳 Vista Árbol",
    "🔍 Navegador de Nodos",
    "✏️ Editor de JSON"
    ])

    #pestaña 1: arbol colapsable
    with tab_arbol:
        col_a,col_b = st.columns([3,1])
        with col_b:
            profundidad = st.number_input("Nivel de expansión:",min_value=1,max_value=10,value=2)
        with col_a:
            st.subheader("Estructura completa actual")
            st.json(st.session_state.json_data,expanded=profundidad)
    #pestaña 2: navegador de nodos
    with tab_navegador:

        st.subheader("Selecciona el nodo que deseas inspeccionar o editar")
        st.caption("Navega por las claves/listas para enfocar una sección del JSON.")
    
        curr_level = st.session_state.json_data
        path = []
    
        for level in range(5):
            if isinstance(curr_level, dict):
                keys = list(curr_level.keys())
                selected_key = st.selectbox(
                    f"Nivel {level + 1} (Clave):", 
                    options=["-- Seleccionar nodo --"] + keys,
                    key=f"node_level_{level}"
                )
                if selected_key != "-- Seleccionar nodo --":
                    curr_level = curr_level[selected_key]
                    path.append(selected_key)
                else:
                    break
            elif isinstance(curr_level, list):
                indices = [f"Elemento [{i}]" for i in range(len(curr_level))]
                selected_idx = st.selectbox(
                    f"Nivel {level + 1} (Lista de {len(curr_level)} ítems):", 
                    options=["-- Seleccionar elemento --"] + indices,
                    key=f"node_level_{level}"
                )
                if selected_idx != "-- Seleccionar elemento --":
                    idx = int(selected_idx.split("[")[1].split("]")[0])
                    curr_level = curr_level[idx]
                    path.append(idx)
                else:
                    break
            else:
                break

        # Guardar ruta en session_state para compartirla con la pestaña de edición
        st.session_state.current_path = path

        st.divider()
        if path:
            ruta_str = "root -> " + " -> ".join([str(p) for p in path])
            st.success(f"📍 **Ruta seleccionada:** `{ruta_str}`")
        else:
            st.info("📍 **Ruta seleccionada:** `root` (Raíz del JSON)")
            
        st.json(curr_level)
    
    #pestaña 3 Editor del nodo seleccionado
    with tab_editor:
        path = st.session_state.current_path

        #obtener el sub-nodo objetivo siguiendo la ruta activa
        tarjet_node = st.session_state.json_data
        for p in path:
            tarjet_node = tarjet_node[p]
        
        ruta_str = "root" if not path else "root -> " + " -> ".join([str(p) for p in path])
        st.subheader(f"Editando: '{ruta_str}'")

        #convertir el sub-nodo a dataframe para st.data_editor
        try:
            if isinstance(tarjet_node,list):
                #si es lista de objeros o primitivos
                if len(tarjet_node) > 0 and isinstance(tarjet_node[0],dict):
                    df_node = pd.json_normalize(tarjet_node)
                else:
                    df_node = pd.DataFrame(tarjet_node,columns=["valor"])
            elif isinstance(tarjet_node,dict):
                #si es un objeto/diccionario, se edita como clave/valor
                df_node = pd.DataFrame(list(tarjet_node.items()),columns=["Clave","Valor"])
                is_dic_mode = True
            else:
                df_node = None
                
        except Exception as e:
            st.error("No se puede renderizar este nivel en formato de tablas: {e}")

def main():
    initSystem()
    dashboard()

if __name__ == "__main__":
    main()