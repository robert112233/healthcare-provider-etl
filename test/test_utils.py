from DAGs.utils.create_and_insert_utils import (
    create_random_address, 
    create_random_phone_number, 
    create_random_weight,
    create_random_height,
    create_random_date_of_birth,
    create_last_name,
    create_first_name,
    create_random_patient,
    create_random_patients,
    create_random_notes,
    create_random_date,
    create_random_appointment,
    create_random_appointments
)

import re

class TestCreateRandomAddress:

    def test_address_is_string(self):
        random_address = create_random_address()
        assert isinstance(random_address, str)

    def test_address_starts_with_number(self):
        random_address = create_random_address()
        assert re.search(r"^\d{1,2} \w*", random_address)

class TestRandomPhoneNumber:

    def test_number_is_integer(self):
        random_phone_number = create_random_phone_number()
        assert isinstance(random_phone_number, str)

    def test_number_has_11_digits(self):
        random_phone_number = create_random_phone_number()
        assert len(random_phone_number) == 11

class TestCreateRandomWeight:

    def test_weight_is_string(self):
        random_weight = create_random_weight()
        assert isinstance(random_weight, str)

    def test_weight_is_kg_or_lbs(self):
        random_weight = create_random_weight()
        assert re.search(r"\d{1,3}(kg)|\d{1,3}(lbs)", random_weight)

class TestCreateRandomHeight:

    def test_height_is_string(self):
        random_height = create_random_height()
        assert isinstance(random_height, str)

    def test_height_is_cm_or_ft(self):
        random_height = create_random_height()
        assert re.search(r"\d{1}'\d{1}|\d{2,3}(cm)", random_height)

class TestDateOfBirth:

    def test_date_of_birth_is_string(self):
        random_date_of_birth = create_random_date_of_birth()
        assert isinstance(random_date_of_birth, str)

    def test_height_is_cm_or_ft(self):
        random_date_of_birth = create_random_date_of_birth()
        assert re.search(r"^\d{4}-\d{2}-\d{2}$", random_date_of_birth)

class TestLastName:
    
    def test_last_name_is_string(self):
        random_last_name = create_last_name()
        assert isinstance(random_last_name, str)

class TestFirstName:
    
    def test_first_name_is_tuple(self):
        random_first_name = create_first_name()
        assert isinstance(random_first_name, tuple)

    def test_first_name_contains_name_and_sex(self):
        name, sex = create_first_name()
        assert sex == "male" or sex == "female"
        assert isinstance(name, str)

class TestCreateRandomPatient:

    def test_random_patient_is_dict(self):
        random_patient = create_random_patient()
        assert isinstance(random_patient, dict)

    def test_random_patient_has_correct_structure(self):
        random_patient = create_random_patient()
        assert len(random_patient) == 9
        assert 'last_updated' in random_patient
        assert 'first_name' in random_patient
        assert 'last_name' in random_patient
        assert 'date_of_birth' in random_patient
        assert 'sex' in random_patient
        assert 'height' in random_patient
        assert 'weight' in random_patient
        assert 'phone_number' in random_patient
        assert 'address' in random_patient

class TestCreateRandomPatients:

    def test_random_patients_is_list(self):
        random_patients = create_random_patients()
        assert isinstance(random_patients, list)

    def test_random_patients_are_correctly_structured(self):
        random_patients = create_random_patients()
        for random_patient in random_patients:
            assert 'first_name' in random_patient   

        
class TestCreateRandomNotes:
        
    def test_notes_are_string(self):
        random_notes = create_random_notes()
        assert isinstance(random_notes, str)

class TestCreateRandomDate:

    def test_date_is_str(self):
        random_date = create_random_date()
        assert isinstance(random_date, str)

class TestRandomAppointment:

    def test_appointment_is_dict(self):
        random_appointment = create_random_appointment()
        assert isinstance(random_appointment, dict)

    def test_appointment_is_correctly_structured(self):
        random_appointment = create_random_appointment()
        assert 'last_updated' in random_appointment
        assert 'appointment_date' in random_appointment
        assert 'appointment_status' in random_appointment
        assert 'patient_id' in random_appointment
        assert 'staff_id' in random_appointment
        assert 'notes' in random_appointment

class TestCreateRandomAppointments:

    def test_random_appointments_is_list(self):
        random_appointments = create_random_appointments()
        assert isinstance(random_appointments, list)

    def test_random_appointments_are_correctly_structured(self):
        random_appointments = create_random_appointments()
        for random_patient in random_appointments:
            assert 'patient_id' in random_patient  