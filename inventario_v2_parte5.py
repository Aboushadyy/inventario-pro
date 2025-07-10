import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Historial General", layout="wide")
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

# --- DATOS FICTICIOS PARA DEMO ---
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Código", "Producto", "Stock"])
if "entrada_hist" not in st.session_state:
    st.session_state.entrada_hist = []
if "salida_hist" not in st.session_state:
    st.session_state.salida_hist = []

# --- UNIFICAR HISTORIAL ---
historial_total = []

for entrada in st.session_state.get("entrada_hist", []):
    historial_total.append({
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Tipo": "Entrada",
        "Código": entrada["Código"],
        "Producto": entrada["Producto"],
        "Cantidad": entrada["Cantidad"]
    })

for salida in st.session_state.get("history", []):
    historial_total.append({
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Tipo": "Salida",
        "Código": salida["Código"],
        "Producto": salida["Producto"],
        "Cantidad": salida["Cantidad"]
    })

# --- MOSTRAR HISTORIAL COMBINADO ---
st.title("🧾 Historial General de Movimiento")
if historial_total:
    df_hist = pd.DataFrame(historial_total)
    df_hist = df_hist.sort_values(by="Fecha", ascending=False)
    st.dataframe(df_hist, use_container_width=True)
else:
    st.info("Todavía no hay movimientos registrados.")
