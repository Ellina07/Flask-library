import requests
from flask import Flask, render_template, request, make_response, session, redirect, abort, jsonify
from flask_restful import abort, Api
from data import wishlist_resources
from data.genre import Genre
from data.status import Status
from data.wishlist import Wishlist
from data.users import User, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.wishlist import WishlistForm
from forms.user import RegisterForm
from data import db_session, wishlist_api
from forms.wishlist_edit import WishlistEditForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/get_library', methods=['GET', 'POST'])
@login_required
def get_library():
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Библиотеки Казани&format=json"
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        return render_template("index.html", toponym_address=toponym_address)
    else:
        abort(404)
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/wishlist_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def wishlist_delete(id):
    db_sess = db_session.create_session()
    wishlist = db_sess.query(Wishlist).filter(Wishlist.id == id,
                                      Wishlist.user == current_user
                                      ).first()
    if wishlist:
        db_sess.delete(wishlist)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают!!!")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/wishlist',  methods=['GET', 'POST'])
@login_required
def add_wishlist():
    db_sess = db_session.create_session()
    form = WishlistForm()
    genre_list = db_sess.query(Genre).all()
    status_list = db_sess.query(Status).all()
    if form.validate_on_submit():
        wishlist = Wishlist()
        wishlist.title = form.title.data
        wishlist.author = form.author.data
        #было до выпадающего списка
        wishlist.genre_id = form.genre.data
        wishlist.status_id = form.status.data
        current_user.wishlist.append(wishlist)
        db_sess.merge(current_user)
        db_sess.commit()

        return redirect('/')
    return render_template('wishlist.html', title='Добавление книги',
                           form=form, genre_list=genre_list, status_list=status_list)


@app.route('/wishlist/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_wishlist(id):
    form = WishlistEditForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        wishlist = db_sess.query(Wishlist.title, Wishlist.author).filter(Wishlist.id == id,
                                                                                      Wishlist.user == current_user
                                                                                      ).first()
        if wishlist:
            form.title.data = wishlist.title
            form.author.data = wishlist.author
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        wishlist = db_sess.query(Wishlist).filter(Wishlist.id == id,
                                          Wishlist.user == current_user
                                          ).first()
        if wishlist:
            wishlist.title = form.title.data
            wishlist.author = form.author.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('wishlist_edit.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/wishlist_edit_status/<int:id>', methods=['GET', 'POST'])
@login_required
def wishlist_edit_status(id):
    form = WishlistForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        wishlist = db_sess.query(Wishlist.title, Wishlist.author).filter(Wishlist.id == id,
                                                                                      Wishlist.user == current_user
                                                                                      ).first()
        status_list = db_sess.query(Status).all()
        if wishlist:
            form.title.data = wishlist.title
            form.author.data = wishlist.author
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        wishlist = db_sess.query(Wishlist).filter(Wishlist.id == id,
                                          Wishlist.user == current_user
                                          ).first()
        if wishlist:
            wishlist.title = form.title.data
            wishlist.author = form.author.data
            wishlist.status_id = form.status.data
            # для выпадающего списка
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('wishlist_edit_status.html',
                           title='Редактирование новости',
                           form=form, status_list=status_list
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        wishlist = db_sess.query(Wishlist).filter(
            (Wishlist.user == current_user))
    else:
        wishlist = []
    return render_template("index.html", wishlist=wishlist, filename='books.jpg')


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


def main():
    db_session.global_init("db/books.db")
    app.register_blueprint(wishlist_api.blueprint)


    api.add_resource(wishlist_resources.WishlistListResource, '/api/v2/wishlist')

    # для одного объекта
    api.add_resource(wishlist_resources.WishlistResource, '/api/v2/wishlist/<int:wishlist_id>')

    app.run()


if __name__ == '__main__':
    main()