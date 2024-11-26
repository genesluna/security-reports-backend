from uuid import uuid4

import pytest

from src.report.application.use_cases.exceptions import ReportNotFound
from src.report.application.use_cases.update_report import (
    UpdateReport,
    UpdateReportRequest,
)
from src.report.domain.report import Report
from src.report.domain.value_objects import ReportStatus, ReportType
from src.report.infrastructure.in_memory_report_repository import (
    InMemoryReportRepository,
)


class TestUpdateReport:
    @pytest.fixture
    def existing_report(self):
        return Report(
            id=uuid4(),
            title="Original Title",
            complaint="Original Complaint",
            report_type=ReportType.DATA_LEAK,
            report_status=ReportStatus.PENDING,
            name="John Doe",
            email="john@example.com",
        )

    @pytest.fixture
    def repository(self, existing_report):
        repository = InMemoryReportRepository()
        repository.save(existing_report)
        return repository

    def test_update_report_success(self, repository, existing_report):
        update_use_case = UpdateReport(repository)
        update_request = UpdateReportRequest(
            id=existing_report.id,
            title="Updated Title",
            complaint="Updated Complaint",
            report_type=ReportType.INAPPROPRIATE_PRACTICES,
            report_status=ReportStatus.COMPLETED,
            name="Jane Doe",
            email="jane@example.com",
        )

        update_use_case.execute(update_request)

        updated_report = repository.get_by_id(existing_report.id)
        assert updated_report.title == "Updated Title"
        assert updated_report.complaint == "Updated Complaint"
        assert updated_report.report_type == ReportType.INAPPROPRIATE_PRACTICES
        assert updated_report.report_status == ReportStatus.COMPLETED
        assert updated_report.name == "Jane Doe"
        assert str(updated_report.email) == "jane@example.com"

    def test_update_report_partial_update(self, repository, existing_report):
        update_use_case = UpdateReport(repository)
        update_request = UpdateReportRequest(id=existing_report.id, title="Updated Title")

        update_use_case.execute(update_request)

        updated_report = repository.get_by_id(existing_report.id)
        assert updated_report.title == "Updated Title"
        assert updated_report.complaint == "Original Complaint"
        assert updated_report.report_type == ReportType.DATA_LEAK
        assert updated_report.report_status == ReportStatus.PENDING
        assert updated_report.name == "John Doe"
        assert str(updated_report.email) == "john@example.com"  # expect original email

    def test_update_report_not_found(self, repository):
        update_use_case = UpdateReport(repository)
        non_existent_id = uuid4()
        update_request = UpdateReportRequest(id=non_existent_id, title="Updated Title")

        with pytest.raises(ReportNotFound):
            update_use_case.execute(update_request)

    def test_update_report_no_changes(self, repository, existing_report):
        update_use_case = UpdateReport(repository)
        update_request = UpdateReportRequest(id=existing_report.id)

        update_use_case.execute(update_request)

        updated_report = repository.get_by_id(existing_report.id)
        assert updated_report.title == "Original Title"
        assert updated_report.complaint == "Original Complaint"
        assert updated_report.report_type == ReportType.DATA_LEAK
        assert updated_report.report_status == ReportStatus.PENDING
        assert updated_report.name == "John Doe"
        assert str(updated_report.email) == "john@example.com"
