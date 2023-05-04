import sqlite3
import json
from models import Location, Animal, Employee

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]


def get_all_locations():
    
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address,
            e.id employee_id,
            e.name employee_name,
            e.address employee_address,
            e.location_id employee_location_id,
            a.id animal_id,
            a.name animal_name,
            a.breed animal_breed,
            a.status animal_status,
            a.location_id animal_location_id,
            a.customer_id animal_customer_id
        FROM Location l
        JOIN Employee e
            ON l.id = e.location_id
        JOIN Animal a
            ON l.id = a.location_id
        """)

        # Initialize an empty list to hold all animal representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            location = Location(row['id'], row['name'],
                                row['address'])
            
            employee = Employee(row['employee_id'],row['employee_name'], row['employee_address'], row['employee_location_id'])
            
            animal = Animal(row['animal_id'], row['animal_name'], row['animal_breed'],
                            row['animal_status'], row['animal_location_id'], row['animal_customer_id'])
           
            location.employee = employee.__dict__
            
            location.animal = animal.__dict__
            
            locations.append(location.__dict__) # see the notes below for an explanation on this line of code.

    return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address,
            e.id employee_id,
            e.name employee_name,
            e.address employee_address,
            e.location_id employee_location_id,
            a.id animal_id,
            a.name animal_name,
            a.breed animal_breed,
            a.status animal_status,
            a.location_id animal_location_id,
            a.customer_id animal_customer_id
        FROM Location l
        JOIN Employee e
            ON l.id = e.location_id
        JOIN Animal a
            ON l.id = a.location_id
        """)

        # Initialize an empty list to hold all animal representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for data in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            location = Location(data['id'], data['name'],
                                data['address'])

            employee = Employee(data['employee_id'],
                data['employee_name'], data['employee_address'], data['employee_location_id'])

            animal = Animal(data['animal_id'], data['animal_name'], data['animal_breed'], data['animal_status'],
                            data['animal_location_id'], data['animal_customer_id'])

            location.employee = employee.__dict__

            location.animal = animal.__dict__

            # see the notes below for an explanation on this line of code.
            locations.append(location.__dict__)

        return location.__dict__


def create_location(location):
    # Get the id value of the last animal in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    location["id"] = new_id

    # Add the animal dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location

def delete_location(id):
    # Initial -1 value for animal index, in case one isn't found
    location_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the animal. Store the current index.
            location_index = index

    # If the animal was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)
        
def update_location(id, new_location):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the animal. Update the value.
            LOCATIONS[index] = new_location
            break
