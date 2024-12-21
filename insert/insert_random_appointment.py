from get_connection import get_connection
from create_random_appointment import create_random_appointment

def insert_random_appointment():
    connection = get_connection()
    appointment_values = create_random_appointment()
    query = """INSERT INTO appointments (last_updated, appointment_date, appointment_status, patient_id, staff_id, notes) 
                      VALUES
                      (:last_updated, :appointment_date, :appointment_status, :patient_id, :staff_id, :notes)"""
    connection.run(query, **appointment_values)
    print('random appointment inserted 🎲')
    
