from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

from pyosint.core.wrapper import Wrapper


app = FastAPI()


class Query(BaseModel):
    search: str
    category: str


@app.post("/search/")
async def perform_search(query: Query) -> Dict:
    search_results = Wrapper(query.search, query.category).handle_parsers()
    return search_results
