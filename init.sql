CREATE TABLE query(
	id SERIAL PRIMARY KEY,
	query varchar(64) NOT NULL,
	region varchar(64) NOT NULL
);

CREATE TABLE count_in_interval(
    id SERIAL PRIMARY KEY,
    query_id INTEGER NOT NULL,
    count_items INTEGER NOT NULL,
    time_stamp TIMESTAMP NOT NULL default NOW(),
    FOREIGN KEY (query_id) REFERENCES query(id)
);

CREATE TABLE top_5(
    id SERIAL PRIMARY KEY,
    query_id INTEGER NOT NULL,
    links TEXT [],
    FOREIGN KEY (query_id) REFERENCES query(id)
);