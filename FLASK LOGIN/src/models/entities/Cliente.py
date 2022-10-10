from flask_login import UserMixin

class Cliente(UserMixin):
    """Esta es la clase de los clientes que hace referencia a la base de datos"""
    
    def __init__(self,id,fullname="",telefono = str,direccion=str,email = str,veterinaria=str) -> None:
        """Metodo constructor

        Args:
            id (_type_): _description_
            fullname (str, optional): _description_. Defaults to "".
            telefono (_type_, optional): _description_. Defaults to str.
            direccion (_type_, optional): _description_. Defaults to str.
            email (_type_, optional): _description_. Defaults to str.
            veterinaria (_type_, optional): _description_. Defaults to str.
        """
        self.id = id
        self.fullname = fullname
        self.veterinaria = veterinaria
        self.direccion = direccion
        self.email = email
        self.telefono = telefono
        
help(Cliente.__init__)