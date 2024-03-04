from pydantic import BaseModel as PydanticBaseModel, Field, ConfigDict
from datetime import datetime
from humps import camelize
from math import ceil
from typing import TypeVar, Generic


T = TypeVar('T')


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True
    )


class EntityBaseModel(BaseModel):
    id: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime


class BaseFilter(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)



class Page(BaseModel, Generic[T]):
    items: list[T]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total_pages: int = Field(ge=0)
    total_elements: int = Field(ge=0)

    def get_page(items: list[T], filter: BaseFilter, total_items: int):
        return Page(
            items=items,
            page=filter.page,
            page_size=filter.page_size,
            total_items=total_items,
            total_pages=ceil(total_items / filter.page_size),
        )
