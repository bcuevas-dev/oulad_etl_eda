-- ===============================================
-- FULL DOMAIN PARA OULAD
-- ===============================================

-- 🔧 Limpieza previa por si existen
DROP TABLE IF EXISTS domain_assessment_type;
DROP TABLE IF EXISTS domain_activity_type;
DROP TABLE IF EXISTS domain_final_result;
DROP TABLE IF EXISTS domain_highest_education;
DROP TABLE IF EXISTS domain_age_band;
DROP TABLE IF EXISTS domain_disability;
DROP TABLE IF EXISTS domain_gender;
DROP TABLE IF EXISTS domain_region;

-- ===============================================
-- ASSESSMENT TYPE DOMAIN
CREATE TABLE domain_assessment_type (
    assessment_type VARCHAR(20) PRIMARY KEY,
    assessment_type_ordinal INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO domain_assessment_type VALUES
('TMA', 1),
('CMA', 2),
('Exam', 3);

-- ===============================================
-- ACTIVITY TYPE DOMAIN (VLE)
CREATE TABLE domain_activity_type (
    activity_type VARCHAR(50) PRIMARY KEY,
    activity_type_ordinal INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO domain_activity_type VALUES
('homepage', 1),
('resource', 2),
('url', 3),
('oucontent', 4),
('subpage', 5),
('forumng', 6),
('oucollaborate', 7),
('quiz', 8),
('sharedsubpage', 9),
('glossary', 10),
('repeatactivity', 11),
('externalquiz', 12);

-- ===============================================

CREATE TABLE domain_final_result (
    final_result VARCHAR(20) PRIMARY KEY,
    final_result_ordinal INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO domain_final_result VALUES
('Fail', 0),
('Withdrawn', 1),
('Pass', 2),
('Distinction', 3);

-- ===============================================

CREATE TABLE domain_highest_education (
    highest_education VARCHAR(50) PRIMARY KEY,
    highest_education_ordinal INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO domain_highest_education VALUES
('No Formal quals', 0),
('Lower Than A Level', 1),
('A Level or Equivalent', 2),
('HE Qualification', 3),
('Post Graduate Qualification', 4);

-- ===============================================

CREATE TABLE domain_age_band (
    age_band VARCHAR(20) PRIMARY KEY,
    age_band_ordinal INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO domain_age_band VALUES
('0-35', 0),
('35-55', 1),
('55<=', 2);

-- ===============================================

CREATE TABLE domain_disability (
    disability VARCHAR(10) PRIMARY KEY,
    disability_ordinal INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO domain_disability VALUES
('N', 0),
('Y', 1);

-- ===============================================

CREATE TABLE domain_gender (
    gender VARCHAR(10) PRIMARY KEY,
    gender_ordinal INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO domain_gender VALUES
('M', 0),
('F', 1);

-- ===============================================
-- REGION DOMAIN
CREATE TABLE domain_region (
    region VARCHAR(50) PRIMARY KEY,
    region_ordinal INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO domain_region VALUES
('East Anglian Region', 1),
('East Midlands Region', 2),
('Ireland Region', 3),
('London Region', 4),
('North Region', 5),
('North Western Region', 6),
('Scotland Region', 7),
('South East Region', 8),
('South Region', 9),
('South West Region', 10),
('Wales Region', 11),
('West Midlands Region', 12),
('Yorkshire Region', 13);


