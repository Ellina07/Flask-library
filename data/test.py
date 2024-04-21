from requests import get, post, delete
print(get('http://localhost:5000/api/wishlist').json())

print(get('http://localhost:5000/api/wishlist/4').json())

print(get('http://localhost:5000/api/wishlist/999').json())

print(post('http://localhost:5000/api/wishlist', json={}).json())

print(post('http://localhost:5000/api/wishlist',
           json={'title': 'Заголовок'}).json())

print(post('http://localhost:5000/api/wishlist',
           json={'title': 'Название книги1',
                 'author': 'Автор книги1',
                 'genre': 'Классика',
                 'user_id': 1,
                 'status': 'Прочитано'}).json())

print(delete('http://localhost:5000/api/wishlist/999').json())

print(delete('http://localhost:5000/api/wishlist/22').json())
