CREATE TABLE Videos (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    teacher_id UUID NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    path text,
    is_file_encoded BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_teacher_id FOREIGN KEY(teacher_id) REFERENCES users(id)
);

DROP TYPE IF EXISTS VideoStatus;
CREATE Type VideoStatus AS ENUM (
    'PENDING',
    'ENCODING',
    'COMPLETED',
    'FAILED'
);

CREATE TABLE video_encoding_queue (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    video_id UUID NOT NULL,
    file_key text NOT NULL,
    status VideoStatus DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_video_id FOREIGN KEY(video_id) REFERENCES videos(id)
);
