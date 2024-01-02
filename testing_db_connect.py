import mariadb
import sys
import pandas as pd
import streamlit as st

# Connect to MariaDB
try:
    conn = mariadb.connect(
        user=st.secrets.db_credentials.user,
        password=st.secrets.db_credentials.password,
        host=st.secrets.db_credentials.host,
        port=st.secrets.db_credentials.port,
        database=st.secrets.db_credentials.database

    )
except mariadb.Error as e:
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