from dataclasses import dataclass
from uuid import UUID

from src.report.application.use_cases.exceptions import InvalidReport
from src.report.domain.report import Report
from src.report.domain.report_repository import ReportRepository
from src.report.domain.value_objects import ReportStatus, ReportType


@dataclass
class CreateReportRequest:
    title: str
    complaint: str
    report_type: ReportType
    name: str = ""
    email: str = ""
    report_status: ReportStatus = ReportStatus.PENDING


@dataclass
class CreateReportResponse:
    id: UUID


class CreateReport:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    def execute(self, request: CreateReportRequest) -> CreateReportResponse:
        try:
            report = Report(
                title=request.title,
                complaint=request.complaint,
                report_type=request.report_type,
                name=request.name,
                email=request.email,
                report_status=request.report_status,
            )
        except ValueError as err:
            raise InvalidReport(err)

        self.repository.save(report)
        return CreateReportResponse(id=report.id)
