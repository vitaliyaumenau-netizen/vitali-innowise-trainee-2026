from interfaces import CreateTable


class CreateDatabaseRequest:
    def __init__(self, creator: CreateTable) -> None:
        self.creator = creator

    def execute_create_request(self, query: str) -> None:
        self.creator.execute_create_request(query)