import pandas as pd
import streamlit as st

st.set_page_config(page_title="Trazabilidad Bripez", layout="wide")
st.title("📋 Estado de Producción de Pedidos - Bripez")

try:
    df = pd.read_excel("produccion_bripez.xlsx")
    
    def evaluar_estado(row):
        etapas = ["Corte", "Confección", "Bordado", "Calidad", "Entregado"]
        completadas = sum([row[etapa] == "Sí" for etapa in etapas])
        if completadas == len(etapas):
            return "✅ Completado"
        elif completadas == 0:
            return "⏳ Pendiente"
        return f"🛠️ En proceso ({completadas}/{len(etapas)})"

    df["Estado"] = df.apply(evaluar_estado, axis=1)

    st.subheader("📦 Producción actual")
    st.dataframe(df[["Pedido", "Cliente", "Estado"]], use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ No se encontró 'produccion_bripez.xlsx'.")
except Exception as e:
    st.error(f"🚨 Error: {e}")

