try:
    # Case when imported from outside package
    from ThetaDatabase.DBInterface import Database 
except:
    # Case when ran from this file
    from DBInterface import Database

from typing import Optional
import os
import json
import threading


class ThetaDB(Database):
    """
    Implementation of the Database interface as a system of JSON files.
    In this abstraction, a JSON file is called a "table", and a dictionary
    being stored in that file is called an "entry".

    Docstrings for all methods are in the Database interface
    """

    def __init__(self, storage_path: str):
        super().__init__(storage_path)
        # Lock, for multithreaded applications.
        # If a thread needs to use this database, the lock is acquired to assure
        # consistency
        self._lock = threading.Lock()
        # Create the directory for this database, if it doesn't exist
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    @staticmethod
    def _read_table_file(filepath: str) -> list:
        """
        Static, private helper function
        Read a table from the given file path, return the contained list
        """
        with open(filepath, "r") as f:
            file_data = f.read()
        json_list = json.loads(file_data)
        if type(json_list) is not list:
            raise Exception("Invalid file read: Expected JSON file at " + filepath + " to contain an array.")
        return json_list

    def table_exists(self, table_name: str) -> bool:
        with self._lock:
            return os.path.exists(os.path.join(self.path, table_name + ".json"))

    def create_table(self, table_name: str):
        with self._lock:
            filepath = os.path.join(self.path, table_name + ".json")
            if os.path.exists(filepath):
                raise Exception("Table already exists.")

            with open(filepath, "w") as f:
                f.write("[]")

    def drop_table(self, table_name: str):
        with self._lock:
            filepath = os.path.join(self.path, table_name + ".json")
            if not os.path.exists(filepath):
                raise Exception("Tried to delete a nonexistant table")
            os.remove(filepath)

    def insert(self, table_name: str, entry: dict) -> int:
        with self._lock:
            filepath = os.path.join(self.path, table_name + ".json")
            if not os.path.exists(filepath):
                raise Exception("Tried insert into a nonexistant table")
            if "id" in entry:
                raise Exception("New entry to the table cannot have the field 'id', the id will be automatically assigned.")

            json_list = self._read_table_file(filepath)

            # Find the highest ID in the file. Unique ID for the new entry will be this value + 1
            highest_id: int = 0
            for file_entry in json_list:
                highest_id = max(highest_id, file_entry["id"])
            entry["id"] = highest_id + 1

            json_list.append(entry)
            
            # Write the modified table to file
            with open(filepath, "w") as f:
                f.write(json.dumps(json_list))

            return entry["id"]

    def get_all_entries(self, table_name: str):
        with self._lock:
            filepath = os.path.join(self.path, table_name + ".json")
            if not os.path.exists(filepath):
                raise Exception("Tried get entries from a nonexistant table")

            return self._read_table_file(filepath)

    def get_entry(self, table_name: str, entry_id: int) -> Optional[dict]:
        with self._lock:
            filepath = os.path.join(self.path, table_name + ".json")
            if not os.path.exists(filepath):
                raise Exception("Tried retireve entry from a nonexistant table")

            json_list = self._read_table_file(filepath)

            # Find the entry and return it, if it exists
            for i, file_entry in enumerate(json_list):
                if file_entry["id"] == entry_id:
                    return file_entry
            return None

    def replace_entry(self, table_name: str, entry_id: int, new_entry: dict):
        new_entry_copy = new_entry.copy()
        if ("id" in new_entry_copy):
            if(new_entry_copy["id"] != entry_id):
                raise Exception("Unique ID of new entry does not match the ID of the entry to replace.")
        else:
            # Set the new entry's ID to the appropriate entry ID otherwise
            new_entry_copy["id"] = entry_id

        with self._lock:
            filepath = os.path.join(self.path, table_name + ".json")
            if not os.path.exists(filepath):
                raise Exception("Tried replace entry from a nonexistant table")

            json_list = self._read_table_file(filepath)

            # Find the entry and replace it
            found_entry = False
            for i, file_entry in enumerate(json_list):
                if file_entry["id"] == entry_id:
                    found_entry = True
                    json_list[i] = new_entry_copy
                    break
            if not found_entry:
                raise Exception("Tried to replace a nonexistant entry from " + table_name)

            # Write the modified table to file
            with open(filepath, "w") as f:
                f.write(json.dumps(json_list))

    def delete_entry(self, table_name: str, entry_id: int):
        with self._lock:
            filepath = os.path.join(self.path, table_name + ".json")
            if not os.path.exists(filepath):
                raise Exception("Tried delete entry from a nonexistant table")

            json_list = self._read_table_file(filepath)

            # Find the entry and delete it
            found_entry = False
            for i, file_entry in enumerate(json_list):
                if file_entry["id"] == entry_id:
                    found_entry = True
                    json_list.pop(i)
                    break
            if not found_entry:
                raise Exception("Tried to delete a nonexistant entry from " + table_name)

            # Write the modified table
            with open(filepath, "w") as f:
                f.write(json.dumps(json_list))

    def select(self, table_name: str, key: str, matchval) -> list:
        with self._lock:
            filepath = os.path.join(self.path, table_name + ".json")
            if not os.path.exists(filepath):
                raise Exception("Tried select from a nonexistant table")

            json_list = self._read_table_file(filepath)

            # Find any matching entries and append them to the list
            found_entries = []
            for i, file_entry in enumerate(json_list):
                if file_entry[key] == matchval:
                    found_entries.append(file_entry)

            return found_entries


def main():
    # Test of this database
    print("Test of ThetaDB started\n")
    db: Database = ThetaDB("testdir")

    # Make a table, and insert some entries
    print("\nTest of create_table, insert, and get_all_entries...")
    if db.table_exists("menu_items"):
        raise Exception("Please start the test with an empty test directory (error: testdir contained a table)")
    db.create_table("menu_items")
    db.insert("menu_items", {"name": "Burger", "price_cents": 500})
    db.insert("menu_items", {"name": "Salad", "price_cents": 200})
    all_menu_items = db.get_all_entries("menu_items")
    if len(all_menu_items) == 2:
        print("\tTest successful.")
    else:
        print("\tTest failed.")

    # Insert an entry and get its ID, then retrieve the entry using its ID
    print("\nTest of insert, and get_entry...")
    coffee_entry_id = db.insert("menu_items", {"name": "Coffee", "price_cents": 100})
    coffee_entry = db.get_entry("menu_items", coffee_entry_id)
    if coffee_entry:
        if coffee_entry["id"] == coffee_entry_id and coffee_entry["name"] == "Coffee" \
                and coffee_entry["price_cents"] == 100:
            print("\tTest successful.")
        else:
            print("\tTest failed.")
    else:
        print("\tTest failed, could not find entry after inserting.")

    # Modify an entry, replace it in the table, and then retrieve it.
    print("\nTest of replace_entry")
    coffee_entry["price_cents"] = 200
    db.replace_entry("menu_items", coffee_entry_id, coffee_entry)
    new_coffee_entry = db.get_entry("menu_items", coffee_entry_id)
    if new_coffee_entry:
        if new_coffee_entry["price_cents"] == 200 and new_coffee_entry["id"] == coffee_entry_id:
            print("\tTest successful.")
        else:
            print("\tTest failed.")
    else:
        print("\tTest failed, could not find entry after replacing.")

    # Get all entries in the table with a matching value
    print("\nTest of select")
    two_dollar_items = db.select("menu_items", "price_cents", 200)
    if len(two_dollar_items) == 2 and two_dollar_items[0]["price_cents"] == 200 \
            and two_dollar_items[1]["price_cents"] == 200:
        print("\tTest successful.")
    else:
        print("\tTest failed.")

    # Delete an entry
    print("\nTest of delete_entry")
    db.delete_entry("menu_items", coffee_entry_id)
    # get_entry should return None now that the entry is gone.
    if not db.get_entry("menu_items", coffee_entry_id):
        print("\tTest successful.")
    else:
        print("\tTest failed.")

    # Delete the table
    print("\nTest of drop_table")
    db.drop_table("menu_items")
    # table_exists should now return False
    if not db.table_exists("menu_items"):
        print("\tTest successful.")
    else:
        print("\tTest failed.")


if __name__ == "__main__":
    main()
