import pymysql
import sys
import pandas as pd
import streamlit as st


st.title('testing dataframe')

# # Connect to MariaDB

# @st.cache_resource
# def init_connection():
#     return pymysql.connect(user=st.secrets.db_credentials.user,password=st.secrets.db_credentials.password,host=st.secrets.db_credentials.host,port=st.secrets.db_credentials.port,database=st.secrets.db_credentials.database)


# Get Cursor
#cur = conn.cursor()

# @st.cache_data
# def query():
#     return pd.read_sql( st.secrets.db_query.query_1 , con= conn)

conn = st.connection("mydb", type="sql", autocommit=True)
df = conn.query( st.secrets.db_query.query_1)
st.dataframe(df.head(10))
st.write('Done')
