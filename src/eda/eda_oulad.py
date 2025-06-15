import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
import itertools
import os
from sqlalchemy import create_engine

# Importamos la configuracion de mysql desde settings.py 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings

# Creamos el engine usando SQLAlchemy
engine = create_engine(settings.SQLALCHEMY_URL)

# Carpeta de salida
output_dir = 'outputs/figures'
os.makedirs(output_dir, exist_ok=True)

def plot_confusion_matrix(cm, classes, normalize=False, title='Matriz de Confusión', cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('Etiqueta verdadera')
    plt.xlabel('Etiqueta predicha')
    plt.savefig(f"{output_dir}/matriz_confusion.png")
    plt.show()

def main():
    # Cargamos los datos desde MySQL
    student_info = pd.read_sql('SELECT * FROM studentInfo', con=engine)
    assessments = pd.read_sql('SELECT * FROM assessments', con=engine)
    student_assessments = pd.read_sql('SELECT * FROM studentAssessment', con=engine)
    courses = pd.read_sql('SELECT * FROM courses', con=engine)
    vle = pd.read_sql('SELECT * FROM vle', con=engine)
    student_vle = pd.read_sql('SELECT * FROM studentVle', con=engine)
    student_registration = pd.read_sql('SELECT * FROM studentRegistration', con=engine)

    print("Tablas cargadas desde MySQL correctamente.")

    # --- Análisis descriptivo ---
    print("Resumen general studentInfo:")
    print(student_info.describe(include='all'))
    print("\nDistribución final_result:")
    print(student_info['final_result'].value_counts())

    # --- Correlación ---
    numeric_cols = ['disability', 'gender_ordinal', 'region_ordinal', 'age_band_ordinal',
                    'highest_education_ordinal', 'imd_band_ordinal', 'final_result_ordinal']
    corr = student_info[numeric_cols].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Matriz de correlación (student_info)')
    plt.savefig(f"{output_dir}/matriz_correlacion.png")
    plt.show()

    # --- Boxplot ---
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='final_result', y='disability', data=student_info)
    plt.title('Disability vs Final Result (Boxplot)')
    plt.savefig(f"{output_dir}/boxplot_disability_result.png")
    plt.show()

    # --- Histograma ---
    plt.figure(figsize=(8, 6))
    sns.histplot(student_info['age_band_ordinal'], kde=True, bins=10)
    plt.title('Distribución Age Band Ordinal con curva KDE')
    plt.savefig(f"{output_dir}/distribucion_edad.png")
    plt.show()

    # --- Scatter plot ---
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='highest_education_ordinal', y='final_result_ordinal', data=student_info)
    plt.title('Highest Education Ordinal vs Final Result Ordinal')
    plt.savefig(f"{output_dir}/dispersion_education_result.png")
    plt.show()

    # --- Pivot Table ---
    merged_sa = pd.merge(student_assessments, assessments, on='id_assessment', how='left')
    merged_sa = pd.merge(merged_sa, student_info[['id_student', 'final_result']], on='id_student', how='left')
    pivot = pd.pivot_table(merged_sa, index='assessment_type', columns='final_result',
                            values='score', aggfunc='mean')
    print("\nPivot table: Promedio score por assessment_type y final_result")
    print(pivot)

    # --- Matriz de Confusión ---
    y_true = student_info['final_result_ordinal']
    y_pred = student_info['final_result_ordinal'].sample(frac=1).reset_index(drop=True)
    cm = confusion_matrix(y_true, y_pred)
    classes = student_info['final_result'].unique()
    plot_confusion_matrix(cm, classes, normalize=True)

    # --- Total de clics por módulo ---
    vle_clicks = student_vle.groupby('code_module')['sum_click'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=vle_clicks.index, y=vle_clicks.values)
    plt.title('Total de clics en VLE por módulo')
    plt.xlabel('Módulo')
    plt.ylabel('Total clics')
    plt.savefig(f"{output_dir}/clics_por_modulo.png")
    plt.show()

    print("EDA completado y gráficos generados.")

if __name__ == '__main__':
    main()
