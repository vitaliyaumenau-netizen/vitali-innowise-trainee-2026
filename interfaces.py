from typing import Protocol, Any

class BatchInserter(Protocol):
    def execute_batch_insert(self, query: str, data: list[dict[str, Any]]) -> None:
        pass

class QueryExecutor(Protocol):
    def execute_query(self, query: str, params: tuple[Any, ...] | None = None) -> tuple:
        pass

class CreateTable(Protocol):
    def execute_create_request(self, query: str) -> None:
        pass