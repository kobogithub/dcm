from tinydb import TinyDB

class documento(dict):
    def __init__(self, *args):
        """
        La clase documento recibe como parametro un diccionario, 
        del que se provee cada uno de los campos de la base de datos,
        el argumento *args solo recibe un diccionario,
        por ejemplo: 
        ---- {'key1':'value1','key2':'value2'} ----\n
        Para modificar una clave solo basta con llamar la funcion 'update'
        y se actualizara en la DB.
        """
        return self.__dict__.update(*args) 

    def __str__(self) -> str:
        return str(self.__dict__)
    
class MyTiny:
    def __init__(self):
        """
        Inicia una instancia para la consulta de base de datos de TinyDB,
        que toma como lectura el archivo db/db.json \n
        La tabla inicializada es 'docs'.
        """
        self.db = TinyDB('db/db.json')
        self.docs = self.db.table('docs')

    def _new_document(self,data) -> int :
        """
        Esta funcion instancia la clase documento, de la cual puede
        insertar documento en la database exportando en dict. \n 
        Retorna el id de dicho documento insertado.
        """
        doc = documento(data)
        id = self.docs.insert(doc.__dict__)
        return id


db = MyTiny()
print(db._new_document({'name':'kevin','lastname':'barroso'}))
