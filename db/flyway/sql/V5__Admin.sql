-- Insert admin user into users table
INSERT INTO users
(id, "type", given_name, surname, avatar, created_at, updated_at, deleted_at)
VALUES('c25f6091-0dc4-4c8b-81c6-c088d2d4ab74', 'ADMIN', 'Tipsy', 'Admin', NULL, NOW(), NOW(), NULL);

-- Insert corresponding entry into user_credentials table
INSERT INTO public.user_credentials
(id, user_id, email, sso_provider, openid, password_hash, password_salt, password_hash_params, created_at, updated_at, deleted_at)
VALUES('b854c0ee-a357-46bc-adb2-9f77959b59bb', 'c25f6091-0dc4-4c8b-81c6-c088d2d4ab74', 'change_me@example.com', NULL, NULL, decode('E48C2CD50A8415349AA8A559FE499C6B803E82E20BF68986E47844482AC6944AA4D641CFD2902BCB68B48442B30258FF423B690CCC251633B5F511CA7B55BE2128CD4497DEAE5232F79D49D545726CD88A4AF37F202DE9608BA8941C127BB07DB318B973828404E80A1514D2544180890D4E0742A47EB19369341DFE02CD59F9','hex'), decode('8DA728214FAF6769B32E26CB06F00A2140E9AA0885E28BB7EBA44540664075DA','hex'), '{"N": 2048, "r": 8, "p": 1, "dkLen": 128}', NOW(), NOW(), NULL);
