from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import UUID

from src import config
from src.report.domain.report_repository import ReportRepository
from src.report.domain.value_objects import ReportStatus, ReportType


@dataclass
class ReportOutput:
    id: UUID
    title: str
    complaint: str
    report_type: ReportType
    name: str
    email: str
    report_status: ReportStatus


@dataclass
class ListReportRequest:
    order_by: str = "title"
    current_page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    search_query: str | None = None


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    total: int = 0


T = TypeVar("T")


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


@dataclass
class ListReportResponse(ListOutput[ReportOutput]):
    pass


class ListReport:
    def __init__(self, repository: ReportRepository) -> None:
        self.repository = repository

    def execute(self, request: ListReportRequest) -> ListReportResponse:
        if request.per_page > config.MAX_PAGINATION_SIZE:
            request.per_page = config.MAX_PAGINATION_SIZE

        reports = self.repository.list(
            request.order_by,
            request.current_page,
            request.per_page,
            request.search_query,
        )

        page_offset = (request.current_page - 1) * request.per_page
        reports_page = reports[page_offset : page_offset + request.per_page]

        return ListReportResponse(
            [
                ReportOutput(
                    id=report.id,
                    name=report.name,
                    email=report.email,
                    title=report.title,
                    complaint=report.complaint,
                    report_type=report.report_type,
                    report_status=report.report_status,
                )
                for report in reports_page
            ],
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=request.per_page,
                total=len(reports),
            ),
        )
