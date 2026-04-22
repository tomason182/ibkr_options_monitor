class PostgreSQLRepository:
    def __init__(self, db):
        self.db = db

    def exists(self, exec_id):
        print("...Checking if id is stored")
        return True

    def save(self, exec_data):
        print("...Saving executions")
        return True
