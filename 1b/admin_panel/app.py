from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Конфигурация базы данных и загрузки файлов
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Добавьте нужные расширения

db = SQLAlchemy(app)

# Модель для товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

# Функция для проверки разрешенных расширений файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Главная страница с фильтрацией по категории
@app.route('/', methods=['GET', 'POST'])
def index():
    categories = set([product.category for product in Product.query.all()])  # Получаем все уникальные категории
    selected_category = request.args.get('category')  # Получаем выбранную категорию из запроса

    if selected_category:
        products = Product.query.filter_by(category=selected_category).all()
    else:
        products = Product.query.all()

    return render_template('index.html', products=products, categories=categories, selected_category=selected_category)

# Страница добавления товара
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        category = request.form['category']
        image = request.files['image']

        # Проверка расширения файла
        if image and allowed_file(image.filename):
            # Сохраняем изображение
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

            # Добавляем новый товар в базу данных
            new_product = Product(
                name=name,
                price=price,
                quantity=quantity,
                category=category,
                image_url=image_filename  # Храним только имя файла без 'images/'
            )
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')

    return render_template('add_product.html')

# Удаление товара
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/')

# Страница заказов (пока просто заглушка)
@app.route('/orders')
def orders():
    return render_template('orders.html')

# Редактирование товара
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)  # Получаем товар по id

    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        category = request.form['category']
        image = request.files['image']

        # Обработка изображения (если оно новое)
        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join('static/images', image_filename)
            image.save(image_path)
            product.image_url = f'images/{image_filename}'  # Обновляем ссылку на изображение

        # Обновляем другие данные товара
        product.name = name
        product.price = price
        product.quantity = quantity
        product.category = category

        # Сохраняем изменения в базе данных
        db.session.commit()

        return redirect('/')

    return render_template('edit_product.html', product=product)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
