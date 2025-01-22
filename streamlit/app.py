import streamlit as st
import os
from create_connection import create_connection
from dotenv import load_dotenv
import pandas as pd
import altair as alt
import plotly.graph_objects as go

load_dotenv()

RDS_ENDPOINT = os.getenv("RDS_ENDPOINT")

olap_conn = create_connection("olap", RDS_ENDPOINT)

st.set_page_config(layout="wide")

st.title("Healthcare Provider ETL Dashboard")

app_by_staff_department = """
    SELECT COUNT(appointment_id) as appointment_count, department_name
    FROM fact_appointments JOIN dim_staff ON
    fact_appointments.staff_id = dim_staff.staff_id
    JOIN dim_departments
    ON dim_staff.department_id = dim_departments.department_id
    WHERE appointment_date BETWEEN '2025-01-01' AND '2025-12-31'
    GROUP BY department_name;"""

df_1 = pd.read_sql_query(app_by_staff_department, olap_conn)

col1, col2 = st.columns(2, gap='large')

with col1:
    chart = alt.Chart(df_1).mark_bar().encode(
        x=alt.X('department_name:N', title="Department",
                axis=alt.Axis(labelAngle=-45)),
        y=alt.X('appointment_count:Q', title="Number of Appointments"),
        color=alt.Color('department_name:N', legend=None),
        tooltip=['department_name', 'appointment_count']
    ).properties(
        title="Appointments per Department",
        width=800,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

missed_apps_by_demographic = """SELECT
        COUNT(appointment_id) AS appointment_count,
        CASE
            WHEN EXTRACT(YEAR FROM AGE(NOW(), date_of_birth)) <= 18
            THEN '1. Children 0-18'
            WHEN EXTRACT(YEAR FROM AGE(NOW(), date_of_birth)) <= 28
            THEN '2. Young Adults 19-28'
            WHEN EXTRACT(YEAR FROM AGE(NOW(), date_of_birth)) <= 38
            THEN '3. Adults 29-38'
            WHEN EXTRACT(YEAR FROM AGE(NOW(), date_of_birth)) <= 48
            THEN '4. Middle Aged Adults 39-48'
            WHEN EXTRACT(YEAR FROM AGE(NOW(), date_of_birth)) <= 58
            THEN '5. Older Adults 49-58'
            WHEN EXTRACT(YEAR FROM AGE(NOW(), date_of_birth)) <= 68
            THEN '6. Mature Adults 59-68'
            WHEN EXTRACT(YEAR FROM AGE(NOW(), date_of_birth)) <= 78
            THEN '7. Senior Adult 68+'
            WHEN EXTRACT(YEAR FROM AGE(NOW(), date_of_birth)) > 78
            THEN '8. Eldery 78+'
        END age_demographic
    FROM
        dim_patients
        JOIN fact_appointments
        ON dim_patients.patient_id = fact_appointments.patient_id
    WHERE
        appointment_status = 'missed'
    GROUP BY
        age_demographic
    ORDER BY
        age_demographic;"""

df_2 = pd.read_sql_query(missed_apps_by_demographic, olap_conn)

with col2:
    chart = alt.Chart(df_2).mark_bar().encode(
        x=alt.X('age_demographic:N', title="Demographic",
                axis=alt.Axis(labelAngle=-45)),
        y=alt.X('appointment_count:Q', title="Missed Appointments"),
        color=alt.Color('age_demographic:N', legend=None),
        tooltip=['age_demographic', 'appointment_count']
    ).properties(
        title="Missed Appointments Per Age Group",
        width=800,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

col3, col4 = st.columns(2, gap='large')


missed_apps_by_month = """SELECT
    TO_CHAR(DATE_TRUNC('month', appointment_date), 'Mon') AS month,
    COUNT(
        CASE
            WHEN appointment_status = 'missed' THEN appointment_id
        END
    ) AS missed,
    COUNT(
        CASE
            WHEN appointment_status = 'cancelled' THEN appointment_id
        END
    ) AS cancelled
    FROM
        fact_appointments
    WHERE
        EXTRACT(
            YEAR
            FROM
                appointment_date
        ) = '2025'
    GROUP BY
        DATE_TRUNC('month', appointment_date)
    ORDER BY
        DATE_TRUNC('month', appointment_date);"""

df_3 = pd.read_sql_query(missed_apps_by_month, olap_conn)

df_3_long = df_3.melt(id_vars=['month'],
                      value_vars=['missed', 'cancelled'],
                      var_name='appointment_status',
                      value_name='count')

with col3:
    chart = alt.Chart(df_3_long).mark_line().encode(
        x=alt.X('month:N', title="Month"),
        y=alt.Y('count:Q', title="Appointments"),
        color=alt.Color(
            'appointment_status:N',
            title="Appointment Status",
            scale=alt.Scale(domain=['missed', 'cancelled'],
                            range=['#03dbfc', '#fc0380'])),
            tooltip=['month', 'appointment_status', 'count']
        ).properties(
            title="Missed And Cancelled Appointments in 2025",
            width=600,
            height=400
        )

    st.altair_chart(chart, use_container_width=True)

patients_reporting_flu_like_symptoms_this_month = """SELECT
    COUNT(dim_patients.patient_id) as number_of_patients
FROM
    fact_appointments
    JOIN dim_patients ON fact_appointments.patient_id = dim_patients.patient_id
WHERE
    notes ILIKE ANY (
        ARRAY [
    '%flu%',
    '%temperature%',
    '%sneez%',
    '%congest%',
    '%headache%',
    '%fever%',
    '%fatigue%',
    '%taste%',
    '%cold sweats%']
    )
    AND EXTRACT(
        MONTH
        FROM
            appointment_date
    ) = EXTRACT(
        MONTH
        FROM
            NOW()
    );"""

patients_this_month = """SELECT
    COUNT(dim_patients.patient_id) as number_of_patients
FROM
    fact_appointments
    JOIN dim_patients ON fact_appointments.patient_id = dim_patients.patient_id
WHERE
    EXTRACT(
        MONTH
        FROM
            appointment_date
    ) = EXTRACT(
        MONTH
        FROM
            NOW()
    );"""

number_of_patients_reporting_flu_this_month = pd.read_sql_query(
    patients_reporting_flu_like_symptoms_this_month, olap_conn
    )['number_of_patients'].iloc[0]

number_of_patients_this_month = pd.read_sql_query(
    patients_this_month, olap_conn
    )['number_of_patients'].iloc[0]

percentage_of_patients_reporting_flu_this_month = (
    number_of_patients_reporting_flu_this_month /
    number_of_patients_this_month) * 100

with col4:

    st.markdown("**Patients Reporting Flu Symptoms This Month**",
                unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=percentage_of_patients_reporting_flu_this_month,
        number={'suffix': "%"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "#2196F3", 'thickness': 0.5},
               'steps': [
                        {'range': [0, 33], 'color': '#abde6d'},
                        {'range': [33, 66], 'color': "#f2e477"},
                        {'range': [66, 100], 'color': "#d63845"}
                        ]}
        ))
    fig.update_layout(
        height=375,  # Adjust height
        width=625    # Adjust width
    )

    st.plotly_chart(fig, use_container_width=True)

app_data = """SELECT
    EXTRACT(YEAR FROM appointment_date) AS year,
    COALESCE(SUM(CASE WHEN appointment_status = 'attended'
        THEN 1 ELSE 0 END), 0) AS attended,
    COALESCE(SUM(CASE WHEN appointment_status IN ('missed', 'cancelled')
        THEN 1 ELSE 0 END), 0) AS not_attended
    FROM
        fact_appointments
    GROUP BY
        EXTRACT(YEAR FROM appointment_date)
    ORDER BY
        year;"""

app_df = pd.read_sql_query(app_data, olap_conn)

attended_2025 = app_df[app_df['year'] == 2025]['attended'].values[0]
not_attended_2025 = app_df[app_df['year'] == 2025]['not_attended'].values[0]

attended_2024 = app_df[app_df['year'] == 2024]['attended'].values[0]
not_attended_2024 = app_df[app_df['year'] == 2024]['not_attended'].values[0]

total_apps_not_upcoming_2025 = attended_2024 + attended_2025
percentage_of_apps_attended_2025 = round(
    (attended_2025 / total_apps_not_upcoming_2025)
    * 100, 1)

total_apps_not_upcoming_2024 = attended_2024 + attended_2024
percentage_of_apps_attended_2024 = round(
    (attended_2024 / total_apps_not_upcoming_2024)
    * 100, 1)

percentage_change = round(
    (percentage_of_apps_attended_2025 - percentage_of_apps_attended_2024)
    / percentage_of_apps_attended_2024 * 100, 1)

symbol = '⬆️' if percentage_change > 0 else '⬇️'

col5, col6, col7 = st.columns(3)
with col6:
    with st.container():
        st.markdown(
            f"""
            <div style='text-align: center; font-size: 16px;
            color: white; background-color: #0068C9;padding: 20px;
            border-radius: 10px; max-width: 500px;'>
                <div style='font-size: 40px; font-weight: bold;'>
                    {percentage_of_apps_attended_2025}%
                </div>
                <div style='font-size: 20px; font-weight: bold;'>
                    Appointments Attended This Year<br>
                </div>
                <div style='font-size: 30px; font-weight: bold;'>
                    {symbol} {percentage_change}%
                </div>
                <div style='font-size: 20px; font-weight: bold;'>
                    Compared To Last Year<br>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
