from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.report.application.use_cases.exceptions import InvalidReport, ReportNotFound
from src.report.application.use_cases.update_report import (
    UpdateReport,
    UpdateReportRequest,
)
from src.report.domain.value_objects import ReportStatus, ReportType


class TestUpdateReport:
    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def existing_report(self):
        report = Mock()
        report.id = uuid4()
        report.title = "Original Title"
        report.complaint = "Original Complaint"
        report.report_type = ReportType.DATA_LEAK
        report.report_status = ReportStatus.PENDING
        report.name = "John Doe"
        report.email = "john@example.com"
        return report

    def test_update_report_success(self, mock_repository, existing_report):
        mock_repository.get_by_id.return_value = existing_report
        update_use_case = UpdateReport(mock_repository)

        update_request = UpdateReportRequest(
            id=existing_report.id,
            title="Updated Title",
            complaint="Updated Complaint",
            report_type=ReportType.SUSPICIOUS_ACTIVITIES,
            report_status=ReportStatus.PROCESSING,
            name="Jane Doe",
            email="jane@example.com",
        )

        update_use_case.execute(update_request)

        mock_repository.update.assert_called_once_with(existing_report)
        existing_report.update_report.assert_called_once_with(
            title="Updated Title",
            complaint="Updated Complaint",
            report_type=ReportType.SUSPICIOUS_ACTIVITIES,
            report_status=ReportStatus.PROCESSING,
            name="Jane Doe",
            email="jane@example.com",
        )

    def test_update_report_partial_update(self, mock_repository, existing_report):
        mock_repository.get_by_id.return_value = existing_report
        update_use_case = UpdateReport(mock_repository)

        update_request = UpdateReportRequest(
            id=existing_report.id, title="Updated Title"
        )

        update_use_case.execute(update_request)

        mock_repository.update.assert_called_once_with(existing_report)
        existing_report.update_report.assert_called_once_with(
            title="Updated Title",
            complaint="Original Complaint",
            report_type=ReportType.DATA_LEAK,
            report_status=ReportStatus.PENDING,
            name="John Doe",
            email="john@example.com",
        )

    def test_update_report_not_found(self, mock_repository):
        non_existent_id = uuid4()
        mock_repository.get_by_id.return_value = None
        update_use_case = UpdateReport(mock_repository)

        update_request = UpdateReportRequest(id=non_existent_id, title="Updated Title")

        with pytest.raises(ReportNotFound) as exc_info:
            update_use_case.execute(update_request)

        assert str(exc_info.value) == f"Report with {non_existent_id} not found"
        mock_repository.update.assert_not_called()

    def test_update_report_invalid_report(self, mock_repository, existing_report):

        mock_repository.get_by_id.return_value = existing_report
        update_use_case = UpdateReport(mock_repository)

        # Simulate update_report method raising ValueError
        existing_report.update_report.side_effect = ValueError("Invalid report update")

        update_request = UpdateReportRequest(
            id=existing_report.id, title="Updated Title"
        )

        with pytest.raises(InvalidReport) as exc_info:
            update_use_case.execute(update_request)

        assert str(exc_info.value) == "Invalid report update"
        mock_repository.update.assert_not_called()

    def test_update_report_no_changes(self, mock_repository, existing_report):
        mock_repository.get_by_id.return_value = existing_report
        update_use_case = UpdateReport(mock_repository)

        update_request = UpdateReportRequest(id=existing_report.id)

        update_use_case.execute(update_request)

        mock_repository.update.assert_called_once_with(existing_report)
        existing_report.update_report.assert_called_once_with(
            title="Original Title",
            complaint="Original Complaint",
            report_type=ReportType.DATA_LEAK,
            report_status=ReportStatus.PENDING,
            name="John Doe",
            email="john@example.com",
        )
