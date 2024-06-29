CREATE TABLE Products (
    Brand_Prod_id SERIAL PRIMARY KEY,
    Brand VARCHAR(50),
    Descript VARCHAR(800),
    Price FLOAT()
);

CREATE TABLE product_characteristics (
    id SERIAL PRIMARY KEY,
    Brand_id INTEGER REFERENCES Products(Brand_Prod_id),
    Brand VARCHAR(50),
    Descript VARCHAR(50)
);

CREATE TABLE product_img (
    id SERIAL PRIMARY KEY,
    Brand_id INTEGER REFERENCES Products(Brand_Prod_id),
    image_name VARCHAR(50),
);