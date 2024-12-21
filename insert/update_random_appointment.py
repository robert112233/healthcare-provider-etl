from get_connection import get_connection
from random import randint

def update_random_appointment():
    max_id = get_max_appointment_id()
    random_id = randint(1, max_id)
    random_status = ['cancelled', 'attended', 'missed'][randint(0,2)]
    print(random_id)
    
    connection = get_connection()
    connection.run("""UPDATE appointments
                      SET appointment_status = :random_status, last_updated = NOW()
                      WHERE appointment_id = :random_id AND appointment_status = 'upcoming';
                   """, random_status=random_status, random_id=random_id)
 
def get_max_appointment_id():
    connection = get_connection()
    return (connection.run("SELECT MAX(appointment_id) FROM appointments;")[0][0])
