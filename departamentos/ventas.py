
import streamlit as st
import pandas as pd
import os

def mostrar():
    st.header("Departamento de Ventas")
    csv_path = os.path.abspath(os.path.join("data", "pedidos.csv"))
    try:
        df = pd.read_csv(csv_path)
        pedidos = df[df["Departamento"] == "Ventas"]
        if not pedidos.empty:
            for idx, row in pedidos.iterrows():
                with st.expander(f"Pedido {row['ID']} – {row['Cliente']}"):
                    st.write(f"**Producto:** {row['Producto']}")
                    st.write(f"**Estado actual:** {row['Estado']}")
                    col1, col2 = st.columns(2)
                    if col1.button("Iniciar", key=f"iniciar_{row['ID']}"):
                        df.loc[df['ID'] == row['ID'], 'Estado'] = 'En curso'
                        df.to_csv(csv_path, index=False, encoding='utf-8')
                        st.success("✅ Pedido marcado como EN CURSO")
                        st.rerun()
                    if col2.button("Finalizar", key=f"finalizar_{row['ID']}"):
                        df.loc[df['ID'] == row['ID'], 'Estado'] = 'Finalizado'
                        df.to_csv(csv_path, index=False, encoding='utf-8')
                        st.success("✅ Pedido marcado como FINALIZADO")
                        st.rerun()
                    st.text_area("Observaciones", key=f"obs_{row['ID']}")
        else:
            st.info("No hay pedidos asignados a este departamento.")
    except Exception as e:
        st.error(f"No se pudo acceder a pedidos.csv: {e}")
