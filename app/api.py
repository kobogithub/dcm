from tinydb import TinyDB, Query
Doc = Query()

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

    def _new_document(self,data : dict) -> int :
        """
        Esta funcion instancia la clase documento, de la cual puede
        insertar documento en la database exportando en dict. \n 
        Retorna el id de dicho documento insertado.
        """
        doc = documento(data)
        return self.docs.insert(doc.__dict__)
    
    def _get_document(self, NumDoc : str) -> dict:
        """
        Esta funcion comprueba si el documento existe, 
        y lo retorna en una lista.
        """
        doc = self.docs.search(Doc.NumDoc == NumDoc)
        if doc:
            return doc

db = MyTiny()
doc = {
    'NumDoc':'EEPL-CAREM25C-220',
    'Section':'Estructural',
    'Title': 'Linea estructural H - +10',
    'Revs':[
        {
            'Rev': 0,
            'Date': '2022-02-01',
            'OS':250,
            'TotalSheets': 1,
            'Status': 'APROBADO LIBERADO',
            'Sheets':[
                {
                    'Sheet': 1,
                    'Format': 'A1',
                    'Ric':[
                        {
                            'Rev': 'A',
                            'Date':'2022-02-14',
                            'NumNota':[1,2]
                        }
                    ],
                    'DQAs':[
                        {
                            'Nota':1,
                            'NumDoc':'NCO-141',
                            'Status':'PARA EJECUCION',
                            'Verificacion':'SIN EJECUTAR'
                        },
                        {
                            'Nota':2,
                            'NumDoc':'AT-CAREM25OT-104',
                            'Rev':0,
                            'Status':'APROBADO LIBERADO',
                            'Verificacion':'VERIFICADO'
                        }
                    ]
                }
            ]
        }
    ]
}
print(db._get_document('EEPL-CAREM25C-220'))