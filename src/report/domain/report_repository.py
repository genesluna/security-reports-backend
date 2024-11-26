from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.report.domain.report import Report


class ReportRepository(ABC):
    @abstractmethod
    def save(self, report: Report):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Report | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        order_by: Optional[str] = None,
        current_page: Optional[int] = None,
        per_page: Optional[int] = None,
        search_query: Optional[str] = None,
    ) -> list[Report]:
        raise NotImplementedError

    @abstractmethod
    def update(self, report: Report) -> None:
        raise NotImplementedError
