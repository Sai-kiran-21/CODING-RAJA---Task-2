from flask import Flask, render_template, redirect, url_for, request, session
from models import db, Product, CartItem
from forms import CheckoutForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem(product_id=product.id, quantity=1)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = CartItem.query.all()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        # Process checkout
        session['cart_items'] = []
        return redirect(url_for('home'))
    return render_template('checkout.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
