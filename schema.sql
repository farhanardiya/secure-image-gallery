CREATE TABLE users(
    user_id     uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    username    varchar(255) NOT NULL UNIQUE,
    password    char(72) NOT NULL,
    is_active   boolean DEFAULT TRUE,
    created_at  bigint  not null,
    created_by  varchar(255) not null,
    updated_at  bigint  not null,
    updated_by  varchar(255) not null
);

CREATE TABLE user_image(
    image_id            uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id             uuid NOT NULL,
    image_name          varchar(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    image_enc     	bytea NOT NULL,
    iv              bytea NOT NULL,
    created_at  bigint  not null,
    created_by  varchar(255) not null,
    updated_at  bigint  not null,
    updated_by  varchar(255) not null,
    CONSTRAINT fk_user_image_user_id
      FOREIGN KEY(user_id) 
        REFERENCES users(user_id)
);
