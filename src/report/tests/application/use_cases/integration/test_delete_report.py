from uuid import uuid4

import pytest

from src.report.application.use_cases.delete_report import (
    DeleteReport,
    DeleteReportRequest,
)
from src.report.application.use_cases.exceptions import ReportNotFound
from src.report.domain.report import Report
from src.report.domain.value_objects import ReportType
from src.report.infrastructure.in_memory_report_repository import (
    InMemoryReportRepository,
)


class TestDeleteReport:
    def test_delete_report_removes_report_from_repository(self):
        report = Report(
            id=uuid4(),
            title="Test Report",
            complaint="Test Complaint",
            report_type=ReportType.DATA_LEAK,
            name="John Doe",
            email="john@example.com",
        )
        repository = InMemoryReportRepository([report])
        delete_report_use_case = DeleteReport(repository)
        request = DeleteReportRequest(id=report.id)

        delete_report_use_case.execute(request)

        assert repository.get_by_id(report.id) is None
        assert len(repository.reports) == 0

    def test_delete_report_multiple_reports(self):
        report1 = Report(
            id=uuid4(),
            title="Report 1",
            complaint="Complaint 1",
            report_type=ReportType.DATA_LEAK,
            name="John Doe",
            email="john@example.com",
        )
        report2 = Report(
            id=uuid4(),
            title="Report 2",
            complaint="Complaint 2",
            report_type=ReportType.DATA_LEAK,
            name="Jane Doe",
            email="jane@example.com",
        )
        repository = InMemoryReportRepository([report1, report2])
        delete_report_use_case = DeleteReport(repository)
        request = DeleteReportRequest(id=report1.id)

        delete_report_use_case.execute(request)

        assert repository.get_by_id(report1.id) is None
        assert repository.get_by_id(report2.id) is not None
        assert len(repository.reports) == 1
        assert repository.reports[0] == report2

    def test_delete_nonexistent_report_raises_exception(self):
        repository = InMemoryReportRepository()
        delete_report_use_case = DeleteReport(repository)
        non_existent_id = uuid4()
        request = DeleteReportRequest(id=non_existent_id)

        with pytest.raises(ReportNotFound) as exc_info:
            delete_report_use_case.execute(request)

        assert str(exc_info.value) == f"Report with {non_existent_id} not found"
        assert len(repository.reports) == 0

    def test_delete_report_multiple_calls_same_report(self):

        report = Report(
            id=uuid4(),
            title="Test Report",
            complaint="Test Complaint",
            report_type=ReportType.DATA_LEAK,
            name="John Doe",
            email="john@example.com",
        )
        repository = InMemoryReportRepository([report])
        delete_report_use_case = DeleteReport(repository)
        request = DeleteReportRequest(id=report.id)

        delete_report_use_case.execute(request)

        assert repository.get_by_id(report.id) is None
        assert len(repository.reports) == 0

        with pytest.raises(ReportNotFound):
            delete_report_use_case.execute(request)
