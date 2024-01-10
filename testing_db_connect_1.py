import pymysql
import sys
import pandas as pd
import streamlit as st

# Connect to MariaDB
try:
    conn = pymysql.connect(
        user=st.secrets.db_credentials.user,
        password=st.secrets.db_credentials.password,
        host=st.secrets.db_credentials.host,
        port=st.secrets.db_credentials.port,
        db=st.secrets.db_credentials.database

    )
except pymysql.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
#cur = conn.cursor()

@st.cache_data
def query():
    return pd.read_sql( st.secrets.db_query.query_1 , con= conn)

st.title('testing dataframe')
df = query()
st.dataframe(df.head(10))




# import pymysql
# import mysql
# import sys
# import pandas as pd
# import streamlit as st



# # @st.cache_resource
# # def init_connection():
#     # Connect to MariaDB
#     # try:
#     # conn = mysql.connector.connect(user="iotreporter", password="fastbook44", host="192.168.9.230",port=3306, database="IoT")

#     # return  conn
#     # except pymysql.Error as e:
#     #     print(f"Error connecting to MariaDB Platform: {e}")
#     #     sys.exit(1)

# st.write('star')
# conn = st.connection("mydb", type="sql")



# df = conn.query("SELECT * FROM Teltonika_ALLCAN300_Supported_List where id = 1")
# st.dataframe(df)

# # Get Cursor
# #cur = conn.cursor()

# #conn = init_connection()

# # @st.cache_data
# # def query(conn):

# #     return pd.read_sql( st.secrets.db_query.query_1 , con= conn)

# # st.title('testing dataframe')
# # df = query()
# # st.dataframe(df.head(10))



# import streamlit as st
# import numpy as np
# import pandas as pd
# import sqlalchemy
# import pyodbc
# import pymysql


# st.write('start')

# engine = sqlalchemy.create_engine(
#     "mysql://datauser:hotmouse24@192.168.9.230/DataAnalytics"
#     )

# title_df = pd.read_sql('SELECT * FROM Teltonika_ALLCAN300_Supported_List', engine)

# st.dataframe(title_df[0:5])