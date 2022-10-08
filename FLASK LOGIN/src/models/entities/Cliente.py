from flask_login import UserMixin

class Cliente(UserMixin):
    #Metodo constructor
    def __init__(self,id,fullname="",telefono = str,direccion=str,email = str,veterinaria=str) -> None:
        self.id = id
        self.fullname = fullname
        self.veterinaria = veterinaria
        self.direccion = direccion
        self.email = email
        self.telefono = telefono