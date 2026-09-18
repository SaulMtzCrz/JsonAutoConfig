import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Inspector y Editor de JSON Anidados", page_icon="🌳", layout="wide")

st.title("🌳 Inspector y Editor de JSONs Anidados")

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

# Inicializar estado de sesión
if "json_data" not in st.session_state:
    st.session_state.json_data = DEFAULT_NESTED_JSON

# Variable global de sesión para rastrear la ruta elegida en el navegador
if "current_path" not in st.session_state:
    st.session_state.current_path = []

# ---------------------------------------------------------
# Sidebar: Carga y Exportación
# ---------------------------------------------------------
st.sidebar.header("⚙️ Configuración & Carga")
fuente = st.sidebar.radio("Fuente:", ["Ejemplo Anidado", "Pegar JSON", "Subir Archivo"])

if fuente == "Pegar JSON":
    raw_text = st.sidebar.text_area("Pega tu JSON aquí:", height=180)
    if st.sidebar.button("Cargar JSON"):
        try:
            st.session_state.json_data = json.loads(raw_text)
            st.session_state.current_path = []
            st.toast("JSON cargado correctamente", icon="✅")
        except Exception as e:
            st.sidebar.error(f"JSON inválido: {e}")
elif fuente == "Subir Archivo":
    file = st.sidebar.file_uploader("Archivo .json", type=["json"])
    if file:
        st.session_state.json_data = json.load(file)

st.sidebar.divider()
st.sidebar.subheader("💾 Exportar JSON Completo")
json_export = json.dumps(st.session_state.json_data, indent=2, ensure_ascii=False)
st.sidebar.download_button(
    "Descargar JSON Modificado",
    data=json_export,
    file_name="json_actualizado.json",
    mime="application/json",
    type="primary"
)

# ---------------------------------------------------------
# Pestañas de Visualización y Edición
# ---------------------------------------------------------
tab_arbol, tab_navegador, tab_editor = st.tabs([
    "🌳 Vista Árbol", 
    "🔍 Navegador de Nodos", 
    "📝 Editor del Nodo Seleccionado"
])

# --- Pestaña 1: Árbol Colapsable ---
with tab_arbol:
    col_a, col_b = st.columns([3, 1])
    with col_b:
        profundidad = st.number_input("Nivel de expansión:", min_value=1, max_value=10, value=2)
    with col_a:
        st.subheader("Estructura completa actual")
        st.json(st.session_state.json_data, expanded=profundidad)

# --- Pestaña 2: Navegación de Nodos (Define la ruta a editar) ---
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

# --- Pestaña 3: Editor del Nodo Seleccionado ---
with tab_editor:
    path = st.session_state.current_path
    
    # 1. Obtener el sub-nodo objetivo siguiendo la ruta activa
    target_node = st.session_state.json_data
    for p in path:
        target_node = target_node[p]

    ruta_str = "root" if not path else "root -> " + " -> ".join([str(p) for p in path])
    st.subheader(f"📝 Editando: `{ruta_str}`")
    
    # 2. Convertir el sub-nodo a DataFrame para st.data_editor
    try:
        if isinstance(target_node, list):
            # Si es lista de objetos o primitivos
            if len(target_node) > 0 and isinstance(target_node[0], dict):
                df_node = pd.json_normalize(target_node)
            else:
                df_node = pd.DataFrame(target_node, columns=["Valor"])
            is_dict_mode = False
        elif isinstance(target_node, dict):
            # Si es un objeto/diccionario, se edita como Clave/Valor
            df_node = pd.DataFrame(list(target_node.items()), columns=["Clave", "Valor"])
            is_dict_mode = True
        else:
            df_node = None

        if df_node is not None:
            st.caption("Doble clic sobre cualquier celda para modificar sus datos:")
            
            # Editor interactivo
            edited_df = st.data_editor(
                df_node, 
                num_rows="dynamic" if not is_dict_mode else "fixed", 
                use_container_width=True,
                key=f"editor_{hash(tuple(path))}"
            )
            
            # Botón para confirmar y reinyectar los cambios en el JSON principal
            if st.button("💾 Guardar cambios en este nodo", type="primary"):
                # Reconstruir los datos editados al tipo de dato original
                if is_dict_mode:
                    updated_data = dict(zip(edited_df["Clave"], edited_df["Valor"]))
                else:
                    if "Valor" in edited_df.columns and len(edited_df.columns) == 1:
                        updated_data = edited_df["Valor"].tolist()
                    else:
                        updated_data = edited_df.to_dict(orient="records")

                # Reinyectar el nodo actualizado en el JSON de session_state
                if not path:
                    st.session_state.json_data = updated_data
                else:
                    ref = st.session_state.json_data
                    for p in path[:-1]:
                        ref = ref[p]
                    ref[path[-1]] = updated_data

                st.success("¡Nodo actualizado con éxito!")
                st.toast("Estructura JSON global actualizada", icon="✅")
                st.rerun()

        else:
            st.warning("El nodo seleccionado es un valor primario (texto, número o booleano). Selecciona una clave que sea un Diccionario o Lista en la pestaña 'Navegador de Nodos' para editarla como tabla.")

    except Exception as e:
        st.error(f"No se pudo renderizar este nivel en formato de tabla: {e}")