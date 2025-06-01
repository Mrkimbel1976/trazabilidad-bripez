import streamlit as st
import pandas as pd
import os

def mostrar():
    st.header("🔔 Alertas por Pedidos Estancados")

    csv_path = os.path.join("data", "alertas_estancadas.csv")

    try:
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')

        if df.empty:
            st.success("✅ No hay alertas activas por estancamiento.")
        else:
            for _, row in df.iterrows():
                with st.expander(f"🟠 Pedido ID {row['ID']} - {row['Cliente']}"):
                    st.write(f"**Departamento afectado:** {row['Departamento Afectado']}")
                    st.write(f"**Días sin avance:** {row['Días Estancado']}")
                    st.write(f"**Complejidad:** {row['Complejidad']}")
                    st.write(f"**Mensaje de alerta:** {row['Mensaje de alerta']}")

    except FileNotFoundError:
        st.error("❌ Archivo de alertas no encontrado.")
    except Exception as e:
        st.error(f"Error al cargar las alertas: {e}")


