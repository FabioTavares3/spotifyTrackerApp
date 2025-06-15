import pandas as pd
import ServerHTTPClass
from insertClass import records_inserter 


if __name__ == "__main__":
    inserter = records_inserter()
    # Insert records into the database
    inserter.insert_records()
    # Start the HTTP server
    server = ServerHTTPClass.HTTPServer()
    server.run()

    

