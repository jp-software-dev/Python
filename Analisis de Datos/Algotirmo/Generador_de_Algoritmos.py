import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# 1. Cargar tu archivo 
df = pd.read_csv('Analisis de Datos/BD_titanic_limpio.csv')

# Limpiar filas con valores vacíos
df = df.dropna()

# 2. Definir la columna objetivo explícitamente
columna_objetivo = 'Survived'
print(f"-> Usando la columna '{columna_objetivo}' como el objetivo a predecir.\n")

# 3. Separar las características (X) de la meta (y)
X = df.drop(columna_objetivo, axis=1) 
y = df[columna_objetivo] 

# Transformar textos a números (en tu archivo limpio ya son números, pero es buena práctica mantenerlo por seguridad)
X = pd.get_dummies(X, drop_first=True)
 
# 4. Dividir los datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Crear y entrenar el clasificador de árbol de decisión
# Limitamos la profundidad a 3 (max_depth=3) para que el árbol sea fácil de interpretar visualmente
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)
 
# 6. Realizar predicciones y evaluar la precisión
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Cálculo de F1-Score y Matriz de Confusión para tu reporte
f1 = f1_score(y_test, y_pred) 
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"Precisión (Accuracy): {accuracy:.4f}")
print(f"F1-Score: {f1:.4f}")
print("\nMatriz de Confusión:")
print(conf_matrix)
print("-" * 30)

# 7. Graficar el árbol de decisiones
plt.figure(figsize=(16, 9))

# Nombramos las clases para que el gráfico sea más fácil de leer
clases_nombres = ['No Sobrevivió', 'Sobrevivió']
plot_tree(clf, feature_names=list(X.columns), class_names=clases_nombres, filled=True, rounded=True)
plt.title("Árbol de Decisión - Supervivencia en el Titanic")
plt.show()