import sqlite3

# Connexion à la base de données
connection = sqlite3.connect('Delicrous.db')
cursor = connection.cursor()

print("Opened database successfully")

# Création de la table User
cursor.execute('''  
CREATE TABLE IF NOT EXISTS User (
    id_User INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    firstname_User TEXT NOT NULL,
    lastname_User TEXT NOT NULL,
    email_User TEXT NOT NULL, 
    phone_User TEXT NOT NULL,
    password_User TEXT NOT NULL,
    professional_User BOOLEAN NOT NULL,
    scholar_User BOOLEAN NOT NULL
)''')   

print("Table User created successfully")

# Création de la table Campus
cursor.execute('''
CREATE TABLE IF NOT EXISTS Campus (
    id_Campus INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name_Campus TEXT NOT NULL,
    location_Campus TEXT NOT NULL
)''')

print("Table Campus created successfully")

# Création de la table Restaurant
cursor.execute('''  
CREATE TABLE IF NOT EXISTS Restaurant (
    id_Restaurant INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name_Restaurant TEXT NOT NULL,
    phone_Restaurant TEXT NOT NULL,
    description_Restaurant TEXT,
    image_logo_Restaurant TEXT,
    image_banner_Restaurant TEXT ,
    opening_time_Restaurant TEXT,
    closing_time_Restaurant TEXT,
    campus_id_Restaurant INTEGER NOT NULL,
    FOREIGN KEY(campus_id_Restaurant) REFERENCES Campus(id_Campus)
)''')

print("Table Restaurant created successfully")

# Création de la table Dish
cursor.execute('''  
CREATE TABLE IF NOT EXISTS Dish (
    id_Dish INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name_Dish TEXT NOT NULL,
    price_Dish REAL NOT NULL,
    description_Dish TEXT,
    image_Dish TEXT,
    restaurant_id_Dish INTEGER NOT NULL,
    FOREIGN KEY(restaurant_id_Dish) REFERENCES Restaurant(id_Restaurant)
)''')

print("Table Dish created successfully")

# Création de la table Orders
cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    id_Orders INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id_Orders INTEGER NOT NULL,
    date_Orders TEXT NOT NULL,
    FOREIGN KEY(user_id_Orders) REFERENCES User(id_User)
)''')

print("Table Orders created successfully")

# Création de la table OrderItem
cursor.execute('''
CREATE TABLE IF NOT EXISTS OrderItem (
    id_OrderItem INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    order_id_OrderItem INTEGER NOT NULL,
    dish_id_OrderItem INTEGER NOT NULL,
    restaurant_id_OrderItem INTEGER NOT NULL,
    quantity_OrderItem INTEGER NOT NULL,
    FOREIGN KEY(order_id_OrderItem) REFERENCES Orders(id_Orders),
    FOREIGN KEY(dish_id_OrderItem) REFERENCES Dish(id_Dish),
    FOREIGN KEY(restaurant_id_OrderItem) REFERENCES Restaurant(id_Restaurant)
)''')

print("Table OrderItem created successfully")

# Création de la table de jonction User_Restaurant pour la relation many-to-many
cursor.execute('''  
CREATE TABLE IF NOT EXISTS User_Restaurant (
    id_UserRestaurant INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id_UserRestaurant INTEGER NOT NULL,
    restaurant_id_UserRestaurant INTEGER NOT NULL,
    FOREIGN KEY(user_id_UserRestaurant) REFERENCES User(id_User),
    FOREIGN KEY(restaurant_id_UserRestaurant) REFERENCES Restaurant(id_Restaurant)
)''')

print("Table User_Restaurant created successfully")

# Création de la table de jonction User_Owns_Restaurant pour la relation many-to-many de possession
cursor.execute('''  
CREATE TABLE IF NOT EXISTS User_Owns_Restaurant (
    id_UserOwnsRestaurant INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id_UserOwnsRestaurant INTEGER NOT NULL,
    restaurant_id_UserOwnsRestaurant INTEGER NOT NULL,
    FOREIGN KEY(user_id_UserOwnsRestaurant) REFERENCES User(id_User),
    FOREIGN KEY(restaurant_id_UserOwnsRestaurant) REFERENCES Restaurant(id_Restaurant)
)''')

print("Table User_Owns_Restaurant created successfully")

# Fermeture de la connexion à la base de données
connection.commit()
connection.close()

print("Database operation completed successfully")
