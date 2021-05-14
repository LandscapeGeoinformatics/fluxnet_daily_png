from pyhocon import ConfigFactory
import pyodbc
import urllib.parse


def fields():
    conf = ConfigFactory.parse_file("tables.conf")

    database = conf.get("db.database")
    server = conf.get_string("db.server")
    port = conf["db.port"]  #
    username = conf["db"]["username"]
    password = conf.get_config("db")["password"]

    return {
        "database" : database,
        "server" : server,
        "port" : port,
        "username" : username,
        "password" : password
    }

def conn_string():
    d = fields()
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:"+d['server']+";PORT="+d['port']+";UID="+d['username']+";PWD="+d['password']+";DATABASE="+d['database']
    return conn_str


def conn_uri():
    conn_str = conn_string()
    conn_str_quoted = urllib.parse.quote_plus(conn_str)
    connection_uri = 'mssql+pyodbc:///?odbc_connect={}'.format(conn_str_quoted)
    return connection_uri


if __name__ == "__main__":

    conn = pyodbc.connect(conn_string() )
    cur = conn.cursor()

    cur.execute("SELECT @@version;")

    for rows in cur.fetchone():
        print(rows)
