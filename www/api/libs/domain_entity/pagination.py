from typing import Optional
from dataclasses import dataclass


@dataclass
class Pagination:
    page: int
    per_page: int
    total: Optional[int] = None
    total_pages: Optional[int] = None
    data: Optional[list] = None
