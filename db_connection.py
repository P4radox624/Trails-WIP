import mysql.connector
#Database credentials
def connect():
    #try:
        return mysql.connector.connect(
            host="sql.freedb.tech",
            port="3306",
            user="freedb_guest",
            password="N$U22Epa3WAzH?A",
            database="freedb_credentials"
        )
    #except:
        print(ConnectionRefusedError)

