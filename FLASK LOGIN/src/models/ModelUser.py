from .entities.User import User

class ModelUser():
    
    @classmethod
    def login(self,db,user):
        try:
            cursor = db.cursor()
            consulta = "SELECT * FROM USUARIOS where USERNAME = '{}'".format(user.username)
            cursor.execute(consulta)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0],row[1],User.check_password(row[2],user.password),row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.cursor()
            consulta = "SELECT id, username, fullname FROM USUARIOS where id = {}".format(id)
            cursor.execute(consulta)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0],row[1],None,row[2])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    