from ThetaDatabase.DBInterface import Database
from ThetaDatabase.ThetaDB import ThetaDB

class Authentication:
    """
    Handles authentication for the Employee part of the site.
    NOTE: This is insecure, as it stores passwords as PLAIN TEXT.

    Usernames are stored as lowercase, and username inputs to all functions
    are NOT case sensitive.
    So, if user "john" exists, user_exists("JOHN") or user_exists("jOhN")
    should return True
    """

    def __init__(self, db_ref: Database):
        """
        Create a new Authentication object.
        :param db_ref: Reference to the system's Database object.
        """
        self.database = db_ref
        if not self.database.table_exists("users"):
            self.database.create_table("users")
        

    def user_exists(self, username: str) -> bool:
        """
        Returns whether there is a user with the given username
        :param username: Username of the user to check for
        """
        username = username.lower()
        users_with_username = self.database.select("users", "uname", username)
        return len(users_with_username) > 0


    def add_user(self, username: str, password: str):
        """
        Given a username and password, create a new user with this info.
        :param username: Username of new user
        :param password: Password of new user
        """
        username = username.lower()
        if self.user_exists(username):
            raise Exception("Tried to create a user with an existing username")

        user_entry = {"uname": username, "pass": password}
        self.database.insert("users", user_entry)


    def is_login_valid(self, username: str, password: str) -> bool:
        """
        Given a username and password, returns whether they match for a
        user in the system.
        :param username: Username of user to check
        :param password: Password of user to check
        """
        username = username.lower()
        users_with_username = self.database.select("users", "uname", username)
        num_results = len(users_with_username)
        if num_results > 1:
            raise Exception(
                "ERROR: More than one user exists with the same username"
                )
        elif num_results == 1:
            return users_with_username[0]["pass"] == password
        else:
            # No user with that username exists, return false
            return False


def main():
    # Test of Authentication
    test_db: Database = ThetaDB("testdir")
    test_auth = Authentication(test_db)

    # Test of add_user and user_exists
    print("Test of add_user()")
    test_auth.add_user("John", "password123")
    test_auth.add_user("Adil", "thisisacoolpassword")
    # Usernames should NOT be case sensitive
    if test_auth.user_exists("john") and test_auth.user_exists("adil") \
    and test_auth.user_exists("jOhN") and test_auth.user_exists("ADIL"):
        print("\tTest succeeded.")
    else:
        print("\tTest failed.")

    # Test of is_login_valid
    print("Test of is_login_valid()")
    if test_auth.is_login_valid("JoHn", "wrongPASSWORD!"):
        print("\tTest failed.")
    elif test_auth.is_login_valid("john", "PASSWORD123"):
        # Password is the wrong case, should fail
        print("\tTest failed.")
    elif test_auth.is_login_valid("JOHN", "password123"):
        print("\tTest succeeded.")


    test_db.drop_table("users")



if __name__ == "__main__":
    main()


