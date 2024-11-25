from dataclasses import dataclass
from uuid import UUID

from src.report.application.use_cases.exceptions import InvalidReport, ReportNotFound
from src.report.domain.report_repository import ReportRepository
from src.report.domain.value_objects import ReportStatus, ReportType


@dataclass
class UpdateReportRequest:
    id: UUID
    title: str | None = None
    complaint: str | None = None
    report_type: ReportType | None = None
    name: str | None = None
    email: str | None = None
    report_status: ReportStatus | None = None


class UpdateReport:
    def __init__(self, repository: ReportRepository):
        self.repository = repository

    def execute(self, request: UpdateReportRequest) -> None:
        report = self.repository.get_by_id(request.id)

        if report is None:
            raise ReportNotFound(f"Report with {request.id} not found")

        try:
            current_title = report.title
            current_complaint = report.complaint
            current_report_type = report.report_type
            current_report_status = report.report_status
            current_name = report.name
            current_email = report.email

            if request.title is not None:
                current_title = request.title

            if request.complaint is not None:
                current_complaint = request.complaint

            if request.report_type is not None:
                current_report_type = request.report_type

            if request.report_status is not None:
                current_report_status = request.report_status

            if request.name is not None:
                current_name = request.name

            if request.email is not None:
                current_email = request.email

            report.update_report(
                title=current_title,
                complaint=current_complaint,
                report_type=current_report_type,
                report_status=current_report_status,
                name=current_name,
                email=current_email,
            )

        except ValueError as error:
            raise InvalidReport(error)

        self.repository.update(report)
