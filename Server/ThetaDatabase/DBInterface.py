from typing import Optional


class Database:
    """
    Interface for a Database
    """
    def __init__(self, storage_path: str):
        """
        Creates a new Database, with data stored at the given directory path.
        """
        self.path = storage_path

    def table_exists(self, table_name: str) -> bool:
        """
        Returns whether the given table exists.
        :param table_name: str, Name of the table to check
        :return: bool; whether the table exists
        """
        pass

    def create_table(self, table_name: str):
        """
        Creates a new table with the given table name.
        :param table_name: str, Name of the new table
        """
        pass

    def drop_table(self, table_name: str):
        """
        Deletes the table with the given name
        :param table_name: Name of the table to delete
        """
        pass

    def insert(self, table_name: str, entry: dict) -> int:
        """
        Inserts the given entry into the table with the given name.
        Returns the unique ID of the new entry.
        :param table_name: Name of the table to insert to
        :param entry: dictionary, new entry to the given table
        :return: int, unique ID of the new entry.
        """
        pass

    def replace_entry(self, table_name: str, entry_id: int, new_entry: dict):
        """
        Replace the entry with entry_id with new_entry.
        New_entry may contain the 'id' field if it is equal to entry_id
        :param table_name: str, name of the table to replace an entry in
        :param entry_id: int, ID of the entry to replace
        :param new_entry: dict, entry to replace the existing entry with.
                        May optionally contain an 'id' field if it is equal to entry_id
        """

    def get_all_entries(self, table_name: str):
        """
        Returns all entries in the table corresponding to table_name
        :param table_name: Name of the table from which to retrieve all entries
        """
        pass

    def get_entry(self, table_name: str, entry_id: int) -> Optional[dict]:
        """
        Given a table_name, and an entry ID,
        returns the entry with the matching unique ID.
        :param table_name: Name of the table to return an entry from
        :param entry_id: Unique ID of the entry to return
        :return: dict, the entry if it exists in the table. None if it does not.
        """
        pass

    def delete_entry(self, table_name: str, entry_id: int):
        """
        Given a table_name, and an entry ID,
        deletes the entry with the matching unique ID.
        :param table_name: Name of the table to delete an entry from
        :param entry_id: Unique ID of the entry to delete
        """
        pass

    def select(self, table_name: str, key: str, matchval) -> list:
        """
        Given a table_name, a key, and a value to match,
        returns a list containing all entries in the table where the
        value of entry[key] == matchval.
        :param table_name: Name of the table to search
        :param key: Name of the attribute to match
        :param matchval: Value of the attribute to match
        :return: List of all matching entries. Possibly empty.
        """
        pass
