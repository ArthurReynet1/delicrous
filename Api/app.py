import sqlite3
from flask import Flask, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__, template_folder='App/templates', static_folder='App/static')
app.config['SESSION_TYPE'] = 'filesystem' #pour que les sessions soient stockées dans le système de fichiers (au meme endroit que le programme)
app.config['SESSION_PERMANENT'] = False #pour que les sessions ne soient pas permanentes c'est a dire qu'elles expirent quand le navigateur est fermé
Session(app) #pour initialiser de l'extension flask-session avec les paramètres ci-dessus définis


@app.route('/', methods=['GET'])
def home():
    connection = sqlite3.connect('../Delicrous.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name_Campus FROM Campus')
    campus = cursor.fetchall()
    user_name = cursor.execute('SELECT firstname_User FROM User WHERE id_User=?', (session['id_Utilisateur'],))
    connection.close()
    return render_template('index.html', select_campus=campus, user_name=user_name)

@app.route('/restaurants-liste', methods=['GET'])
def restaurant():
    campus_id = request.args.get('campus_id', type=int)  # Get campus_id from query parameters
    connection = sqlite3.connect('../Delicrous.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name_Restaurant, description_Restaurant, image_logo_Restaurant FROM Restaurant WHERE campus_id_Restaurant=?', (campus_id,))
    restaurant_list = cursor.fetchall()
    user_name = cursor.execute('SELECT firstname_User FROM User WHERE id_User=?', (session['id_Utilisateur'],))
    connection.close()
    return render_template('restaurants-liste.html', restaurant_list=restaurant_list, user_name=user_name)

@app.route('/restaurant-detail', methods=['GET'])
def restaurant_detail():
    restaurant_name = request.args.get('restaurant_name')
    connection = sqlite3.connect('../Delicrous.db')
    cursor = connection.cursor()
    cursor.execute('SELECT name_Restaurant, description_Restaurant, image_logo_Restaurant, image_banner_Restaurant, opening_time_Restaurant, closing_time_Restaurant FROM Restaurant WHERE name_Restaurant=?', (restaurant_name,))
    restaurant = cursor.fetchone()
    cursor.execute('SELECT name_Dish, price_Dish, description_Dish, image_Dish FROM Dish WHERE restaurant_id_Dish=(SELECT id_Restaurant FROM Restaurant WHERE name_Restaurant=?)', (restaurant_name,))
    dish_list = cursor.fetchall()
    user_name = cursor.execute('SELECT firstname_User FROM User WHERE id_User=?', (session['id_Utilisateur'],))
    connection.close()
    return render_template('restaurant-detail.html', restaurant=restaurant, dish_list=dish_list, user_name=user_name)

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        mail = request.form.get("mail")
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        phone = request.form.get("phone")
        mdp = request.form.get("mdp")
        professional = request.form.get("professional", type=bool)
        scholar = request.form.get("scholar", type=bool)
        connection = sqlite3.connect('../Delicrous.db')
        cursor = connection.cursor()
        cursor.execute("SELECT email_User FROM User WHERE email_User=?", (mail,))
        data = cursor.fetchone()
        if data:
            return redirect('/inscription')
        cursor.execute("""INSERT INTO User (
                            firstname_User, 
                            lastname_User, 
                            email_User, 
                            phone_User, 
                            password_User, 
                            professional_User, 
                            scholar_User, 
                            ) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", 
                          (prenom, nom, mail, phone, mdp, professional, scholar, ))
        connection.commit()
        connection.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail=request.values.get("email")
        mdp=request.values.get("password")
        connection=sqlite3.connect('../Delicrous.db')
        cursor=connection.cursor()
        cursor.execute("""SELECT id_User, email_User, password_User FROM User;""")
        data=cursor.fetchall()


        for i in range (len(data)):
            if mail == data[i][1] and mdp == data[i][2]:
                session['id_Utilisateur'] = data[i][0] #enregistrement de l'id de l'utilisateur dans la session
                
        connection.commit()
        connection.close()

        return redirect('/')
    return render_template('login.html') #si methode get on renvoie le model html pour generer la page


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
