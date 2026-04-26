import sqlalchemy
print(sqlalchemy.__file__)
print(sqlalchemy.__version__)
print('has___all__', hasattr(sqlalchemy, '__all__'))
print('dir', dir(sqlalchemy)[:20])
