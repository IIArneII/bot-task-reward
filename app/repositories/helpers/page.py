from sqlalchemy.orm import Query
from typing import TypeVar, Type

from app.services.models.base import Page, BaseFilter


T = TypeVar('T')


def build_page(model: Type[T], query: Query, filter: BaseFilter) -> Page[T]:
    count = query.count()
    elements = query.offset((filter.page - 1) * filter.page_size).limit(filter.page_size).all()
    
    elements = [model.model_validate(e) for e in elements]

    return Page[model].get_page(elements, filter.page, filter.page_size, count)
