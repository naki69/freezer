import sqlite3
import datetime
import streamlit as st

con = sqlite3.connect('/home/stef/freezer/freezer.db')
cur = con.cursor()

cur.execute(""" SELECT * FROM temp WHERE id  =(SELECT MAX(id) FROM  temp); """)


output = cur.fetchall()
con.close()
output = output[0]
col1, col2, col3, col4 = st.columns(4)

col1.metric("Data Points", output[0])
col2.metric("Days", output[0]/24/60/60)
col3.metric("Last Temp1", output[2])
col4.metric("Last temp2", output[3])
st.write("Last Update: " + output[1])
