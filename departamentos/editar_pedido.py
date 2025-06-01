
import streamlit as st
import pandas as pd
import os

def mostrar():
    st.header("✏️ Editar Estado y Observaciones por Pedido")

    csv_path = os.path.join("data", "tabla_trazabilidad.csv")
    try:
        df = pd.read_csv(csv_path, delimiter=";")
        pedido_ids = df["ID"].dropna().unique().tolist()
        pedido_seleccionado = st.selectbox("Selecciona el ID del pedido:", pedido_ids)

        pedido_df = df[df["ID"] == pedido_seleccionado].copy()
        index = df[df["ID"] == pedido_seleccionado].index[0]

        columnas_estados = [col for col in df.columns if col not in ["ID", "Cliente", "Producto"] and not col.startswith("Obs -")]
        columnas_obs = [f"Obs - {col}" for col in columnas_estados]

        # Asegurar que el CSV tenga columnas de observación
        for obs_col in columnas_obs:
            if obs_col not in df.columns:
                df[obs_col] = ""

        nuevos_estados = {}
        nuevas_obs = {}

        st.write(f"**Cliente:** {pedido_df.iloc[0]['Cliente']}")
        st.write(f"**Producto:** {pedido_df.iloc[0]['Producto']}")

        for col in columnas_estados:
            estado_actual = pedido_df.iloc[0][col]
            nuevos_estados[col] = st.selectbox(f"{col}:", ["Pendiente", "En curso", "Finalizado", "No aplica"], index=["Pendiente", "En curso", "Finalizado", "No aplica"].index(estado_actual) if estado_actual in ["Pendiente", "En curso", "Finalizado", "No aplica"] else 0)

            obs_col = f"Obs - {col}"
            observacion_actual = pedido_df.iloc[0][obs_col] if obs_col in pedido_df.columns else ""
            nuevas_obs[obs_col] = st.text_area(f"📝 Observación ({col}):", observacion_actual)

        if st.button("💾 Guardar cambios"):
            for col, estado in nuevos_estados.items():
                df.at[index, col] = estado
            for obs_col, texto in nuevas_obs.items():
                df.at[index, obs_col] = texto
            df.to_csv(csv_path, sep=";", index=False)
            st.success("✅ Cambios guardados exitosamente.")
            st.experimental_rerun()

    except Exception as e:
        st.error(f"No se pudo cargar o actualizar la tabla: {e}")
