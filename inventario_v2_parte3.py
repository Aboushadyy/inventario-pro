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

# --- DATOS INICIALES ---
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Código", "Producto", "Stock"])
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📦 Inventario Profesional - Parte 3")
st.markdown("Descuenta productos del inventario fácilmente.")

# --- SELECCIÓN DE PRODUCTO ---
if not st.session_state.df.empty:
    codigos = st.session_state.df["Código"].tolist()
    selected_code = st.selectbox("Selecciona un código para descontar:", codigos)
    producto_row = st.session_state.df[st.session_state.df["Código"] == selected_code].iloc[0]
    st.markdown(f"**Producto:** {producto_row['Producto']}")
    st.markdown(f"**Stock actual:** {producto_row['Stock']} unidades")

    qty = st.number_input("¿Cuántas unidades salieron?", min_value=1, step=1)
    if st.button("➖ Registrar salida"):
        idx = st.session_state.df[st.session_state.df["Código"] == selected_code].index[0]
        stock_actual = st.session_state.df.at[idx, "Stock"]
        if qty > stock_actual:
            st.error("❌ No hay suficiente stock.")
        else:
            st.session_state.df.at[idx, "Stock"] -= qty
            st.session_state.history.append({
                "Código": selected_code,
                "Producto": producto_row["Producto"],
                "Cantidad": qty
            })
            st.success(f"✅ Se descontaron {qty} unidades de {producto_row['Producto']}")
else:
    st.warning("No hay productos en el inventario aún.")

# --- HISTORIAL DE SALIDAS ---
if st.session_state.history:
    st.subheader("📜 Historial de salidas")
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df[::-1], use_container_width=True)
