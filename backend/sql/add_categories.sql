-- Dodaj nową tabelę kategorii
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Dodaj pole category_id do tabeli przepisów
ALTER TABLE recipes
    ADD COLUMN category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL;