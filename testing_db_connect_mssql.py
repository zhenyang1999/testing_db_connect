import pyodbc

import pandas as pd
import streamlit as st



# Initialize connection.
# Uses st.cache_resource to only run once.



@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + st.secrets.db_mssql.SERVER
        + ";DATABASE="
        + st.secrets.db_mssql.DATABASE
        + ";UID="
        + st.secrets.db_mssql.UID
        + ";PWD="
        + st.secrets.db_mssql.PWD
    )

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from zStationInfo WHERE Station_Code = 1021003;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
    
#st.dataframe(df.head(10))