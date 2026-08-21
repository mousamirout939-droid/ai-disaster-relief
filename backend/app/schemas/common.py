from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def build(cls, items: list, total: int, page: int, page_size: int):
        total_pages = (total + page_size - 1) // page_size if page_size else 0
        return cls(items=items, total=total, page=page, page_size=page_size, total_pages=total_pages)


class MessageResponse(BaseModel):
    detail: str


class GeoPointIn(BaseModel):
    longitude: float
    latitude: float
