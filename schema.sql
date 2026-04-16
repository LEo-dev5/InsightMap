-- InsightMap Database Schema

CREATE TABLE snapshots (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE
);

CREATE TABLE nodes (
    id SERIAL PRIMARY KEY,
    snapshot_id INTEGER REFERENCES snapshots(id),
    label VARCHAR(100) NOT NULL
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT,
    date DATE,
    url TEXT
);

CREATE TABLE node_articles (
    node_id INTEGER REFERENCES nodes(id),
    article_id INTEGER REFERENCES articles(id),
    PRIMARY KEY (node_id, article_id)
);

CREATE TABLE edges (
    id SERIAL PRIMARY KEY,
    snapshot_id INTEGER REFERENCES snapshots(id),
    from_node INTEGER REFERENCES nodes(id),
    to_node INTEGER REFERENCES nodes(id)
);
