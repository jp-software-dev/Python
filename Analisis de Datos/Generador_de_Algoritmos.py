import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# 1. Cargar tu archivo de clientes de seguros
df = pd.read_csv('Analisis de Datos/clientes_seguro.csv')

# Limpiar filas con valores vacíos
df = df.dropna()

# 2. Buscar automáticamente la columna objetivo en datos de seguros
columna_objetivo = None
columnas_candidatas = ['compro_seguro', 'adquirio', 'fraude', 'siniestro', 'reclamo', 'target', 'riesgo', 'respuesta']

for col in columnas_candidatas:
    if col.lower() in [c.lower() for c in df.columns]:
        columna_objetivo = [c for c in df.columns if c.lower() == col.lower()][0]
        break

# Si no encuentra ninguna palabra clave, elige la última columna por defecto
if columna_objetivo is None:
    columna_objetivo = df.columns[-1]

print(f"-> Usando la columna '{columna_objetivo}' como el objetivo a predecir.\n")

# 3. Separar las características (X) de la meta (y)
X = df.drop(columna_objetivo, axis=1) 
y = df[columna_objetivo] 

# Transformar textos (ej. 'Hombre'/'Mujer', 'Tipo de Auto') a números
X = pd.get_dummies(X, drop_first=True)
 
# 4. Dividir los datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Crear y entrenar el clasificador de árbol de decisión
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)
 
# 6. Realizar predicciones y evaluar la precisión
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)


# 7. Graficar el árbol de decisiones
plt.figure(figsize=(16, 9))
clases_unicas = [str(c) for c in sorted(y.unique())]
plot_tree(clf, feature_names=list(X.columns), class_names=clases_unicas, filled=True, rounded=True)
plt.show()