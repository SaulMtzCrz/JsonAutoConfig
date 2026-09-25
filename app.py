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
example_hex = ""

def initSystem():
    #inicializar variables
    if "inputHex" not in st.session_state:
        st.session_state.inputHex = ""
    if "json_data" not in st.session_state:
        st.session_state.json_data = DEFAULT_NESTED_JSON
    if "current_path" not in st.session_state:
        st.session_state.current_path = []
    if "checks" not in st.session_state:
        st.session_state.checks = []
    if "texto_user" not in st.session_state:
        st.session_state.texto_user = ""
    # if "text_usuario" not in st.session_state:
    #     st.session_state.texto_usuario_a = json.dumps(
    #         DEFAULT_NESTED_JSON,
    #         ensure_ascii=False,
    #         separators=(",", ":")
    #     )

def escapar_comillas():
    texto = st.session_state.texto_user

    # Escapar solamente las comillas que todavía no tienen \
    resultado = ""
    i = 0

    while i < len(texto):
        if texto[i] == '"':
            # Si la comilla anterior ya es \, no volver a escaparla
            if i > 0 and texto[i - 1] == '\\':
                resultado += '"'
            else:
                resultado += '\\"'
        else:
            resultado += texto[i]

        i += 1

    st.session_state.texto_user = resultado

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

def filtrarJson(data,claves_permitidas):
    if isinstance(data, dict):
        nuevo_dict = {}
        for k, v in data.items():
            if k in claves_permitidas:
                # Si la clave coincide, la conservamos tal cual
                nuevo_dict[k] = v
            else:
                # Si no coincide, exploramos si dentro hay diccionarios/listas que contengan la clave
                val_filtrado = filtrarJson(v, claves_permitidas)
                # Mantener solo si el sub-objeto resultante no está vacío
                if val_filtrado:
                    nuevo_dict[k] = val_filtrado
        return nuevo_dict

    elif isinstance(data, list):
        # Filtrar cada elemento de la lista y omitir elementos vacíos
        lista_filtrada = [filtrarJson(item, claves_permitidas) for item in data]
        return [item for item in lista_filtrada if item]

    # Primitivos que no coincidan con las claves buscadas se descartan
    return None

def update_json_text():
    st.session_state.texto_user = json.dumps(
        st.session_state.json_data,
        ensure_ascii=False,
        separators=(",", ":")
    )

def dashboard():
    st.sidebar.header("⚙️ Configuración & Carga")
    fuente = st.sidebar.radio("Fuente:",["Pegar HEX","Pegar Json"])
    if fuente == "Pegar HEX":
        # col1,col2 = st.sidebar.columns(2)
        # checkHedaer = col1.checkbox("Nivel Header",value=True)
        # valueHeader = col2.number_input("Valor Header:",value=12)

        raw_text = st.sidebar.text_area("Pega tu HEX aquí:", height=180)

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
    tab_arbol,tab_navegador,tab_editor,editor = st.tabs([
    "🌳 Vista Árbol",
    "🔍 Navegador de Nodos",
    "✏️ Editor de JSON",
    "🔖 Editor txt"
    ])

    #pestaña 1: arbol colapsable
    with tab_arbol:
        col_a,col_b = st.columns([3,1])
        with col_b:
            profundidad = st.number_input("Nivel de expansión:",min_value=1,max_value=10,value=2)
            st.download_button(
                "Descargar JSON",
                data=json.dumps(st.session_state.json_data,separators=(',',':'),ensure_ascii=False),
                file_name="json_actualizado.txt",
                mime="application/json",
                type="primary"
            )
        with col_a:
            st.subheader("Estructura completa actual")
            st.json(st.session_state.json_data,expanded=profundidad)

    #pestaña 2: navegador de nodos
    with tab_navegador:
        st.subheader("Selecciona el nodo que deseas inspeccionar o editar")
        st.caption("Navega por las claves/listas para enfocar una sección del JSON.")
        curr_level = st.session_state.json_data
        path = []
        for level in range(10):
            if isinstance(curr_level, dict):
                keys = list(curr_level.keys())
                st.session_state.checks.clear()
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

        # Guardar ruta en session_state para compartirla con la pestaña de edición
        st.session_state.current_path = path
        st.divider()

        if path:
            ruta_str = "root -> " + " -> ".join([str(p) for p in path])
            st.success(f"📍 **Ruta seleccionada:** `{ruta_str}`")
        else:
            st.info("📍 **Ruta seleccionada:** `root` (Raíz del JSON)")
            
        st.write("### contenido del nodo seleccionado:")
        claves = None
        
        #manejo seguro segun el tipo de dato:
        if isinstance(curr_level,(dict,list)):
            col1,col2 = st.columns([2,1])
            with col1:
                st.json(curr_level)
                if isinstance(curr_level,dict):
                    claves = list(curr_level.keys())
            with col2:
                st.session_state.checks.clear() #borrar la lista de checks antes de llenarla con los nuevos
                #Encontrar la manera de borrar el check de las casillas cuando se regresa a root
                #ya que si se selecciona en niveles mas abajo al momento de regresar mantiene los checks seleccionados
                #pero si me voy regresando de nivel en nivel si se borra
                if claves:
                    for i,clave in enumerate(claves):
                        st.session_state.checks.append((clave,st.checkbox(clave,value=False,key=f"check_{i}")))
        else:
            #muestra limpia para valores simples como string int float bool etc
            col1,col2 = st.columns([1,2])
            with col1:
                st.info(f"**Tipo de dato:** `{type(curr_level).__name__}`")
            with col2:
                st.success(f"**valor:** `{curr_level}`")

    # --- Pestaña 3: Editor del Nodo Seleccionado ---
    with tab_editor:
        #for clave, checked in checks:
            #print(f"Checkbox {clave}: {'checked' if checked else 'unchecked'}")

        #clave actual seleccionada en el navegador de nodos
        path = st.session_state.current_path
        claves_seleccionados = []
        # 1. Obtener la referencia al nodo objetivo siguiendo la ruta activa
        target_node = st.session_state.json_data
        for p in path:
            target_node = target_node[p]
            #print(f"Ruta actual: {path}, Nodo objetivo: {target_node}")

        ruta_str = "root" if not path else "root -> " + " -> ".join([str(p) for p in path])
        st.subheader(f"Editando: `{ruta_str}`")
        
        if isinstance(target_node, (dict, list)): 
            try:
                #1 intenta solo reccorer el nodo actual y no todo el json para esta prueba
                print("###########################")
                for clave, checked in st.session_state.checks:
                    # print(f"Checkbox {clave}: {'checked' if checked else 'unchecked'}")
                    #print(f"Valor del nodo actual: {clave} : {target_node.get(clave, 'No existe la clave')} = {'checked' if checked else 'unchecked'}")
                    if checked:
                        claves_seleccionados.append(clave)
                        print(f"Checkbox {clave} está marcado. Valor actual: {target_node.get(clave, 'No existe la clave')}")

                if isinstance(target_node, list):#[]
                    # Si es lista de objetos o de elementos simples
                    if len(target_node) > 0 and isinstance(target_node[0], dict):
                        df_node = pd.json_normalize(target_node)
                    else:
                        df_node = pd.DataFrame(target_node, columns=["valor"])
                    is_dict_mode = False
                else:
                    # Si es un objeto/diccionario, se edita como Clave/Valor
                    json_active = filtrarJson(target_node,claves_seleccionados)
                    df_node = pd.DataFrame(list(json_active.items()), columns=["Clave", "Valor"])
                    #para editar la tabla conviene pasarlo todo a string ya que si hay dos tipos de dato la tabla no se podrá editar
                    df_node["Valor"] = df_node["Valor"].astype(str) 
                    is_dict_mode = True

                st.caption("Doble clic en cualquier celda para modificar los datos:")
                
                edited_df = st.data_editor(
                    df_node, 
                    num_rows="dynamic" if not is_dict_mode else "fixed", 
                    width='stretch',
                    key=f"editor_{hash(tuple(path))}"
                )
                
                if st.button("Guardar cambios en esta tabla", type="primary"):
                    if is_dict_mode:
                        updated_data = {}
                        for _, row in edited_df.iterrows():
                            clave = row["Clave"]
                            valor = row["Valor"]

                            # Recuperar tipo básico
                            if isinstance(valor, str):
                                if valor.lower() == "true":
                                    valor = True
                                elif valor.lower() == "false":
                                    valor = False
                                elif valor.lower() == "null":
                                    valor = None
                                else:
                                    try:
                                        valor = int(valor)
                                    except ValueError:
                                        try:
                                            valor = float(valor)
                                        except ValueError:
                                            pass
                            
                            updated_data[clave] = valor
                    else:
                        if "Valor" in edited_df.columns and len(edited_df.columns) == 1:
                            updated_data = edited_df["Valor"].tolist()
                        else:
                            updated_data = edited_df.to_dict(orient="records")

                    # Guardar en el JSON principal
                    if not path:
                        if is_dict_mode:
                            st.session_state.json_data.update(updated_data)
                        else:
                            st.session_state.json_data = updated_data
                    else:
                        ref = st.session_state.json_data

                        for p in path[:-1]:
                            ref = ref[p]

                        if is_dict_mode:
                            ref[path[-1]].update(updated_data)
                        else:
                            ref[path[-1]] = updated_data

                    st.success("¡Nodo actualizado correctamente!")
                    st.rerun()

            except Exception as e:
                st.error(f"Error al renderizar la tabla: {e}")

        else:
            st.info(f"El nodo seleccionado es un valor de tipo **{type(target_node).__name__}**.")
            
            # Renderizar el widget adecuado según el tipo de dato
            nuevo_valor = target_node
            
            if isinstance(target_node, bool):
                nuevo_valor = st.toggle("Valor booleano:", value=target_node)
                
            elif isinstance(target_node, int):
                nuevo_valor = st.number_input("Valor entero:", value=int(target_node), step=1)
                
            elif isinstance(target_node, float):
                nuevo_valor = st.number_input("Valor decimal:", value=float(target_node), format="%.4f")
                
            elif isinstance(target_node, str):
                # Si el texto es largo, usamos text_area; si es corto, text_input
                if len(target_node) > 60:
                    nuevo_valor = st.text_area("Valor de texto:", value=target_node, height=120)
                else:
                    nuevo_valor = st.text_input("Valor de texto:", value=target_node)
                    
            elif target_node is None:
                st.warning("El valor actual es `None` / `null`.")
                nuevo_valor = st.text_input("Asignar nuevo valor de texto:", value="")

            # Botón para confirmar el cambio del valor simple
            if st.button("Guardar valor", type="primary"):
                if not path:
                    st.session_state.json_data = nuevo_valor
                else:
                    ref = st.session_state.json_data
                    for p in path[:-1]:
                        ref = ref[p]
                    ref[path[-1]] = nuevo_valor

                st.success(f"¡Valor actualizado a `{nuevo_valor}`!")
                st.rerun()

    # --- Pestaña 4: Editor txt del arbol completo
    with editor:
        st.subheader("Editor libre")

        edit_json = st.text_area(
            label="Editar JSON directamente",
            height=250,
            key="texto_user"
        )

        col1,col2,col3 = st.columns(3)

        with col1:
            st.button("update JSON",type="primary",on_click=update_json_text)
                
        with col2:
            st.button("formatear JSON",type="primary",on_click=escapar_comillas)
        
def main():
    initSystem()
    dashboard()

if __name__ == "__main__":
    main()