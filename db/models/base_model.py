from db.connection import DBConnectionService
from pydantic import BaseModel

class DBModel:

    @classmethod
    def read(cls, columns = None, **kwargs):
        db_cursor = DBConnectionService().connection.cursor()

        values_to_query_for = []
        for key,value in kwargs.items():
            values_to_query_for.append(f'{key}={value}')

        db_cursor.execute(f"SELECT {', '.join(columns) if columns else '*'} FROM { cls.table } WHERE { ' AND '.join(values_to_query_for)  if kwargs else '' } ")
        results = db_cursor.fetchall()

        del DBConnectionService().connection
        return results

    @classmethod
    def delete():
        ...

    @classmethod
    def write(cls, data):
        data_in_dictionary = data.dict()

        keys = data_in_dictionary.keys()
        values = data_in_dictionary.values()

        db_connection = DBConnectionService().connection
        query = f"INSERT INTO {cls.table}({', '.join(keys)}) VALUES ({'?, ' * (len(values) - 1)} ?)"

        db_connection.cursor().execute(query, tuple(values))
        db_connection.commit()
        del DBConnectionService().connection

    @classmethod
    def create(cls):
        pass
        db_connection = DBConnectionService().connection
        query = f"CREATE TABLE {cls.table}"


