from distutils.debug import DEBUG


class Config:
    SECRET_KEY = 'MILLAVESECRETA'

class DevelopmentConfig(Config):
    DEBUG = True
    
    
config = {
    'development': DevelopmentConfig
}

direccion_servidor = 'DESKTOP-F9S5AFJ'
nombre_bd = 'FILEPET'
nombre_usuario = 'sa'
password = '123456'