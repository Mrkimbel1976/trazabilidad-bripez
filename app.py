import streamlit as st
from departamentos import ventas, produccion, diseno, corte, empaquetado, trazabilidad, editar_pedido, alertas
from PIL import Image
import os

# ✅ Configuración de la página (debe ir primero)
st.set_page_config(page_title="Bripez App", layout="wide")

# ✅ Cargar logo desde carpeta assets
logo_path = os.path.join("assets", "logo_bripez_ajustado.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)

# ✅ Aplicar estilo visual personalizado
css_path = os.path.join("data", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Menú lateral
menu = st.sidebar.radio("Ir a:", [
    "Ventas",
    "Producción",
    "Diseño",
    "Corte",
    "Empaquetado",
    "Trazabilidad General",
    "Editar Pedido",
    "Alertas"
])

# ✅ Enrutamiento a módulos
if menu == "Ventas":
    ventas.mostrar()
elif menu == "Producción":
    produccion.mostrar()
elif menu == "Diseño":
    diseno.mostrar()
elif menu == "Corte":
    corte.mostrar()
elif menu == "Empaquetado":
    empaquetado.mostrar()
elif menu == "Trazabilidad General":
    trazabilidad.mostrar()
elif menu == "Editar Pedido":
    editar_pedido.mostrar()
elif menu == "Alertas":
    alertas.mostrar()
