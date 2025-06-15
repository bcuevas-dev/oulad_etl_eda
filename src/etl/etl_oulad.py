import pandas as pd
import numpy as np
import os

def main():
    cleaned_dir = 'data/cleaned'
    if not os.path.exists(cleaned_dir):
        os.makedirs(cleaned_dir)

    # Leer datasets originales
    student_info = pd.read_csv('data/original/studentInfo.csv')
    courses = pd.read_csv('data/original/courses.csv')
    student_registration = pd.read_csv('data/original/studentRegistration.csv')
    assessments = pd.read_csv('data/original/assessments.csv')
    student_assessments = pd.read_csv('data/original/studentAssessment.csv')
    vle = pd.read_csv('data/original/vle.csv')
    student_vle = pd.read_csv('data/original/studentVle.csv')

    # --------------------- LIMPIEZA GENERAL ---------------------
    for df in [student_info, courses, student_registration, assessments, student_assessments, vle, student_vle]:
        df.drop_duplicates(inplace=True)

    courses.drop_duplicates(subset=['code_module', 'code_presentation'], inplace=True)

    student_info.dropna(subset=['id_student'], inplace=True)
    student_info.dropna(axis=1, how='all', inplace=True)

    assessments.dropna(subset=['id_assessment', 'assessment_type'], inplace=True)
    student_assessments.dropna(subset=['id_assessment', 'id_student', 'score'], inplace=True)
    courses.dropna(subset=['code_module', 'code_presentation'], inplace=True)
    student_vle.dropna(subset=['id_student', 'id_site', 'date', 'sum_click'], inplace=True)
    vle.dropna(subset=['id_site', 'activity_type'], inplace=True)
    student_registration.dropna(subset=['id_student', 'date_registration'], inplace=True)

    # -------------------- NORMALIZACIÓN Y FACTORIZACIÓN --------------------
    student_info['disability'] = student_info['disability'].map({'Y': 1, 'N': 0})

    for col in ['age_band', 'highest_education', 'imd_band', 'region', 'final_result', 'gender',
                'code_module', 'code_presentation']:
        if col in student_info.columns:
            student_info[col] = student_info[col].astype(str).str.lower()

    for col in ['code_module', 'code_presentation']:
        if col in courses.columns:
            courses[col] = courses[col].astype(str).str.lower()
        if col in vle.columns:
            vle[col] = vle[col].astype(str).str.lower()
        if col in student_vle.columns:
            student_vle[col] = student_vle[col].astype(str).str.lower()

    def factorize_col(df, col):
        df[col + '_ordinal'], uniques = pd.factorize(df[col])
        return df, uniques

    student_info, _ = factorize_col(student_info, 'age_band')
    student_info, _ = factorize_col(student_info, 'highest_education')
    student_info, _ = factorize_col(student_info, 'imd_band')
    student_info, _ = factorize_col(student_info, 'region')
    student_info, _ = factorize_col(student_info, 'final_result')
    student_info, _ = factorize_col(student_info, 'gender')

    assessments['assessment_type'] = assessments['assessment_type'].str.lower()
    assessments, _ = factorize_col(assessments, 'assessment_type')

    vle['activity_type'] = vle['activity_type'].str.lower()
    vle, _ = factorize_col(vle, 'activity_type')

    # -------------------- CONVERSIÓN DE FECHAS --------------------
    student_registration['date_registration'] = pd.to_datetime(student_registration['date_registration'], errors='coerce')
    student_registration['date_unregistration'] = pd.to_datetime(student_registration.get('date_unregistration'), errors='coerce')

    if 'date_submitted' in student_assessments.columns:
        student_assessments['date_submitted'] = pd.to_datetime(student_assessments['date_submitted'], errors='coerce')

    if 'date' in student_vle.columns:
        student_vle['date'] = pd.to_datetime(student_vle['date'], errors='coerce')

    # -------------------- CONVERSIÓN DE TIPOS NUMÉRICOS --------------------
    for df in [student_assessments, student_registration, student_vle]:
        for col in ['sum_click', 'score']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

    # -------------------- GUARDADO FINAL --------------------
    student_info.to_csv(f'{cleaned_dir}/student_info_clean.csv', index=False)
    assessments.to_csv(f'{cleaned_dir}/assessments_clean.csv', index=False)
    student_assessments.to_csv(f'{cleaned_dir}/student_assessments_clean.csv', index=False)
    courses.to_csv(f'{cleaned_dir}/courses_clean.csv', index=False)
    student_vle.to_csv(f'{cleaned_dir}/student_vle_clean.csv', index=False)
    vle.to_csv(f'{cleaned_dir}/vle_clean.csv', index=False)
    student_registration.to_csv(f'{cleaned_dir}/student_registration_clean.csv', index=False)

    print("ETL completo. Archivos limpios guardados en carpeta 'data/cleaned/'.")

if __name__ == '__main__':
    main()

