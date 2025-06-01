
import streamlit as st
import pandas as pd
import os

def mostrar():
    st.header("✏️ Editar Estado por Pedido")

    csv_path = os.path.join("data", "tabla_trazabilidad.csv")
    try:
        df = pd.read_csv(csv_path, delimiter=";")
        pedido_ids = df["ID"].dropna().unique().tolist()
        pedido_seleccionado = st.selectbox("Selecciona el ID del pedido:", pedido_ids)

        pedido_df = df[df["ID"] == pedido_seleccionado].copy()
        index = df[df["ID"] == pedido_seleccionado].index[0]

        columnas_editables = [col for col in df.columns if col not in ["ID", "Cliente", "Producto"]]
        nuevos_valores = {}

        st.write(f"**Cliente:** {pedido_df.iloc[0]['Cliente']}")
        st.write(f"**Producto:** {pedido_df.iloc[0]['Producto']}")

        for col in columnas_editables:
            estado_actual = pedido_df.iloc[0][col]
            nuevos_valores[col] = st.selectbox(f"{col}:", ["Pendiente", "En curso", "Finalizado", "No aplica"], index=["Pendiente", "En curso", "Finalizado", "No aplica"].index(estado_actual) if estado_actual in ["Pendiente", "En curso", "Finalizado", "No aplica"] else 0)

        if st.button("💾 Guardar cambios"):
            for col, valor in nuevos_valores.items():
                df.at[index, col] = valor
            df.to_csv(csv_path, sep=";", index=False)
            st.success("✅ Cambios guardados exitosamente.")
            st.experimental_rerun()

    except Exception as e:
        st.error(f"No se pudo cargar o actualizar la tabla: {e}")
