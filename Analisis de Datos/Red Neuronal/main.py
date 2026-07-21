import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. CARGA DE DATOS ---
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_csv = os.path.join(directorio_actual, 'red_neuronal.csv')

# Verificar si el archivo existe antes de leerlo
if not os.path.exists(ruta_csv):
    print(f"ERROR: No se encontró el archivo en {ruta_csv}")
    print("Asegúrate de que el archivo 'red_neuronal.csv' esté en la misma carpeta que este script.")
    exit()

df = pd.read_csv(ruta_csv)

X = df.drop('ID', axis=1)
y = df['ID']

# Detección automática para el diagrama
n_inputs = X.shape[1]
n_outputs = y.nunique()

# --- 2. ENTRENAMIENTO DE LA RED NEURONAL ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Mantenemos la arquitectura
red_neuronal = MLPClassifier(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', max_iter=1000, random_state=42)
red_neuronal.fit(X_train_scaled, y_train)

y_pred = red_neuronal.predict(X_test_scaled)

# Extraer métricas para gráficos
cm = confusion_matrix(y_test, y_pred)
loss_curve = red_neuronal.loss_curve_
acc = red_neuronal.score(X_test_scaled, y_test)

# --- 3. GENERACIÓN DE GRÁFICOS (DISEÑO PROFESIONAL) ---
# Establecer estilo base
plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(22, 9), facecolor='#f8f9fa')

# Título principal
fig.suptitle('Análisis Avanzado de Red Neuronal - Clasificación de Vinos', 
             fontsize=24, fontweight='bold', color='#2c3e50', y=0.96)

# ---- Gráfico 1: Arquitectura de la Red Neuronal ----
ax1 = plt.subplot(1, 3, 1)
ax1.set_facecolor('#ffffff')

# Reducimos los nodos visualmente para que el diagrama sea limpio
layers = [n_inputs, 8, 6, n_outputs] 
x_positions = [0, 1.5, 3, 4.5]

# Dibujar conexiones
for i in range(len(layers) - 1):
    for y1 in range(layers[i]):
        for y2 in range(layers[i+1]):
            y_pos1 = y1 - (layers[i] - 1) / 2
            y_pos2 = y2 - (layers[i+1] - 1) / 2
            ax1.plot([x_positions[i], x_positions[i+1]], [y_pos1, y_pos2], 
                    c='#bdc3c7', alpha=0.3, zorder=1, linewidth=1)

# Dibujar nodos
colors = ['#3498db', '#e74c3c', '#e74c3c', '#2ecc71']
layer_names = ['Entrada\n(13 caract.)', 'Capa Oculta 1', 'Capa Oculta 2', 'Salida\n(3 Clases)']

for i, layer_size in enumerate(layers):
    y_positions = [j - (layer_size - 1) / 2 for j in range(layer_size)]
    ax1.scatter([x_positions[i]] * layer_size, y_positions, s=250, c=colors[i], 
                edgecolors='white', linewidth=2, zorder=2)
    
    # Etiquetas de las capas
    ax1.text(x_positions[i], max(y_positions) + 1.2, layer_names[i], 
             ha='center', va='bottom', fontsize=12, fontweight='bold', color='#34495e')

ax1.set_title('Topología de la Red', fontsize=16, color='#2c3e50', pad=25, fontweight='bold')
ax1.axis('off')

# ---- Gráfico 2: Matriz de Confusión ----
ax2 = plt.subplot(1, 3, 2)
sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu', ax=ax2, 
            xticklabels=np.unique(y), yticklabels=np.unique(y),
            cbar_kws={'shrink': 0.8}, square=True, annot_kws={"size": 16, "weight": "bold"})
ax2.set_title('Matriz de Confusión', fontsize=16, color='#2c3e50', pad=20, fontweight='bold')
ax2.set_xlabel('Predicción del Modelo', fontsize=14, labelpad=10)
ax2.set_ylabel('Valor Real (Etiqueta)', fontsize=14, labelpad=10)
ax2.tick_params(axis='both', which='major', labelsize=12)

# ---- Gráfico 3: Curva de Pérdida ----
ax3 = plt.subplot(1, 3, 3)
ax3.set_facecolor('#ffffff')

# Línea de pérdida y área sombreada
ax3.plot(loss_curve, color='#e74c3c', linewidth=3, label='Error (Pérdida)')
ax3.fill_between(range(len(loss_curve)), loss_curve, color='#e74c3c', alpha=0.1)

ax3.set_title('Curva de Aprendizaje', fontsize=16, color='#2c3e50', pad=20, fontweight='bold')
ax3.set_xlabel('Épocas de Entrenamiento', fontsize=14, labelpad=10)
ax3.set_ylabel('Valor de Pérdida (Loss)', fontsize=14, labelpad=10)
ax3.tick_params(axis='both', which='major', labelsize=12)
ax3.grid(True, linestyle='--', alpha=0.6, color='#bdc3c7')
ax3.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)

# Cuadro resumen de métricas flotante
textstr = f'Precisión Final: {acc*100:.1f}%\nTotal Épocas: {len(loss_curve)}'
props = dict(boxstyle='round,pad=0.8', facecolor='#2ecc71', alpha=0.15, edgecolor='#27ae60', linewidth=2)
ax3.text(0.5, 0.5, textstr, transform=ax3.transAxes, fontsize=15, fontweight='bold',
        verticalalignment='center', horizontalalignment='center', bbox=props, color='#2c3e50')

# Ajustar márgenes y Guardar
plt.tight_layout(rect=[0, 0.03, 1, 0.93])
archivo_salida = os.path.join(directorio_actual, 'reporte_red_neuronal_PRO.png')
plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')

print(f"\n¡Proceso exitoso!")
print(f"Se ha guardado el reporte profesional en: {archivo_salida}")

# Mostrar ventana interactiva
plt.show()