import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="📦 Inventario Pro", layout="wide")

# --- LOGIN SIMPLE ---
PASSWORD = "mi_clave_segura"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.sidebar.title("🔐 Iniciar sesión")
    password = st.sidebar.text_input("Contraseña:", type="password")
    if st.sidebar.button("Entrar"):
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
if "salida_hist" not in st.session_state:
    st.session_state.salida_hist = []

# --- SIDEBAR DE NAVEGACIÓN ---
st.sidebar.title("📋 Menú")
opcion = st.sidebar.radio("Ir a la sección:", [
    "📥 Agregar productos",
    "➕ Registrar entrada",
    "➖ Registrar salida",
    "📘 Ver inventario",
    "🧾 Historial general"
])

st.markdown("<style>section.main > div {padding-top: 20px;}</style>", unsafe_allow_html=True)

# --- SECCIÓN: AGREGAR PRODUCTOS ---
if opcion == "📥 Agregar productos":
    st.title("📥 Agregar productos nuevos")
    st.markdown("Pega aquí productos en el formato: `CODIGO, Nombre, Cantidad`")

    texto = st.text_area("Productos nuevos:", height=150)
    if st.button("Agregar"):
        nuevas_filas = []
        for linea in texto.strip().split("\n"):
            partes = [p.strip() for p in linea.split(",")]
            if len(partes) == 3:
                cod, nombre, cantidad = partes
                try:
                    cantidad = int(cantidad)
                    nuevas_filas.append({"Código": cod, "Producto": nombre, "Stock": cantidad})
                except:
                    st.warning(f"❗ Error en cantidad: {linea}")
            else:
                st.warning(f"❗ Formato incorrecto: {linea}")

        if nuevas_filas:
            df_nuevo = pd.DataFrame(nuevas_filas)
            st.session_state.df = pd.concat([st.session_state.df, df_nuevo], ignore_index=True)
            st.success("✅ Productos agregados")

# --- SECCIÓN: REGISTRAR ENTRADA ---
elif opcion == "➕ Registrar entrada":
    st.title("➕ Entrada de productos")
    if st.session_state.df.empty:
        st.warning("No hay productos en el inventario.")
    else:
        codigo = st.selectbox("Código:", st.session_state.df["Código"].tolist())
        fila = st.session_state.df[st.session_state.df["Código"] == codigo].iloc[0]
        st.markdown(f"**Producto:** {fila['Producto']}")
        st.markdown(f"**Stock actual:** {fila['Stock']}")

        cantidad = st.number_input("Unidades que entraron:", min_value=1, step=1)
        if st.button("Registrar entrada"):
            idx = st.session_state.df[st.session_state.df["Código"] == codigo].index[0]
            st.session_state.df.at[idx, "Stock"] += cantidad
            st.session_state.entrada_hist.append({
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Código": codigo,
                "Producto": fila["Producto"],
                "Cantidad": cantidad,
                "Tipo": "Entrada"
            })
            st.success("✅ Entrada registrada")

# --- SECCIÓN: REGISTRAR SALIDA ---
elif opcion == "➖ Registrar salida":
    st.title("➖ Salida de productos")
    if st.session_state.df.empty:
        st.warning("No hay productos en el inventario.")
    else:
        codigo = st.selectbox("Código:", st.session_state.df["Código"].tolist(), key="salida")
        fila = st.session_state.df[st.session_state.df["Código"] == codigo].iloc[0]
        st.markdown(f"**Producto:** {fila['Producto']}")
        st.markdown(f"**Stock actual:** {fila['Stock']}")

        cantidad = st.number_input("Unidades que salieron:", min_value=1, step=1, key="qty_salida")
        if st.button("Registrar salida"):
            idx = st.session_state.df[st.session_state.df["Código"] == codigo].index[0]
            if cantidad > st.session_state.df.at[idx, "Stock"]:
                st.error("❌ No hay suficiente stock.")
            else:
                st.session_state.df.at[idx, "Stock"] -= cantidad
                st.session_state.salida_hist.append({
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Código": codigo,
                    "Producto": fila["Producto"],
                    "Cantidad": cantidad,
                    "Tipo": "Salida"
                })
                st.success("✅ Salida registrada")

# --- SECCIÓN: VER INVENTARIO ---
elif opcion == "📘 Ver inventario":
    st.title("📘 Inventario actual")
    if st.session_state.df.empty:
        st.info("No hay productos en el inventario.")
    else:
        st.dataframe(st.session_state.df, use_container_width=True)

# --- SECCIÓN: HISTORIAL GENERAL ---
elif opcion == "🧾 Historial general":
    st.title("🧾 Historial de movimientos")
    total = st.session_state.entrada_hist + st.session_state.salida_hist
    if total:
        df_hist = pd.DataFrame(total)
        df_hist = df_hist.sort_values("Fecha", ascending=False)
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.info("No hay movimientos aún.")
