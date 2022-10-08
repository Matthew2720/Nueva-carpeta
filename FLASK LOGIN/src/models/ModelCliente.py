from models.entities.Cliente import Cliente


class ModelCliente():
    @classmethod
    def register(self, db, cliente):
        try:
            cursor = db.cursor()
            consulta = "INSERT into CLIENTE (id_Cliente,nombre_Cliente,tel_Cliente,direccion_Cliente,email_Cliente,fnombrevet_Cliente) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                cliente.id, cliente.fullname,cliente.telefono,cliente.direccion,cliente.email,cliente.veterinaria)
            cursor.execute(consulta)
            cursor.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_users_by_id(self,db,id,centro):
        try:
            cursor = db.cursor()
            consulta = "SELECT * FROM CLIENTE where id_Cliente = '{}' and fnombrevet_Cliente = '{}'".format(id,centro)
            print(consulta)
            cursor.execute(consulta)
            encontradas = cursor.fetchall()
            cursor.close()
            return encontradas
        except Exception as ex:
            raise Exception(ex)
