
-- Insert data into the tables.
INSERT
INTO    customers (name, address)
VALUES  ("Finkakor AB", "Helsingborg"),
        ("Småbröd AB", "Malmö"),
        ("Kaffebröd AB", "Landskrona"),
        ("Bjudkakor AB", "Ystad"),
        ("Kalaskakor AB", "Trelleborg"),
        ("Partykakor AB", "Kristianstad"),
        ("Gästkakor AB", "Hässleholm"),
        ("Skånekakor AB", "Perstorp");

INSERT
INTO    recipes (name)
VALUES  ("Nut ring"),
        ("Nut cookie"),
        ("Amneris"),
        ("Tango"),
        ("Almond delight"),
        ("Berliner");

INSERT
INTO    raw_materials (raw_material, amount)
VALUES  ("Flour", 5000),
        ("Butter", 7000),
        ("Icing sugar", 3000),
        ("Roasted, chopped nuts", 3000),
        ("Fine-ground nuts", 2500),
        ("Ground, roasted nuts", 2700),
        ("Bread crumbs", 4500),
        ("Sugar", 5500),
        ("Egg whites", 2500),
        ("Chocolate", 10000),
        ("Marzipan", 2450),
        ("Eggs", 500),
        ("Potato starch", 2000),
        ("Wheat flour", 25000),
        ("Sodium bicarbonate", 2500),
        ("Vanilla", 4000),
        ("Chopped almonds", 2500),
        ("Cinnamon", 6000),
        ("Vanilla sugar", 2500);

INSERT
INTO    recipe_items (recipe, raw_material, amount)
VALUES  ("Nut ring", "Flour", 450),
        ("Nut ring", "Butter", 450),
        ("Nut ring", "Icing sugar", 190),
        ("Nut ring", "Roasted, chopped nuts", 225),
        ("Nut cookie", "Fine-ground nuts", 750),
        ("Nut cookie", "Ground, roasted nuts", 625),
        ("Nut cookie", "Bread crumbs", 125),
        ("Nut cookie", "Sugar", 375),
        ("Nut cookie", "Egg whites", 450),
        ("Nut cookie", "Chocolate", 50),
        ("Amneris", "Marzipan", 750),
        ("Amneris", "Butter", 250),
        ("Amneris", "Eggs", 250),
        ("Amneris", "Potato starch", 25),
        ("Amneris", "Wheat flour", 25),
        ("Tango", "Butter", 200),
        ("Tango", "Sugar", 250),
        ("Tango", "Flour", 300),
        ("Tango", "Sodium bicarbonate", 4),
        ("Tango", "Vanilla", 2),
        ("Almond delight", "Butter", 400),
        ("Almond delight", "Sugar", 270),
        ("Almond delight", "Chopped almonds", 279),
        ("Almond delight", "Flour", 400),
        ("Almond delight", "Cinnamon", 10),
        ("Berliner", "Flour", 350),
        ("Berliner", "Butter", 250),
        ("Berliner", "Icing sugar", 100),
        ("Berliner", "Eggs", 50),
        ("Berliner", "Vanilla sugar", 5),
        ("Berliner", "Chocolate", 50);
