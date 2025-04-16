
import pandas as pd

# Cargar archivo Excel
df = pd.read_excel("produccion_bripez.xlsx")

# Función para evaluar estado del pedido
def evaluar_estado(row):
    etapas = ["Corte", "Confección", "Bordado", "Calidad", "Entregado"]
    completadas = sum([row[etapa] == "Sí" for etapa in etapas])
    if completadas == len(etapas):
        return "✅ Completado"
    elif completadas == 0:
        return "⏳ Pendiente"
    else:
        return f"🛠️ En proceso ({completadas}/{len(etapas)})"

# Agregar columna con estado
df["Estado"] = df.apply(evaluar_estado, axis=1)

# Mostrar resultados
print("\nESTADO DE PRODUCCIÓN DE PEDIDOS\n")
print(df[["Pedido", "Cliente", "Estado"]])
