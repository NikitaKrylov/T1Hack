from abc import ABC


class BaseFilter(ABC):

    def __call__(self, query, *args, **kwargs):
        raise NotImplementedError


class PagingFilter(BaseFilter):
    limit: int | None = None
    offset: int | None = None

    def __call__(self, query,  *args, **kwargs):
        if self.offset:
            query = query.offset(self.offset)

        if self.limit:
            query = query.limit(self.limit)

        return query
