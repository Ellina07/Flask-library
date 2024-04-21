import flask
from flask import Flask
from flask import jsonify
from flask import make_response, request

from . import db_session
from .wishlist import Wishlist
from .genre import Genre

blueprint = flask.Blueprint(
    'wishlist_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/wishlist')
def get_wishlist():
    #return "Обработчик в wishlist_api"
    db_sess = db_session.create_session()
    wishlist = db_sess.query(Wishlist).all()
    print(wishlist)
    return jsonify(
        {
            'wishlist':
                [item.to_dict(only=('title', 'author', 'genre_id', 'status_id')) for item in wishlist]
        }
    )
    #response = requests.post(url, headers=headers, json=data)
    #print(response.text)

@blueprint.route('/api/wishlist/<int:wishlist_id>', methods=['GET'])
def get_one_wishlist(wishlist_id):
    print('get one wish')
    db_sess = db_session.create_session()
    wishlist = db_sess.query(Wishlist).get(wishlist_id)
    print(wishlist)
    if not wishlist:
        return make_response(jsonify({'error': 'Not found'}), 404)
        #return make_response({'error': 'Not found'}, 404)
    return jsonify(
        {
            'wishlist': wishlist.to_dict(only=(
                'title', 'author', 'genre_id', 'user_id', 'status_id'))
        }
    )

@blueprint.route('/api/wishlist', methods=['POST'])
def create_wishlist():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['title', 'author', 'user_id', 'genre', 'status']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    wishlist = Wishlist(
        title=request.json['title'],
        author=request.json['author'],
        genre_id=request.json['genre'],
        user_id=request.json['user_id'],
        status_id=request.json['status']
    )
    print(wishlist)
    db_sess.add(wishlist)
    db_sess.commit()
    return jsonify({'id': wishlist.id})

@blueprint.route('/api/wishlist/<int:wishlist_id>', methods=['DELETE'])
def delete_wishlist(wishlist_id):
    db_sess = db_session.create_session()
    wishlist = db_sess.query(Wishlist).get(wishlist_id)
    if not wishlist:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(wishlist)
    db_sess.commit()
    return jsonify({'success': 'OK'})

