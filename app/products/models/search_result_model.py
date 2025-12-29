"""
Search result model for representing paginated product search results.
"""

from pydantic import BaseModel
from typing import List, Dict

class SearchResult(BaseModel):
    total_results: int
    current_page: int
    per_page: int
    total_pages: int
    products: List[Dict]
```