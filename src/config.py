class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'Andres'
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'api_flask'

config = {
    'development': DevelopmentConfig
}