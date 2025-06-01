import streamlit as st
import pandas as pd
import os
import datetime
import pdfkit

def mostrar():
    st.header("Trazabilidad General de Producción - Bripez")
    st.write("Símbolos compatibles: ✔ Finalizado, ● En curso, ✖ Pendiente, ○ No aplica")
    
    csv_path = os.path.join("data", "tabla_trazabilidad.csv")
    try:
        df = pd.read_csv(csv_path, delimiter=";")
        
        estados_simbolos = {
            "Finalizado": "✔ Finalizado",
            "En curso": "● En curso",
            "Pendiente": "✖ Pendiente",
            "No aplica": "○ No aplica"
        }
        
        colores_estado = {
            "✔ Finalizado": "#c6efce",
            "● En curso": "#ffeb9c",
            "✖ Pendiente": "#ffc7ce",
            "○ No aplica": "#f0f0f0"
        }

        df_coloreado = df.copy()
        for col in df.columns:
            if col not in ["ID", "Cliente", "Producto"]:
                df_coloreado[col] = df[col].map(estados_simbolos)

        st.dataframe(df_coloreado, use_container_width=True)

        if st.button("📤 Exportar trazabilidad a PDF"):
            fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            output_path = f"data/trazabilidad_bripez_{fecha}.pdf"

            # Construir filas con colores
            html_rows = ""
            for _, row in df_coloreado.iterrows():
                html_rows += "<tr>"
                for col in df_coloreado.columns:
                    valor = row[col]
                    color = colores_estado.get(valor, "#ffffff")
                    html_rows += f'<td style="background-color:{color};padding:6px;text-align:center;">{valor}</td>'
                html_rows += "</tr>"

            # Construir el HTML completo
            html_content = f'''
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 12px;
                        padding: 20px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
                    th, td {{
                        border: 1px solid #888;
                        padding: 6px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                </style>
            </head>
            <body>
                <h2>Trazabilidad de Producción - Bripez</h2>
                <p>Fecha: {fecha}</p>
                <table>
                    <thead>
                        <tr>{"".join(f"<th>{col}</th>" for col in df_coloreado.columns)}</tr>
                    </thead>
                    <tbody>
                        {html_rows}
                    </tbody>
                </table>
            </body>
            </html>
            '''

            # Generar PDF
            pdfkit.from_string(html_content, output_path)

            # Botón de descarga
            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 Descargar PDF",
                    data=f,
                    file_name=f"trazabilidad_bripez_{fecha}.pdf",
                    mime="application/pdf"
                )

    except Exception as e:
        st.error(f"No se pudo cargar la tabla de trazabilidad: {e}")

