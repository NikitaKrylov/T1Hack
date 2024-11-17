from abc import ABC
from datetime import date
from src.database.models import EntityChanging
from pydantic import BaseModel

class BaseFilter(ABC):

    def __call__(self, query, *args, **kwargs):
        return query


class PagingFilter(BaseFilter, BaseModel):
    limit: int | None = None
    offset: int | None = None

    def __call__(self, query,  *args, **kwargs):
        if self.offset:
            query = query.offset(self.offset)

        if self.limit:
            query = query.limit(self.limit)

        return query


class HistoryDateIntervalFilter(BaseFilter, BaseModel):
    from_date: date | None = None
    to_date: date | None = None

    def __call__(self, query, *args, **kwargs):
        query = super().__call__(query, *args, **kwargs)

        if self.from_date:
            query = query.where(EntityChanging.date >= self.from_date)

        if self.to_date:
            query = query.where(EntityChanging.date <= self.to_date)

        return query


class EntityHistoryFilter(HistoryDateIntervalFilter):
    pass



