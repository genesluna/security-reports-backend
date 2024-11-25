from uuid import uuid4

import pytest

from src.report.domain.report import Report
from src.report.domain.value_objects import ReportType
from src.report.infrastructure.in_memory_report_repository import (
    InMemoryReportRepository,
)


class TestInMemoryReportRepository:
    @pytest.fixture
    def report_repository(self):
        return InMemoryReportRepository()

    @pytest.fixture
    def sample_report(self):
        return Report(
            id=uuid4(),
            title="Test Report",
            complaint="Sample Complaint",
            report_type=ReportType.DATA_LEAK,
            name="John Doe",
            email="john@example.com",
        )

    def test_save_and_get_by_id(self, report_repository, sample_report):
        report_repository.save(sample_report)
        retrieved_report = report_repository.get_by_id(sample_report.id)

        assert retrieved_report is not None
        assert retrieved_report.id == sample_report.id
        assert retrieved_report.title == sample_report.title

    def test_delete(self, report_repository, sample_report):
        report_repository.save(sample_report)
        report_repository.delete(sample_report.id)

        retrieved_report = report_repository.get_by_id(sample_report.id)
        assert retrieved_report is None

    def test_update(self, report_repository, sample_report):
        report_repository.save(sample_report)

        updated_report = Report(
            id=sample_report.id,
            title="Updated Report",
            report_type=ReportType.OTHER,
            complaint="Updated Complaint",
            name="Jane Doe",
            email="jane@example.com",
        )

        report_repository.update(updated_report)
        retrieved_report = report_repository.get_by_id(sample_report.id)

        assert retrieved_report.title == "Updated Report"
        assert retrieved_report.name == "Jane Doe"

    def test_list_without_filters(self, report_repository):
        reports = [
            Report(
                id=uuid4(),
                title="Report 1",
                complaint="Complaint 1",
                report_type=ReportType.DATA_LEAK,
                name="Name 1",
                email="1@example.com",
            ),
            Report(
                id=uuid4(),
                title="Report 2",
                complaint="Complaint 2",
                report_type=ReportType.INAPPROPRIATE_PRACTICES,
                name="Name 2",
                email="2@example.com",
            ),
        ]

        for report in reports:
            report_repository.save(report)

        listed_reports = report_repository.list()
        assert len(listed_reports) == 2

    def test_list_with_search_query(self, report_repository):
        reports = [
            Report(
                id=uuid4(),
                title="Security Report",
                complaint="Network issue",
                report_type=ReportType.DATA_LEAK,
                name="Alice",
                email="alice@example.com",
            ),
            Report(
                id=uuid4(),
                title="Performance Report",
                complaint="Server problem",
                report_type=ReportType.OTHER,
                name="Bob",
                email="bob@example.com",
            ),
        ]

        for report in reports:
            report_repository.save(report)

        security_reports = report_repository.list(search_query="security")
        assert len(security_reports) == 1
        assert security_reports[0].title == "Security Report"

    def test_list_with_order_by(self, report_repository):
        reports = [
            Report(
                id=uuid4(),
                title="B Report",
                complaint="Complaint B",
                report_type=ReportType.DATA_LEAK,
                name="Charlie",
                email="c@example.com",
            ),
            Report(
                id=uuid4(),
                title="A Report",
                complaint="Complaint A",
                report_type=ReportType.SUSPICIOUS_ACTIVITIES,
                name="Alice",
                email="a@example.com",
            ),
        ]

        for report in reports:
            report_repository.save(report)

        ordered_reports = report_repository.list(order_by="title")
        assert len(ordered_reports) == 2
        assert ordered_reports[0].title == "A Report"
        assert ordered_reports[1].title == "B Report"
