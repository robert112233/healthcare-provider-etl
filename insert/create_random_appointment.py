from datetime import datetime
from random import randint


def create_random_appointment():
    return {
        'last_updated': datetime.now(),
        'appointment_date': create_random_date(),
        'appointment_status': 'upcoming',
        'patient_id': randint(0, 250),
        'staff_id': randint(0, 25),
        'notes': create_random_notes()
    }
    
def create_random_date():
    year = [datetime.now().year + 1, datetime.now().year + 2][randint(0,1)]
    month = randint(1,12)
    day = randint(1,28)
    hour = randint(9, 16) 
    minute = ['00','15','30','45'][randint(0,3)]
    return f'{year}-{month:02}-{day:02} {hour:02}:{minute:02}:00'

def create_random_notes():
    opening = ["I'm way out of my depth here. The patient feels ","Patient is doing ", "They are feeling ", "Patient reported feeling ", "Reported feeling ", "They seem to be doing "][randint(0,5)]
    adjective = ["great. ", "fine. ", "okay. ", "quite poorly. ", "oddly well despite everything. ", "miracously amazing. ", "not so good. ", "awfully badly. "][randint(0,7)]
    description = ["They have symptoms including ", "Their symptoms include ", "They are showing signs of ", "They revealed they had experienced "][randint(0,3)]
    symptoms = ["a mild cough, ", "coughs, sneezes and diseases ", "an icky tummy ", "tingly toes ", "shivering ", "cold sweats ", "chest pain ", "uncontrollable laughter ", "lying down for long periods of time ", "vomiting ", "an inability to stop talking ", "a midlife crisis ", "mystical experiences ", "intense euphoria "][randint(0,12)]
    solution = ["so I've recommended taking a brisk walk.", "but I've put a wet paper towel on them so it should be fine.","and I've never seen this before!", "so I think I'll give them a paracetamol, and hope they make a swift recovery.", "so I will prescribe a course of antibiotics.", "which is strange, I will consult my seniors for a diagnosis.", "so I'm going to suggest another appointment next week.", "which is frightening, they are going to A&E now.", "so I think it must be bad."][randint(0,8)]
    return f'{opening}{adjective}{description}{symptoms}{solution}'
