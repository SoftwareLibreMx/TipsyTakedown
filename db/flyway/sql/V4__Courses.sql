DROP TYPE IF EXISTS MaterialType;
CREATE Type MaterialType AS ENUM ('VIDEO', 'PDF');

CREATE TABLE Materials (
	id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
	material_type MaterialType NOT NULL,
	name text NOT NULL,
	teacher_id UUID NOT NULL,
	description text DEFAULT NULL,
	file_path text DEFAULT NULL,
	is_file_encoded BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_teacher_id FOREIGN KEY(teacher_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE Lessons (
	id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
	name text NOT NULL,
	materials uuid[] NOT NULL,
	is_active BOOLEAN DEFAULT TRUE,
	created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE courses (
	id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
	name Text NOT NULL,
	lessons uuid[] NOT NULL,
	thumbnail Text NOT NULL,
	teaser_material_id UUID DEFAULT NULL,
	is_active BOOLEAN DEFAULT TRUE,
	created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    deleted_at TIMESTAMP DEFAULT NULL,
    CONSTRAINT fk_teaser_material_id FOREIGN KEY(teaser_material_id) REFERENCES Material(id)
);

DROP TABLE IF EXISTS Videos;

ALTER TABLE video_encoding_queue DROP CONSTRAINT fk_video_id;
ALTER TABLE video_encoding_queue ADD CONSTRAINT fk_material_id FOREIGN KEY(video_id) REFERENCES materials(id);
