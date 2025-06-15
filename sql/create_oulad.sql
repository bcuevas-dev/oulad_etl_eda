-- Eliminar base de datos si existe y crearla
DROP DATABASE IF EXISTS oulad_db;
CREATE DATABASE oulad_db;
USE oulad_db;

-- Tabla de cursos
CREATE TABLE courses (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    module_presentation_length INT,
    PRIMARY KEY (code_module, code_presentation)
);

-- Información del estudiante
CREATE TABLE studentInfo (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    id_student INT,
    gender VARCHAR(1),
    region VARCHAR(50),
    highest_education VARCHAR(50),
    imd_band VARCHAR(20),
    age_band VARCHAR(20),
    num_of_prev_attempts INT,
    studied_credits INT,
    disability TINYINT,
    final_result VARCHAR(20),

    -- Campos ordinales
    gender_ordinal INT,
    region_ordinal INT,
    age_band_ordinal INT,
    highest_education_ordinal INT,
    imd_band_ordinal INT,
    final_result_ordinal INT,

    PRIMARY KEY (code_module, code_presentation, id_student),
    FOREIGN KEY (code_module, code_presentation) REFERENCES courses(code_module, code_presentation)
);

-- Registro de inscripción de estudiantes
CREATE TABLE studentRegistration (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    id_student INT,
    date_registration DATE,
    date_unregistration DATE NULL,

    PRIMARY KEY (code_module, code_presentation, id_student),
    FOREIGN KEY (code_module, code_presentation, id_student)
        REFERENCES studentInfo(code_module, code_presentation, id_student)
);

-- Evaluaciones
CREATE TABLE assessments (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    id_assessment INT PRIMARY KEY,
    assessment_type VARCHAR(20),
    date INT,  -- corregido de DATE a INT
    weight FLOAT,

    assessment_type_ordinal INT,
    FOREIGN KEY (code_module, code_presentation) REFERENCES courses(code_module, code_presentation)
);

-- Resultados de estudiantes en evaluaciones
CREATE TABLE studentAssessment (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    id_assessment INT,
    id_student INT,
    date_submitted DATE,
    is_banked TINYINT,
    score FLOAT,

    PRIMARY KEY (id_assessment, id_student),
    FOREIGN KEY (id_assessment) REFERENCES assessments(id_assessment),
    FOREIGN KEY (code_module, code_presentation, id_student)
        REFERENCES studentInfo(code_module, code_presentation, id_student)
);

-- VLE – contenidos
CREATE TABLE vle (
    id_site INT PRIMARY KEY,
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    activity_type VARCHAR(50),
    week_from INT,
    week_to INT,
    activity_type_ordinal INT,
    FOREIGN KEY (code_module, code_presentation) REFERENCES courses(code_module, code_presentation)
);

-- Interacciones de estudiantes con VLE
CREATE TABLE studentVle (
    code_module VARCHAR(10),
    code_presentation VARCHAR(10),
    id_student INT,
    id_site INT,
    date DATE,
    sum_click INT,

    PRIMARY KEY (code_module, code_presentation, id_student, id_site, date),
    FOREIGN KEY (code_module, code_presentation, id_student)
        REFERENCES studentInfo(code_module, code_presentation, id_student),
    FOREIGN KEY (id_site) REFERENCES vle(id_site)
);



use oulad_db;
select *from studentVle;

