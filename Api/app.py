from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3

app = Flask(__name__, template_folder='../App/views', static_folder='../App/static')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

def get_cart():
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def add_to_cart(dish_id, quantity):
    cart = get_cart()
    cart.append({'dish_id': dish_id, 'quantity': quantity})
    session['cart'] = cart

def clear_cart():
    session.pop('cart', None)

def get_user_name():
    user_id = session.get('id_Utilisateur')
    if user_id:
        connection = sqlite3.connect('Delicrous.db')
        cursor = connection.cursor()
        cursor.execute('SELECT firstname_User FROM User WHERE id_User=?', (user_id,))
        user_name = cursor.fetchone()
        connection.close()
        if user_name:
            return user_name[0]
    return None

@app.route('/', methods=['GET'])
def home():
    try:
        connection = sqlite3.connect('Delicrous.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name_Campus FROM Campus')
        campus = cursor.fetchall()
        connection.close()
        user_name = get_user_name()
        return render_template('accueil.html', select_campus=campus, user_name=user_name)
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

@app.route('/restaurants-liste', methods=['GET'])
def restaurant():
    try:
        campus_id = request.args.get('campus_id', type=int)
        connection = sqlite3.connect('Delicrous.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name_Restaurant, description_Restaurant, image_logo_Restaurant FROM Restaurant WHERE campus_id_Restaurant=?', (campus_id,))
        restaurant_list = cursor.fetchall()
        connection.close()
        user_name = get_user_name()
        return render_template('restaurants-liste.html', restaurant_list=restaurant_list, user_name=user_name)
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

@app.route('/restaurant-detail', methods=['GET'])
def restaurant_detail():
    try:
        restaurant_name = request.args.get('restaurant_name')
        connection = sqlite3.connect('Delicrous.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name_Restaurant, description_Restaurant, image_logo_Restaurant, image_banner_Restaurant, opening_time_Restaurant, closing_time_Restaurant FROM Restaurant WHERE name_Restaurant=?', (restaurant_name,))
        restaurant = cursor.fetchone()
        cursor.execute('SELECT id_Dish, name_Dish, price_Dish, description_Dish, image_Dish FROM Dish WHERE restaurant_id_Dish=(SELECT id_Restaurant FROM Restaurant WHERE name_Restaurant=?)', (restaurant_name,))
        dish_list = cursor.fetchall()
        connection.close()
        user_name = get_user_name()
        return render_template('restaurant-detail.html', restaurant=restaurant, dish_list=dish_list, user_name=user_name)
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    try:
        if request.method == 'POST':
            mail = request.form.get("mail")
            nom = request.form.get("nom")
            prenom = request.form.get("prenom")
            phone = request.form.get("phone")
            mdp = request.form.get("mdp")
            professional = request.form.get("professional", type=bool)
            scholar = request.form.get("scholar", type=bool)
            connection = sqlite3.connect('Delicrous.db')
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
                                scholar_User
                                ) 
                              VALUES (?, ?, ?, ?, ?, ?, ?);""", 
                              (prenom, nom, mail, phone, mdp, professional, scholar))
            connection.commit()
            connection.close()
            return redirect('/connexion')
        return render_template('register.html')
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    try:
        if request.method == 'POST':
            mail = request.values.get("email")
            mdp = request.values.get("password")
            connection = sqlite3.connect('Delicrous.db')
            cursor = connection.cursor()
            cursor.execute("""SELECT id_User, email_User, password_User FROM User WHERE email_User=?""", (mail,))
            user = cursor.fetchone()
            connection.close()
            if user and user[2] == mdp:
                session['id_Utilisateur'] = user[0]
                return redirect('/')
        return render_template('login.html')
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

@app.route('/order', methods=['GET'])
def order():
    try:
        user_id = session.get('id_Utilisateur')
        if not user_id:
            return redirect('/connexion')

        connection = sqlite3.connect('Delicrous.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT o.id_Orders, o.date_Orders, 
                   GROUP_CONCAT(d.name_Dish || " (x" || oi.quantity_OrderItem || ")") as dishes, 
                   SUM(oi.quantity_OrderItem * d.price_Dish) as total_price
            FROM Orders o
            JOIN OrderItem oi ON o.id_Orders = oi.order_id_OrderItem
            JOIN Dish d ON oi.dish_id_OrderItem = d.id_Dish
            WHERE o.user_id_Orders = ?
            GROUP BY o.id_Orders, o.date_Orders
            ORDER BY o.date_Orders DESC
        ''', (user_id,))

        orders = cursor.fetchall()
        connection.close()
        user_name = get_user_name()
        return render_template('orders.html', orders=orders, user_name=user_name)
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart_route():
    try:
        dish_id = int(request.form.get('dish_id'))
        quantity = int(request.form.get('quantity'))

        if quantity <= 0:
            return redirect(request.referrer)

        add_to_cart(dish_id, quantity)
        return redirect(request.referrer)
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

@app.route('/cart', methods=['GET'])
def cart():
    try:
        cart_items = []
        total_price = 0

        for item in get_cart():
            connection = sqlite3.connect('Delicrous.db')
            cursor = connection.cursor()
            cursor.execute('SELECT name_Dish, price_Dish FROM Dish WHERE id_Dish=?', (item['dish_id'],))
            dish = cursor.fetchone()
            connection.close()

            if dish:
                cart_items.append({'name': dish[0], 'price': dish[1], 'quantity': item['quantity']})
                total_price += dish[1] * item['quantity']

        return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

@app.route('/clear-cart', methods=['POST'])
def clear_cart_route():
    try:
        clear_cart()
        return redirect('/cart')
    except Exception as e:
        # Log the exception e
        return render_template('error.html', error=e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
