from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

import json

from pyosint.core.wrapper import Wrapper


app = FastAPI()


class Query(BaseModel):
    search: str
    category: str


@app.post("/search/")
async def perform_search(query: Query) -> Dict:
    with open('test', 'r', encoding='utf-8') as f:
        search_results = json.load(f)
    # search_results = Wrapper(query.search, query.category).handle_parsers()
    return search_results
