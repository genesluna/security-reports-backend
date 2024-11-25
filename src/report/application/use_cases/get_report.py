from dataclasses import dataclass
from uuid import UUID

from src.report.application.use_cases.exceptions import ReportNotFound
from src.report.domain.report_repository import ReportRepository
from src.report.domain.value_objects import ReportStatus, ReportType


@dataclass
class GetReportRequest:
    id: UUID


@dataclass
class GetReportResponse:
    id: UUID
    title: str
    complaint: str
    report_type: ReportType
    name: str
    email: str
    report_status: ReportStatus


class GetReport:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    def execute(self, request: GetReportRequest) -> GetReportResponse:
        report = self.repository.get_by_id(request.id)

        if report is None:
            raise ReportNotFound(f"Report with {request.id} not found")

        return GetReportResponse(
            id=report.id,
            name=report.name,
            email=report.email,
            title=report.title,
            complaint=report.complaint,
            report_type=report.report_type,
            report_status=report.report_status,
        )
