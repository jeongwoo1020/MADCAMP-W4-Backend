CREATE TABLE animes (
    anime_id SERIAL PRIMARY KEY,
    anilist_id INTEGER UNIQUE,
    title_en VARCHAR(255),
    image_url TEXT,
    description TEXT,
    start_date DATE,
    end_date DATE
);

CREATE TABLE anime_korean_titles (
    id SERIAL PRIMARY KEY,
    anime_id INTEGER REFERENCES animes(anime_id) ON DELETE CASCADE,
    title_kr VARCHAR(255)
);

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(50) UNIQUE
);

CREATE TABLE anime_genre_mapping (
    anime_id INTEGER REFERENCES animes(anime_id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (anime_id, genre_id)
);

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    google_id VARCHAR(255) UNIQUE,
    email VARCHAR(255),
    nick_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE,
    anime_id INTEGER REFERENCES animes(anime_id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'WATCHED', -- 'WATCHED' or 'REVIEWED'
    watching_start DATE,
    watching_end DATE,
    score_story INTEGER,
    score_character INTEGER,
    score_art INTEGER,
    score_music INTEGER,
    score FLOAT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_anime UNIQUE (user_id, anime_id),
);

CREATE TABLE user_insights (
    user_id INTEGER PRIMARY KEY REFERENCES Users(user_id) ON DELETE CASCADE,
    top_genres JSONB,
    preference_vector JSONB,
    persona_text TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);