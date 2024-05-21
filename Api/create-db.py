import sqlite3

# Connexion à la base de données
connection = sqlite3.connect('Delicrous.db')
cursor = connection.cursor()

print("Opened database successfully")

# Création de la table User
cursor.execute('''  
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL, 
    phone TEXT NOT NULL,
    password TEXT NOT NULL,
    professional BOOLEAN NOT NULL,
    scholar BOOLEAN NOT NULL
)''')   

print("Table User created successfully")

# Création de la table Restaurant
cursor.execute('''  
CREATE TABLE IF NOT EXISTS Restaurant (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL
)''')

print("Table Restaurant created successfully")

# Création de la table Dish
cursor.execute('''  
CREATE TABLE IF NOT EXISTS Dish (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL,
    restaurant_id INTEGER NOT NULL,
    FOREIGN KEY(restaurant_id) REFERENCES Restaurant(id)
)''')

print("Table Dish created successfully")

# Création de la table Order
cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES User(id),
    FOREIGN KEY(restaurant_id) REFERENCES Restaurant(id)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS OrderItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    order_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES Orders(id),
    FOREIGN KEY(dish_id) REFERENCES Dish(id)
)''')


# Création de la table de jonction User_Restaurant pour la relation many-to-many
cursor.execute('''  
CREATE TABLE IF NOT EXISTS User_Restaurant (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES User(id),
    FOREIGN KEY(restaurant_id) REFERENCES Restaurant(id)
)''')

print("Table User_Restaurant created successfully")

# Création de la table de jonction User_Owns_Restaurant pour la relation many-to-many de possession
cursor.execute('''  
CREATE TABLE IF NOT EXISTS User_Owns_Restaurant (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES User(id),
    FOREIGN KEY(restaurant_id) REFERENCES Restaurant(id)
)''')

print("Table User_Owns_Restaurant created successfully")

# Fermeture de la connexion à la base de données
connection.commit()
connection.close()

print("Database operation completed successfully")
