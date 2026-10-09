CREATE TYPE gender_enum AS ENUM ('M', 'F');


CREATE TABLE public.Students (
	id SERIAL PRIMARY KEY,
	birthday DATE,
	name VARCHAR(50),
	sex gender_enum,
	
	CONSTRAINT name_not_empty CHECK (name <> ''),
);

CREATE TABLE public.Rooms (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100),
	
	CONSTRAINT chk_room_name CHECK (name ~ '^Room #[0-9]+$')
);

CREATE TABLE public.LinkStudentsWithRooms (
	id SERIAL PRIMARY KEY,
	student INT REFERENCES public.Students(id),
	room INT REFERENCES public.Rooms(id)
);