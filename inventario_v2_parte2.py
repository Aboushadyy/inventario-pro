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

# --- CARGAR INVENTARIO ---
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Código", "Producto", "Stock"])

# --- TÍTULO ---
st.title("📦 Inventario Profesional - Parte 2")
st.markdown("Puedes agregar productos nuevos copiando y pegando varios códigos, nombres y cantidades.")

# --- AGREGAR PRODUCTOS POR TEXTO ---
st.subheader("🆕 Agregar productos en bloque")

st.markdown("Pega los productos en este formato:")
st.code("TTP, Tape transparente pequeño, 66", language="text")

input_text = st.text_area("Pega aquí los productos nuevos:", height=200)
if st.button("➕ Agregar productos"):
    if input_text.strip():
        new_rows = []
        lines = input_text.strip().split("\n")
        for line in lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) == 3:
                codigo, nombre, cantidad = parts
                try:
                    cantidad = int(cantidad)
                    new_rows.append({"Código": codigo, "Producto": nombre, "Stock": cantidad})
                except:
                    st.warning(f"No se pudo convertir la cantidad en la línea: {line}")
            else:
                st.warning(f"Formato incorrecto en línea: {line}")

        if new_rows:
            df_new = pd.DataFrame(new_rows)
            st.session_state.df = pd.concat([st.session_state.df, df_new], ignore_index=True)
            st.success(f"✅ Se agregaron {len(new_rows)} productos nuevos.")
    else:
        st.warning("Por favor, pega algún texto.")

# --- MOSTRAR TABLA ACTUAL ---
st.subheader("📋 Tabla actual de productos")
st.dataframe(st.session_state.df, use_container_width=True)
