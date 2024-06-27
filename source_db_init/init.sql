CREATE TABLE Products (
    Brand_Prod_id SERIAL PRIMARY KEY,
    Brand VARCHAR(50),
    Descript VARCHAR(800)
);

CREATE TABLE product_characteristics (
    id SERIAL PRIMARY KEY,
    Brand_id INTEGER REFERENCES Products(Brand_Prod_id),
    Brand VARCHAR(50),
    Descript VARCHAR(50)
);