CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "citext";

CREATE Type UserType AS ENUM (
 'STUDENT',
 'TEACHER',
 'ADMIN'
);

CREATE Type SSOProvider AS ENUM (
	'GOOGLE',
	'FACEBOOK'
);

CREATE TABLE users (
	id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
	type UserType DEFAULT 'STUDENT',
	given_name text DEFAULT NULL,
	surname text DEFAULT NULL,
    avatar text DEFAULT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	updated_at timestamp NOT NULL DEFAULT now(),
	deleted_at timestamp DEFAULT NULL
);

CREATE TABLE user_credentials (
	id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
	user_id UUID NOT NULL,
	email citext DEFAULT NULL,
	sso_provider SSOProvider DEFAULT NULL,
	openid text DEFAULT NULL,
	password_hash bytea DEFAULT NULL,
    password_salt bytea DEFAULT NULL,
    password_hash_params text DEFAULT NULL,
    created_at timestamp NOT NULL DEFAULT now(),
	updated_at timestamp NOT NULL DEFAULT now(),
	deleted_at timestamp DEFAULT NULL,
	CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT check_authentication_methods CHECK ( 
        ((password_hash IS NOT NULL AND password_salt IS NOT NULL AND password_hash_params IS NOT NULL) 
        OR (sso_provider IS NOT NULL AND openid IS NOT NULL)) 
    )
);
