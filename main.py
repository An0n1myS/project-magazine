import base64
import datetime
import secrets

from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
app = Flask(__name__, template_folder="./")
app.secret_key = secrets.token_hex(16)

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='magazine',
        charset='utf8mb4'
    )
    return connection


# функция для проверки, авторизован ли пользователь
def is_logged_in():
    return 'username' in session


# страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            session['username'] = user[1]
            return redirect('/')
        else:
            error = 'Invalid login credentials'
            return render_template('error.html', error=error)
    else:
        return render_template('error.html')


# страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # подключаемся к базе данных
        connection = get_db_connection()
        cursor = connection.cursor()

        # выполняем запрос на добавление пользователя в базу данных
        cursor.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        connection.commit()

        # закрываем соединение с базой данных
        cursor.close()
        connection.close()

        # перенаправляем на главную авторизации
        return redirect('/')
    else:
        return render_template('error.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':

        session.pop('username', None)
        session.pop('user_id', None)

        return redirect('/')
    else:
        return render_template('error.html')


@app.route("/")
def index():
    # подключаемся к базе данных
    conn = pymysql.connect(host='localhost', user='root', password='', db='magazine')
    cursor = conn.cursor()

    # выполняем запрос и получаем список продуктов
    cursor.execute('SELECT * FROM product_type')
    products = cursor.fetchall()

    # закодировать картинку в формат base64
    new_products = []
    for product in products:
        product_image = base64.b64encode(product[2]).decode('utf-8')
        new_product = list(product)
        new_product[2] = product_image
        new_products.append(new_product)

    # закрываем соединение с базой данных
    cursor.close()
    conn.close()

    return render_template("index.html", products=new_products)


@app.route("/product", methods=["GET", "POST"])
def product():
    # подключаемся к базе данных
    conn = pymysql.connect(host='localhost', user='root', password='', db='magazine')
    cursor = conn.cursor()

    cursor.execute('SELECT id, title FROM product_type')
    product_types = cursor.fetchall()

    # получаем список id типов продуктов, которые были выбраны в чекбоксах
    selected_type_ids = request.args.getlist("type_id")

    # если ни один чекбокс не выбран, то выводим все продукты
    if not selected_type_ids:
        cursor.execute('SELECT * FROM product')
    else:   
        # формируем строку с запятыми из выбранных id типов продуктов
        type_ids_str = ",".join(selected_type_ids)

        # выполняем запрос на получение продуктов с выбранными типами
        cursor.execute(f'SELECT * FROM product WHERE id_type IN ({type_ids_str})')

    products = cursor.fetchall()

    # закодировать картинку в формат base64
    new_products = []
    for product in products:
        product_image = base64.b64encode(product[5]).decode('utf-8')
        new_product = list(product)
        new_product[5] = product_image
        new_products.append(new_product)

    # закрываем соединение с базой данных
    cursor.close()
    conn.close()

    return render_template("product.html", products=new_products, product_types=product_types)


# Обработчик запроса на добавление продукта
@app.route('/add_product_type', methods=['POST'])
def add_product_type():
    # Получение данных из формы
    title = request.form['title_type']
    image = request.files['image_type'].read()

    conn = pymysql.connect(host='localhost', user='root', password='', db='magazine')

    # Выполнение запроса на добавление продукта в базу данных
    with conn.cursor() as cursor:
        sql = "INSERT INTO product_type (title, image) VALUES (%s, %s)"
        cursor.execute(sql, (title, image))
        conn.commit()

    cursor.close()
    conn.close()
    # Отправка ответа об успешном добавлении продукта
    return redirect('/add_product')


@app.route('/add_products', methods=['GET', 'POST'])
def add_products():
    conn = pymysql.connect(host='localhost', user='root', password='', db='magazine')
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        count = request.form['count']
        status = request.form['status']
        image = request.files['image']
        image_data = image.read()
        id_type = request.form['type_id']

        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO product (title, price, count, status, image, id_type) VALUES (%s, %s, %s, %s, %s, %s)',
            (title, price, count, status, image_data, id_type))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/add_product')

@app.route('/add_product')
def add_product():
    conn = pymysql.connect(host='localhost', user='root', password='', db='magazine')
    # Выполнение запроса к базе данных для получения списка типов продуктов
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM product_type')
    product_types = cursor.fetchall()

    # Закрытие курсора и соединения с базой данных
    cursor.close()
    conn.close()

    return render_template('templates/add_product.html', product_types=product_types)


@app.route("/shopping_cart")
def shopping_cart():
    if 'username' not in session:
        return redirect('/')

    connection = get_db_connection()
    cursor = connection.cursor()

    # Получаем идентификатор пользователя по его имени из сессии
    cursor.execute('SELECT id FROM user WHERE username = %s', (session['username'],))
    user_id = cursor.fetchone()[0]

    # Получаем список товаров в корзине для данного пользователя
    cursor.execute('''
        SELECT product.id, product.title, product.price, cart_has_product.count
        FROM cart_has_product
        INNER JOIN product ON product.id = cart_has_product.id_product
        INNER JOIN shopping_cart ON shopping_cart.id = cart_has_product.id_cart
        WHERE shopping_cart.id_user = %s
    ''', (user_id,))
    cart_items = cursor.fetchall()

    total = sum([item[2] * item[3] for item in cart_items])

    query = "UPDATE shopping_cart SET total_price = %s WHERE id_user = %s"
    cursor.execute(query, (total, user_id))
    connection.commit()
    cursor.close()
    connection.close()

    return render_template('shopping_cart.html', cart_items=cart_items, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'username' not in session:
        return redirect('/login')

    connection = get_db_connection()
    cursor = connection.cursor()

    # Get user ID from username
    cursor.execute('SELECT id FROM user WHERE username = %s', (session['username'],))
    user_id = cursor.fetchone()[0]

    # Get product information from database
    cursor.execute('SELECT * FROM product WHERE id = %s', (product_id,))
    product = cursor.fetchone()

    # Check if product is in stock
    if product[4] != 'In stock':
        error = 'Product is not in stock'
        return render_template('error.html', error=error)

    # Check if user has an existing shopping cart
    cursor.execute('SELECT * FROM shopping_cart WHERE id_user = %s', (user_id,))
    cart = cursor.fetchone()

    if not cart:
        # Create a new shopping cart for the user
        cursor.execute('INSERT INTO shopping_cart (id_user) VALUES (%s)', (user_id,))
        connection.commit()
        cart_id = cursor.lastrowid
    else:
        # Use the existing shopping cart
        cart_id = cart[0]

    # Add product to shopping cart
    cursor.execute('INSERT INTO cart_has_product (id_cart, id_product, count) VALUES (%s, %s, %s)',
                   (cart_id, product_id, 1))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/shopping_cart')


@app.route('/shopping_cart/remove', methods=['POST'])
def remove_from_cart():
    if 'username' not in session:
        return redirect('/')

    connection = get_db_connection()
    cursor = connection.cursor()

    product_id = int(request.form['product_id'])

    # Получаем идентификатор корзины пользователя
    cursor.execute('SELECT id FROM shopping_cart WHERE id_user = (SELECT id FROM user WHERE username = %s)', (session['username'],))
    cart_id = cursor.fetchone()[0]

    # Удаляем товар из корзины
    cursor.execute('DELETE FROM cart_has_product WHERE id_cart = %s AND id_product = %s', (cart_id, product_id))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect('/shopping_cart')


@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/')

    connection = get_db_connection()
    cursor = connection.cursor()

    # Получаем информацию о пользователе из базы данных
    cursor.execute('SELECT * FROM user WHERE username = %s', (session['username'],))
    user = cursor.fetchone()

    # Получаем историю заказов пользователя из базы данных
    cursor.execute('''
        SELECT orders.id, orders.date, orders.total_price, GROUP_CONCAT(product.title SEPARATOR ', ')
        FROM `orders`
        INNER JOIN order_has_product ON order_has_product.id_order = orders.id
        INNER JOIN product ON product.id = order_has_product.id_product
        INNER JOIN shopping_cart ON shopping_cart.id = orders.id_cart
        INNER JOIN user ON user.id = shopping_cart.id_user
        WHERE user.id = %s
        GROUP BY orders.id
    ''', (user[0],))
    orders = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('profile.html', user=user, orders=orders)


@app.route('/add_cart_to_order', methods=['POST'])
def add_cart_to_order():
    conn = pymysql.connect(host='localhost', user='root', password='', db='magazine')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id FROM shopping_cart WHERE id_user = (SELECT id FROM user WHERE username = %s)',
                       (session['username'],))
        cart_id = int(cursor.fetchone()[0])
        cursor.execute('SELECT id FROM user WHERE username = %s', (session['username'],))
        user_id = int(cursor.fetchone()[0])

        # Получаем информацию о корзине пользователя
        query = "SELECT * FROM shopping_cart WHERE id = %s AND id_user = %s"
        cursor.execute(query, (cart_id, user_id))
        cart = cursor.fetchone()

        if cart is None:
            # Если корзина не найдена, генерируем исключение
            raise ValueError("Cart not found")

        # Создаем новый заказ и сохраняем его в базе данных
        query = "INSERT INTO `orders` (date, total_price, id_cart) VALUES (%s, %s, %s)"
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_price = cart[2]
        cursor.execute(query, (date, total_price, cart_id))
        order_id = cursor.lastrowid

        # Получаем информацию о содержимом корзины и добавляем её в заказ
        query = "SELECT * FROM cart_has_product WHERE id_cart = %s"
        cursor.execute(query, (cart_id),)
        cart_items = cursor.fetchall()

        for item in cart_items:
            # Уменьшаем количество товара на складе на количество товара в заказе
            query = "UPDATE product SET count = count - %s WHERE id = %s"
            cursor.execute(query, (item[2], item[1]))

            # Добавляем товар в заказ
            query = "INSERT INTO order_has_product (id_order, id_product, count) VALUES (%s, %s, %s)"
            cursor.execute(query, (order_id, item[1], item[2]))

        # Удаляем содержимое корзины из базы данных
        query = "DELETE FROM cart_has_product WHERE id_cart = %s"
        cursor.execute(query, (cart_id),)

        # Завершаем транзакцию и сохраняем изменения в базе данных
        conn.commit()
        print("Order successfully created")

        return redirect('/profile')

    finally:
        # Закрываем соединение с базой данных
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
