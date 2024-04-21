from flask import jsonify
from flask_restful import Resource, reqparse, abort
from data import db_session
from data.wishlist import Wishlist

#для одного объекта
class WishlistResource(Resource):
    def get(self, wishlist_id):
        print('1  get one wish')
        abort_if_wishlist_not_found(wishlist_id)
        session = db_session.create_session()
        wishlist = session.query(Wishlist).get(wishlist_id)
        print(wishlist)
        return jsonify({'wishlist': wishlist.to_dict(
            only=('title', 'author', 'genre_id', 'user_id', 'status_id'))})

    def delete(self, wishlist_id):
        abort_if_wishlist_not_found(wishlist_id)
        session = db_session.create_session()
        wishlist = session.query(Wishlist).get(wishlist_id)
        session.delete(wishlist)
        session.commit()
        return jsonify({'success': 'OK'})


class WishlistListResource(Resource):
    def get(self):
        session = db_session.create_session()
        wishlist = session.query(Wishlist).all()
        return jsonify({'wishlist': [item.to_dict(
            only=('title', 'author', 'genre_id', 'status_id')) for item in wishlist]})

    def post(self):
        print('парсинг')
        args = parser.parse_args()
        session = db_session.create_session()
        wishlist = Wishlist(
            title=args['title'],
            author=args['author'],
            genre=args['genre'],
            user_id=args['user_id'],
            status=args['status']
        )
        session.add(wishlist)
        session.commit()
        return jsonify({'id': wishlist.id})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('author', required=True)
parser.add_argument('genre', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('status', required=True)


def abort_if_wishlist_not_found(wishlist_id):
    session = db_session.create_session()
    wishlist = session.query(Wishlist).get(wishlist_id)
    if not wishlist:
        abort(404, message=f"Wishlist {wishlist_id} not found")