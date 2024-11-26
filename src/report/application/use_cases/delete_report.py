from dataclasses import dataclass
from uuid import UUID

from src.report.application.use_cases.exceptions import ReportNotFound
from src.report.domain.report_repository import ReportRepository


@dataclass
class DeleteReportRequest:
    id: UUID


class DeleteReport:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    def execute(self, request: DeleteReportRequest) -> None:
        report = self.repository.get_by_id(request.id)

        if report is None:
            raise ReportNotFound(f"Report with {request.id} not found")

        self.repository.delete(report.id)
