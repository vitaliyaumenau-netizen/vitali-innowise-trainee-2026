CREATE TYPE gender_enum AS ENUM ('M', 'F');


CREATE TABLE public.Students (
	id SERIAL PRIMARY KEY,
	birthday DATE,
	name VARCHAR(50),
	room INT REFERENCES public.Rooms(id),
	sex gender_enum,
	
	CONSTRAINT name_not_empty CHECK (name <> ''),
);

CREATE TABLE public.Rooms (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100),
	
	CONSTRAINT chk_room_name CHECK (name ~ '^Room #[0-9]+$')
);

-- 1. Индекс для связывания таблиц rooms и students по внешнему ключу room
CREATE INDEX IF NOT EXISTS idx_students_room ON students(room);

-- 2. Составной индекс для поиска по полу и комнате (ускоряет HAVING COUNT(DISTINCT sex) > 1)
CREATE INDEX IF NOT EXISTS idx_students_room_sex ON students(room, sex);

-- 3. Индекс по дате рождения (ускоряет функции AGE, MIN, MAX и AVG)
CREATE INDEX IF NOT EXISTS idx_students_birthday ON students(birthday);