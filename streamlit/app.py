import streamlit as st
import os
from setup.setup import create_connection
from dotenv import load_dotenv
import pandas as pd
import altair as alt

load_dotenv()

RDS_ENDPOINT = os.getenv("RDS_ENDPOINT")

olap_conn = create_connection("olap", RDS_ENDPOINT)

st.title("Healthcare Provider ETL Dashboard")

app_by_staff_department = "SELECT COUNT(appointment_id) as appointment_count FROM fact_appointments GROUP BY staff_id;"

app_by_staff_department = "SELECT * FROM mytable;"
df = pd.read_sql_query(app_by_staff_department, olap_conn)

st.write("## Appointments Grouped by Staff Member")
st.dataframe(df)

# Visualize the data
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("staff_id", sort=None, title="Staff ID"),
    y=alt.Y("appointment_count", title="Number of Appointments"),
    color=alt.Color("appointment_count", scale=alt.Scale(scheme="blues"))
).properties(
    width=600,
    height=400,
    title="Appointments by Staff Member"
)