from random import randint
from datetime import datetime


def insert_patients(oltp_conn):

    oltp_conn.autocommit = True
    cursor = oltp_conn.cursor()

    patients = create_random_patients()
    query = """
    INSERT INTO patients (last_updated, first_name, last_name,
    date_of_birth, sex, height, weight, phone_number, address)
    VALUES (%(last_updated)s, %(first_name)s, %(last_name)s, %(date_of_birth)s,
      %(sex)s, %(height)s, %(weight)s, %(phone_number)s, %(address)s);
    """
    for patient in patients:
        cursor.execute(query, patient)
    print(f"Inserted {len(patients)} patients successfully ✅")
    oltp_conn.commit()
    cursor.close()


def insert_appointments(oltp_conn):

    oltp_conn.autocommit = True
    cursor = oltp_conn.cursor()

    appointments = create_random_appointments()

    query = """INSERT INTO appointments
               (last_updated, appointment_date, appointment_status,
                patient_id, staff_id, notes)
                    VALUES
                    (%(last_updated)s, %(appointment_date)s,
                     %(appointment_status)s, %(patient_id)s,
                     %(staff_id)s, %(notes)s);"""
    for appointment in appointments:
        cursor.execute(query, appointment)
    print(f"Inserted {len(appointments)} appointments successfully ✅")

    oltp_conn.commit()
    cursor.close()


def create_random_appointments():
    appointments = []
    for _ in range(1, 101):
        appointments.append(create_random_appointment())
    return appointments


def create_random_appointment():
    statuses = ['upcoming', 'pending', 'booked', 'scheduled']
    return {
        'last_updated': datetime.now(),
        'appointment_date': create_random_date(),
        'appointment_status': statuses[randint(0, 3)],
        'patient_id': randint(0, 500),
        'staff_id': randint(0, 25),
        'notes': create_random_notes()
    }


def create_random_date():
    year = [datetime.now().year + 1, datetime.now().year + 2][randint(0, 1)]
    month = randint(1, 12)
    day = randint(1, 28)
    hour = randint(9, 16)
    minute = ['00', '15', '30', '45'][randint(0, 3)]
    return f'{year}-{month:02}-{day:02} {hour:02}:{minute:02}:00'


def create_random_notes():
    opening = ["I'm way out of my depth here. The patient feels ",
               "Patient is doing ",
               "They are feeling ",
               "Patient reported feeling ",
               "Reported feeling ",
               "They seem to be doing "][randint(0, 5)]

    adjective = ["great. ", "fine. ", "okay. ", "quite poorly. ",
                 "oddly well despite everything. ",
                 "miracously amazing. ", "not so good. ",
                 "awfully badly. "][randint(0, 7)]

    description = ["They have symptoms including ",
                   "Their symptoms include ",
                   "They are showing signs of ",
                   "They revealed they had experienced "][randint(0, 3)]

    symptoms = ["a mild cough, ", "coughs, sneezes and diseases ",
                "an icky tummy ", "tingly toes ", "shivering ",
                "cold sweats ", "chest pain ", "uncontrollable laughter ",
                "lying down for long periods of time ", "vomiting ",
                "an inability to stop talking ", "a midlife crisis ",
                "mystical experiences ", "intense euphoria "][randint(0, 12)]

    solution = ["so I've recommended taking a brisk walk.",
                "but I've put a wet paper towel on them so it should be fine.",
                "and I've never seen this before!",
                "so I think I'll give them a paracetamol, \
                    and hope they make a swift recovery.",
                "so I will prescribe a course of antibiotics.",
                "which is strange, I will consult my seniors for a diagnosis.",
                "so I'm going to suggest another appointment next week.",
                "which is frightening, they are going to A&E now.",
                "so I think it must be bad."][randint(0, 8)]
    return f'{opening}{adjective}{description}{symptoms}{solution}'


def create_random_patients():
    patients = []
    for _ in range(1, 501):
        patients.append(create_random_patient())
    return patients


def create_random_patient():

    last_updated = datetime.now()

    first_name, sex = create_first_name()

    last_name = create_last_name()

    date_of_birth = create_random_date_of_birth()

    height = create_random_height()

    weight = create_random_weight()

    phone_number = create_random_phone_number()

    address = create_random_address()

    return {'last_updated': last_updated,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'sex': sex,
            'height': height,
            'weight': weight,
            'phone_number': phone_number,
            'address': address}


def create_first_name():

    sex = "female" if randint(0, 1) % 2 == 0 else "male"

    names = {'female': ["Alice", "Daisy", "Fiona", "Hannah", "Ivy", "Katie",
                        "Mia", "Olivia", "Ruby", "Tina", "Uma", "Willow",
                        "Delilah", "Freya", "Hazel", "Isla", "Kylie", "Nina",
                        "Rosie", "Ursula", "Violet", "Xena", "Yvonne", "Amber",
                        "Ella", "Grace", "Iris", "Keria", "Lila", "Nora",
                        "Sophia", "Vanessa", "Ximena", "Yasmin", "Zoe",
                        "Diana", "Faith", "Harper", "Isabelle", "Kayla", "Kat",
                        "Katie", "Katherine", "Liz", "Lizzie", "Elizabeth",
                        "Eliza", "Ellie", "Beth", "Bettie", "Brooke",
                        "Phoebe", "Chloe", "Penny", "Yara"],
             'male': ["Bob", "Charlie", "Ethan", "George", "Jack", "Liam",
                      "Noah", "Paul", "Quinn", "Sam", "Victor", "Xander",
                      "Zane", "Aaron", "Caleb", "Elliot", "Gabriel", "Jacob",
                      "Logan", "Mason", "Oscar", "Quentin", "Sebastian",
                      "Toby", "Wyatt", "Zachary", "Blake", "Dylan", "Finn",
                      "Henry", "James", "Max", "Owen", "Quincy", "Ryan",
                      "Wesley", "Adrian", "Cameron", "Evan", "Gavin", "Jonah",
                      "Lucas", "Thomas"]}

    return names[sex][randint(0, len(names[sex]) - 1)], sex


def create_last_name():
    return [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez",
        "Clark-Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
        "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
        "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera",
        "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
        "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales",
        "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz III", "Morgan",
        "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos",
        "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez",
        "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
        "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
        "Long", "Ross", "Foster", "Jimenez", "Campbell", "Mitchell",
        "Carter",
    ][randint(0, 89)]


def create_random_date_of_birth():
    year = datetime.now().year - randint(16, 100)
    month = randint(1, 12)
    day = randint(1, 28)
    return f'{year}-{month:02}-{day:02}'


def create_random_height():
    metric = "cm" if randint(0, 1) % 2 == 0 else "ft"

    if metric == "cm":
        return f'{randint(155, 201)}cm'
    else:
        return f'{randint(4,6)}\'{randint(0,12)}\"'


def create_random_weight():
    metric = "kg" if randint(0, 1) % 2 == 0 else "lbs"

    if metric == "kg":
        return f'{randint(38, 120)}kg'
    else:
        return f'{randint(84,264)}lbs'


def create_random_phone_number():
    return f'0{randint(1111111111, 9999999999)}'


def create_random_address():
    house_number = randint(1, 99)

    name = [
        "Blossom", "Meadow", "Hillcrest", "Willow", "Elmwood", "Cedar",
        "Riverside", "Parkside", "Maple", "Ash", "Oakwood", "Briar",
        "Pine", "Sycamore", "Haven", "Rosewood", "Sunset", "Spring",
        "Autumn", "Summit", "Cherry", "Magnolia", "Birch", "Valley",
        "Highland", "Aspen", "Lakeview", "Fern", "Woodland", "Clover",
        "Laurel", "Orchard", "Foxglove", "Juniper", "Bluebell", "Holly",
        "Violet", "Peach", "Ivy", "Thistle", "Primrose", "Lilac", "Golden",
        "Poplar", "Evergreen", "Brook", "Winding", "Mulberry", "Daisy",
        "Horizon", "Fieldstone", "Hawthorn", "Garden", "Alder", "Chestnut",
        "Mossy", "Spruce", "Morning", "Bramble", "Amber", "Willowbrook",
        "Crimson", "Sunrise", "Silver", "Glen", "Aspire", "Forest",
        "Wildflower", "Aurora", "Heather", "Marigold", "Boulder", "Creekside",
        "Pebble", "Harmony", "Winterbry", "Cloud", "Meadowbrook", "Stonewall",
        "Lavender", "Moonlight", "Cardinal", "Foxwood", "Snowdrop", "Hearth",
        "Shoreline", "Riverbend", "Goldenrod", "Canyon", "Starling", "Harbor",
        "Autumnwood", "Cypress", "Wisteria", "Birchwood", "Harvest", "Rustic",
        "Clearwater", "Wildrose", "Sparrow"
    ][randint(1, 90)]
    suffix = [
        "Lane", "Street", "Road", "Avenue", "Boulevard", "Drive", "Court",
        "Place", "Terrace", "Circle", "Way", "Alley", "Row", "Path", "Trail",
        "Parkway", "Crescent", "Square", "Loop", "Highway", "Close", "Gardens",
        "Grove", "Meadow", "Walk", "Bypass", "Plaza", "Vista", "Broadway",
        "Promenade", "Causeway", "Esplanade", "Knoll", "Pass", "Quay", "Rise",
        "Hill", "Heights", "Commons", "Turn", "Overpass", "Run", "Crossing",
        "Arcade", "Driveway", "Landing", "Parade", "Outlook", "Spur", "Fork",
        "Bridge", "Depot", "Estate", "Ledge", "Track", "Ridge", "Harbour",
        "Alameda", "Wayfare", "Summit", "Vale", "View", "Field", "Hollow",
        "Park", "Harbor", "Pike", "Pier", "Ramble", "Throughfare", "Territory",
        "Point", "Station", "Passage", "Wharf", "Bluff", "Canyon", "Shore",
        "Landing", "Cape", "Cove", "Bay", "Bend", "Creek", "Chase", "Dale",
        "Glen", "Haven", "Springs", "Terrace"
    ][randint(1, 89)]

    return f'{house_number} {name} {suffix}'
