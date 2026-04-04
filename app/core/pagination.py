from fastapi import Query

class Pagination:
    def __init__(
        self,
        skip:  int = Query(default=0,   ge=0,   description="Number of records to skip"),
        limit: int = Query(default=20,  ge=1,   le=100, description="Number of records to return"),
    ):
        self.skip  = skip
        self.limit = limit