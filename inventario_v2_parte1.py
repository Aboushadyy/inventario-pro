import streamlit as st
import pandas as pd

# --- LOGIN SIMPLE ---
st.set_page_config(page_title="Inventario Pro", layout="wide")

PASSWORD = "mi_clave_segura"  # Puedes cambiarla por otra clave más segura

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Iniciar sesión")
    password = st.text_input("Contraseña:", type="password")
    if st.button("Entrar"):
        if password == PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ Acceso concedido")
        else:
            st.error("❌ Contraseña incorrecta")
    st.stop()

# --- DATOS INICIALES ---
if "df" not in st.session_state:
    # Estructura vacía: Código, Producto, Stock
    st.session_state.df = pd.DataFrame(columns=["Código", "Producto", "Stock"])

# --- TÍTULO ---
st.title("📦 Inventario Profesional - Parte 1")
st.markdown("Esta es la tabla de productos. Puedes modificarla libremente.")

# --- MOSTRAR TABLA Y PERMITIR EDICIÓN ---
edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    use_container_width=True,
    key="editor"
)

# --- GUARDAR CAMBIOS ---
if st.button("💾 Guardar cambios"):
    st.session_state.df = edited_df.copy()
    st.success("✅ Cambios guardados con éxito")
