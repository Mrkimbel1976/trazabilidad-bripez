import streamlit as st
import pandas as pd
import os

def mostrar():
    st.header("Trazabilidad General de Producción - Bripez")
    st.write("Ejemplo de íconos: ✅ Finalizado, 🟡 En curso, 🔴 Pendiente, ⚪ No aplica")

    csv_path = os.path.join("data", "tabla_trazabilidad.csv")
    try:
        df = pd.read_csv(csv_path, delimiter=";")
        estados_colores = {
            "Finalizado": "✅ Finalizado",
            "En curso": "🟡 En curso",
            "Pendiente": "🔴 Pendiente",
            "No aplica": "⚪ No aplica"
        }

        # Aplicar los íconos
        df_coloreado = df.copy()
        for col in df.columns:
            if col not in ["ID", "Cliente", "Producto"]:
                df_coloreado[col] = df[col].map(estados_colores)

        # Filtro por cliente
        clientes = df["Cliente"].dropna().unique().tolist()
        cliente_seleccionado = st.selectbox("🔎 Filtrar por cliente:", ["Todos"] + clientes)

        # Filtro por estado general
        estado_seleccionado = st.selectbox("🎯 Filtrar por estado general:", ["Todos", "Finalizado", "En curso", "Pendiente"])

        # Aplicar filtros
        filtrado = df_coloreado.copy()
        if cliente_seleccionado != "Todos":
            filtrado = filtrado[filtrado["Cliente"] == cliente_seleccionado]

        if estado_seleccionado != "Todos":
            columnas_estado = [col for col in filtrado.columns if col not in ["ID", "Cliente", "Producto"]]
            filtrado = filtrado[filtrado[columnas_estado].apply(lambda row: estado_seleccionado in [s.replace("✅ ","").replace("🟡 ","").replace("🔴 ","").replace("⚪ ","") for s in row], axis=1)]

        st.dataframe(filtrado, use_container_width=True)

    except Exception as e:
        st.error(f"No se pudo cargar la tabla de trazabilidad: {e}")

