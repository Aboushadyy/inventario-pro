import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Inventario Pro", layout="wide")
PASSWORD = "mi_clave_segura"

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

# --- INICIALIZACIÓN DE DATOS ---
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Código", "Producto", "Stock"])
if "entrada_hist" not in st.session_state:
    st.session_state.entrada_hist = []

st.title("📥 Inventario - Parte 4: Entradas")
st.markdown("Usa este panel para registrar **entradas** de productos al inventario.")

# --- SELECCIÓN DE PRODUCTO ---
if not st.session_state.df.empty:
    codigos = st.session_state.df["Código"].tolist()
    selected_code = st.selectbox("Selecciona un código para sumar:", codigos)
    producto_row = st.session_state.df[st.session_state.df["Código"] == selected_code].iloc[0]
    st.markdown(f"**Producto:** {producto_row['Producto']}")
    st.markdown(f"**Stock actual:** {producto_row['Stock']} unidades")

    qty = st.number_input("¿Cuántas unidades entraron?", min_value=1, step=1)
    if st.button("➕ Registrar entrada"):
        idx = st.session_state.df[st.session_state.df["Código"] == selected_code].index[0]
        st.session_state.df.at[idx, "Stock"] += qty
        st.session_state.entrada_hist.append({
            "Código": selected_code,
            "Producto": producto_row["Producto"],
            "Cantidad":
