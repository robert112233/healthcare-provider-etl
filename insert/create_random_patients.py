from random import randint
from datetime import datetime

def create_random_patients():
    patients = []
    for _ in range(1, 501):
        patients.append(create_random_patient())
    print(patients)
    return patients
        

def create_random_patient():

    first_name = create_first_name()

    last_name = create_last_name()
    
    date_of_birth = create_random_date_of_birth()

    phone_number = create_random_phone_number()

    address = create_random_address()

    return {'first_name': first_name, 'last_name': last_name, 'date_of_birth': date_of_birth, 'phone_number': phone_number, 'address': address}


def create_first_name():
    return [
    "Alice", "Bob", "Charlie", "Daisy", "Ethan", "Fiona", "George", "Hannah", "Ivy", "Jack",
    "Katie", "Liam", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Ruby", "Sam", "Tina",
    "Uma", "Victor", "Willow", "Xander", "Yara", "Zane", "Aaron", "Bella", "Caleb", "Delilah",
    "Elliot", "Freya", "Gabriel", "Hazel", "Isla", "Jacob", "Kylie", "Logan", "Mason", "Nina",
    "Oscar", "Penny", "Quentin", "Rosie", "Sebastian", "Toby", "Ursula", "Violet", "Wyatt", "Xena",
    "Yvonne", "Zachary", "Amber", "Blake", "Chloe", "Dylan", "Ella", "Finn", "Grace", "Henry",
    "Iris", "James", "Keira", "Lila", "Max", "Nora", "Owen", "Phoebe", "Quincy", "Ryan",
    "Sophia", "Thomas", "Ulysses", "Vanessa", "Wesley", "Ximena", "Yasmin", "Zoe", "Adrian", "Brooke",
    "Cameron", "Diana", "Evan", "Faith", "Gavin", "Harper", "Isabelle", "Jonah", "Kayla", "Lucas"
    ][randint(0, 89)]


def create_last_name():
    return [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark-Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz III", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"
][randint(0,89)]


def create_random_date_of_birth():
    year = datetime.now().year - randint(16, 100)
    month = randint(1,12)
    day = randint(1,28)
    return f'{year}-{month:02}-{day:02}'


def create_random_phone_number():
    return f'0{randint(1111111111, 9999999999)}'


def create_random_address():
    house_number = randint(1,99)

    name = [
    "Blossom", "Meadow", "Hillcrest", "Willow", "Elmwood", "Cedar", "Riverside", "Parkside", "Maple", "Ash",
    "Oakwood", "Briar", "Pine", "Sycamore", "Haven", "Rosewood", "Sunset", "Spring", "Autumn", "Summit",
    "Cherry", "Magnolia", "Birch", "Valley", "Highland", "Aspen", "Lakeview", "Fern", "Woodland", "Clover",
    "Laurel", "Orchard", "Foxglove", "Juniper", "Bluebell", "Holly", "Violet", "Peach", "Ivy", "Thistle",
    "Primrose", "Lilac", "Golden", "Poplar", "Evergreen", "Brook", "Winding", "Mulberry", "Daisy", "Horizon",
    "Fieldstone", "Hawthorn", "Garden", "Alder", "Chestnut", "Mossy", "Spruce", "Morning", "Bramble", "Amber",
    "Willowbrook", "Crimson", "Sunrise", "Silver", "Glen", "Aspire", "Forest", "Wildflower", "Aurora", "Heather",
    "Marigold", "Boulder", "Creekside", "Pebble", "Harmony", "Winterberry", "Cloud", "Meadowbrook", "Stonewall", "Lavender",
    "Moonlight", "Cardinal", "Foxwood", "Snowdrop", "Hearth", "Shoreline", "Riverbend", "Goldenrod", "Canyon", "Starling",
    "Harbor", "Autumnwood", "Cypress", "Wisteria", "Birchwood", "Harvest", "Rustic", "Clearwater", "Wildrose", "Sparrow"
    ][randint(1,90)]
    suffix = [
    "Lane", "Street", "Road", "Avenue", "Boulevard", "Drive", "Court", "Place", "Terrace", "Circle",
    "Way", "Alley", "Row", "Path", "Trail", "Parkway", "Crescent", "Square", "Loop", "Highway",
    "Close", "Gardens", "Grove", "Meadow", "Walk", "Bypass", "Plaza", "Vista", "Broadway", "Promenade",
    "Causeway", "Esplanade", "Knoll", "Pass", "Quay", "Rise", "Hill", "Heights", "Commons", "Turn",
    "Overpass", "Run", "Crossing", "Arcade", "Driveway", "Landing", "Parade", "Outlook", "Spur", "Fork",
    "Bridge", "Depot", "Estate", "Ledge", "Track", "Ridge", "Harbour", "Alameda", "Wayfare", "Summit",
    "Vale", "View", "Field", "Hollow", "Park", "Harbor", "Pike", "Pier", "Ramble", "Thoroughfare",
    "Territory", "Point", "Station", "Passage", "Wharf", "Bluff", "Canyon", "Shore", "Landing", "Cape",
    "Cove", "Bay", "Bend", "Creek", "Chase", "Dale", "Glen", "Haven", "Springs", "Terrace"
    ][randint(1,89)]

    return f'{house_number} {name} {suffix}'