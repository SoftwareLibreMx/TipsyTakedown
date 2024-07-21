CREATE TABLE Videos (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    teacher_id UUID NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    path text,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_teacher_id FOREIGN KEY(teacher_id) REFERENCES users(id)
);
