from sqlalchemy import create_engine
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class DBconnector:

    def get_connection(self):
        # Create a connection to the MySQL database using SQLAlchemy
        return create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                os.getenv("user"), os.getenv("password"), os.getenv("host"), 3306, os.getenv("database"))
            )
    
    def execute_query(self,query, params=None) -> None:
        # Execute a query and return the result as a pandas DataFrame
        if params:
            result = pd.read_sql(query, self.get_connection(), params=params)
        else:
            result = pd.read_sql(query, self.get_connection())
        
        return result
    