from uuid import UUID, uuid4

import pytest

from src.report.application.use_cases.list_report import ListReport, ListReportRequest
from src.report.domain.report import Report
from src.report.domain.value_objects import ReportStatus, ReportType
from src.report.infrastructure.in_memory_report_repository import (
    InMemoryReportRepository,
)


class TestListReports:
    @pytest.fixture
    def in_memory_repository(self) -> InMemoryReportRepository:
        return InMemoryReportRepository()

    @pytest.fixture
    def list_report_use_case(self, in_memory_repository) -> ListReport:
        return ListReport(in_memory_repository)

    @pytest.fixture
    def sample_reports(self) -> list[Report]:
        reports = []
        for i in range(10):
            report = Report(
                id=uuid4(),
                name=f"User {i}",
                email=f"user{i}@example.com",
                title=f"Report Title {i}",
                complaint=f"Complaint details {i}",
                report_type=ReportType.DATA_LEAK if i % 2 == 0 else ReportType.OTHER,
                report_status=(
                    ReportStatus.PENDING if i < 5 else ReportStatus.PROCESSING
                ),
            )
            reports.append(report)
        return reports

    def test_list_reports_empty_repository(self, list_report_use_case):
        response = list_report_use_case.execute(ListReportRequest())
        assert len(response.data) == 0
        assert response.meta.total == 0

    def test_list_reports_with_multiple_reports(
        self, list_report_use_case, in_memory_repository, sample_reports
    ):
        for report in sample_reports:
            in_memory_repository.save(report)

        response = list_report_use_case.execute(ListReportRequest())

        assert len(response.data) == 10
        assert response.meta.total == 10
        assert all(isinstance(item.id, UUID) for item in response.data)

    def test_list_reports_pagination(
        self, list_report_use_case, in_memory_repository, sample_reports
    ):
        for report in sample_reports:
            in_memory_repository.save(report)

        # Test first page
        first_page_request = ListReportRequest(current_page=1, per_page=5)
        first_page_response = list_report_use_case.execute(first_page_request)
        assert len(first_page_response.data) == 5
        assert first_page_response.meta.current_page == 1

        # Test second page
        second_page_request = ListReportRequest(current_page=2, per_page=5)
        second_page_response = list_report_use_case.execute(second_page_request)
        assert len(second_page_response.data) == 5
        assert second_page_response.meta.current_page == 2

        # Ensure no overlap between pages
        first_page_ids = {report.id for report in first_page_response.data}
        second_page_ids = {report.id for report in second_page_response.data}
        assert len(first_page_ids.intersection(second_page_ids)) == 0

    def test_list_reports_order_by(self, list_report_use_case, in_memory_repository):
        # Prepare reports with predictable titles for sorting
        sample_reports = [
            Report(
                id=uuid4(),
                title="C Report",
                report_type=ReportType.DATA_LEAK,
                complaint="Complaint C",
            ),
            Report(
                id=uuid4(),
                title="A Report",
                report_type=ReportType.DATA_LEAK,
                complaint="Complaint A",
            ),
            Report(
                id=uuid4(),
                title="B Report",
                report_type=ReportType.DATA_LEAK,
                complaint="Complaint B",
            ),
        ]
        for report in sample_reports:
            in_memory_repository.save(report)

        # Test default order (by title)
        response = list_report_use_case.execute(ListReportRequest())
        titles = [report.title for report in response.data]
        assert titles == ["A Report", "B Report", "C Report"]

    def test_list_reports_search(self, list_report_use_case, in_memory_repository):
        # Prepare reports with varied details for searching
        sample_reports = [
            Report(
                id=uuid4(),
                name="John Doe",
                email="john@example.com",
                title="Technical Issue",
                complaint="Software problem with login",
                report_type=ReportType.DATA_LEAK,
            ),
            Report(
                id=uuid4(),
                name="Jane Smith",
                email="jane@example.com",
                title="General Inquiry",
                complaint="Question about product features",
                report_type=ReportType.DATA_LEAK,
            ),
            Report(
                id=uuid4(),
                name="Mike Wilson",
                email="mike@example.com",
                title="Performance Report",
                complaint="Slow system response",
                report_type=ReportType.DATA_LEAK,
            ),
        ]
        for report in sample_reports:
            in_memory_repository.save(report)

        # Test search by name
        name_search_response = list_report_use_case.execute(
            ListReportRequest(search_query="John")
        )
        assert len(name_search_response.data) == 1
        assert name_search_response.data[0].name == "John Doe"

        # Test search by title
        title_search_response = list_report_use_case.execute(
            ListReportRequest(search_query="Technical")
        )
        assert len(title_search_response.data) == 1
        assert title_search_response.data[0].title == "Technical Issue"

        # Test search by complaint
        complaint_search_response = list_report_use_case.execute(
            ListReportRequest(search_query="login")
        )
        assert len(complaint_search_response.data) == 1
        assert "login" in complaint_search_response.data[0].complaint

        # Test case-insensitive search
        case_insensitive_response = list_report_use_case.execute(
            ListReportRequest(search_query="JANE")
        )
        assert len(case_insensitive_response.data) == 1
        assert case_insensitive_response.data[0].name == "Jane Smith"

        # Test search with no results
        no_results_response = list_report_use_case.execute(
            ListReportRequest(search_query="nonexistent")
        )
        assert len(no_results_response.data) == 0
