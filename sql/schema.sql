PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    is_active INTEGER NOT NULL CHECK (is_active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('lecture', 'practice', 'exam')),
    publication_year INTEGER NOT NULL CHECK (publication_year BETWEEN 1900 AND 2100),
    is_published INTEGER NOT NULL CHECK (is_published IN (0, 1)),
    min_study_year INTEGER NOT NULL CHECK (min_study_year BETWEEN 1 AND 6),
    FOREIGN KEY (course_id) REFERENCES courses(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    study_year INTEGER NOT NULL CHECK (study_year BETWEEN 1 AND 6),
    FOREIGN KEY (course_id) REFERENCES courses(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_materials_course ON materials(course_id);
CREATE INDEX IF NOT EXISTS idx_students_course ON students(course_id);
CREATE INDEX IF NOT EXISTS idx_materials_title ON materials(title);
