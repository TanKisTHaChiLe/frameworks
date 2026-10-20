-- 1. Список курсов в алфавитном порядке (SELECT, ORDER BY)
SELECT id, name, is_active
FROM courses
ORDER BY name;

-- 2. Список материалов от новых к старым (SELECT, ORDER BY)
SELECT id, title, publication_year
FROM materials
ORDER BY publication_year DESC, title;

-- 3. Только активные курсы (WHERE)
SELECT id, name
FROM courses
WHERE is_active = 1
ORDER BY name;

-- 4. Опубликованные материалы для первого года обучения (WHERE)
SELECT id, title, category
FROM materials
WHERE is_published = 1 AND min_study_year <= 1
ORDER BY title;

-- 5. Материалы с названиями связанных курсов (JOIN)
SELECT materials.id, materials.title, courses.name AS course_name
FROM materials
JOIN courses ON materials.course_id = courses.id
ORDER BY courses.name, materials.title;

-- 6. Студенты с названиями связанных курсов (JOIN)
SELECT students.id, students.name, students.study_year,
       courses.name AS course_name
FROM students
JOIN courses ON students.course_id = courses.id
ORDER BY students.name;

-- 7. Общее количество материалов (COUNT)
SELECT COUNT(*) AS materials_count
FROM materials;

-- 8. Количество опубликованных материалов (COUNT, WHERE)
SELECT COUNT(*) AS published_count
FROM materials
WHERE is_published = 1;

-- 9. Количество материалов по курсам (JOIN, COUNT, GROUP BY)
SELECT courses.id, courses.name,
       COUNT(materials.id) AS materials_count
FROM courses
LEFT JOIN materials ON courses.id = materials.course_id
GROUP BY courses.id, courses.name
ORDER BY materials_count DESC, courses.name;

-- 10. Количество студентов по курсам (JOIN, COUNT, GROUP BY)
SELECT courses.id, courses.name,
       COUNT(students.id) AS students_count
FROM courses
LEFT JOIN students ON courses.id = students.course_id
GROUP BY courses.id, courses.name
ORDER BY students_count DESC, courses.name;

-- 11. Статистика публикаций по категориям (COUNT, GROUP BY)
SELECT category, COUNT(*) AS materials_count,
       SUM(is_published) AS published_count
FROM materials
GROUP BY category
ORDER BY materials_count DESC, category;

-- 12. Курсы, где больше одного материала (COUNT, GROUP BY, HAVING)
SELECT courses.id, courses.name,
       COUNT(materials.id) AS materials_count
FROM courses
JOIN materials ON courses.id = materials.course_id
GROUP BY courses.id, courses.name
HAVING COUNT(materials.id) > 1
ORDER BY materials_count DESC;

-- 13. Материалы курсов, на которых есть старшекурсники (WHERE, подзапрос)
SELECT id, title, course_id
FROM materials
WHERE course_id IN (
    SELECT DISTINCT course_id
    FROM students
    WHERE study_year >= 3
)
ORDER BY title;
