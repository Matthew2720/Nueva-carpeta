from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    """Metodo constructor de la clase User"""
    def __init__(self,id,username,password,fullname="",rol=str,veterinaria=str,direccion=str,email = str,telefono = str) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.rol = rol
        self.veterinaria = veterinaria
        self.direccion = direccion
        self.email = email
        self.telefono = telefono
        
    @classmethod
    def check_password(self,hashed_password,password):
        """Metodo para verificar el hash de la contraseña"""
        return check_password_hash(hashed_password,password)
    
class Veterinaria(UserMixin):
    #Metodo constructor
    def __init__(self,nombre_vet,ciudad_vet,nombre,apellido, documento, telefono, email):
        self.nombre_vet = nombre_vet
        self.ciudad_vet = ciudad_vet
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.telefono = telefono
        self.email = email
        # self.password = password
