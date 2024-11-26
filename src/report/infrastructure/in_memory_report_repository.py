from typing import Optional
from uuid import UUID

from src.report.domain.report import Report
from src.report.domain.report_repository import ReportRepository


class InMemoryReportRepository(ReportRepository):
    def __init__(self, reports: list[Report] = None):
        self.reports: list[Report] = reports or []

    def save(self, report: Report) -> None:
        self.reports.append(report)

    def get_by_id(self, id: UUID) -> Report | None:
        return next((report for report in self.reports if report.id == id), None)

    def delete(self, id: UUID) -> None:
        report = self.get_by_id(id)
        if report:
            self.reports.remove(report)

    def list(
        self,
        order_by: Optional[str] = None,
        current_page: Optional[int] = None,
        per_page: Optional[int] = None,
        search_query: Optional[str] = None,
    ) -> list[Report]:
        # Start with all reports
        filtered_reports = self.reports

        # Apply search query
        if search_query:
            filtered_reports = [
                report
                for report in filtered_reports
                if search_query.lower() in report.title.lower()
                or search_query.lower() in report.complaint.lower()
                or search_query.lower() in report.name.lower()
                or search_query.lower() in str(report.email).lower()
            ]

        # Sort reports
        if order_by:
            # Dynamically sort based on the order_by parameter
            try:
                filtered_reports = sorted(filtered_reports, key=lambda report: getattr(report, order_by))
            except AttributeError:
                # Fallback to original order if attribute doesn't exist
                pass

        return filtered_reports

    def update(self, report: Report) -> None:
        old_report = self.get_by_id(report.id)
        if old_report:
            self.reports.remove(old_report)
            self.reports.append(report)
