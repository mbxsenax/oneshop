import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Получаем абсолютный путь к папке с проектом
base_dir = os.path.abspath(os.path.dirname(__file__))

# Указываем правильный путь к папке static внутри admin_panel
app = Flask(__name__, template_folder='admin_panel/templates', static_folder='admin_panel/static')


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "admin_panel", "instance", "products.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для товара
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

# Страница с товарами
@app.route('/products', methods=['GET', 'POST'])
def products():
    categories = set([product.category for product in Product.query.all()])  # Получаем все уникальные категории
    selected_category = request.args.get('category')  # Получаем выбранную категорию из запроса

    if selected_category:
        products = Product.query.filter_by(category=selected_category).all()
    else:
        products = Product.query.all()

    return render_template('products_list.html', products=products, categories=categories, selected_category=selected_category)

# Создаем таблицы, если они не существуют
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
