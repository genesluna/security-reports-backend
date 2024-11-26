from unittest.mock import Mock

import pytest

from src.report.application.use_cases.create_report import (
    CreateReport,
    CreateReportRequest,
    CreateReportResponse,
)
from src.report.application.use_cases.exceptions import InvalidReport
from src.report.domain.report import Report
from src.report.domain.report_repository import ReportRepository
from src.report.domain.value_objects import ReportStatus, ReportType


class TestCreateReport:
    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=ReportRepository)

    @pytest.fixture
    def create_report_use_case(self, mock_repository):
        return CreateReport(repository=mock_repository)

    def test_create_report_successfully(self, create_report_use_case, mock_repository):
        request = CreateReportRequest(
            title="Test Report",
            complaint="This is a test complaint",
            report_type=ReportType.DATA_LEAK,
            name="John Doe",
            email="john@example.com",
        )

        response = create_report_use_case.execute(request)

        assert isinstance(response, CreateReportResponse)
        assert response.id is not None

        mock_repository.save.assert_called_once()
        saved_report = mock_repository.save.call_args[0][0]
        assert isinstance(saved_report, Report)
        assert saved_report.title == request.title
        assert saved_report.complaint == request.complaint
        assert saved_report.report_type == request.report_type
        assert saved_report.name == request.name
        assert str(saved_report.email) == request.email
        assert saved_report.report_status == ReportStatus.PENDING

    def test_create_report_with_minimal_data(self, create_report_use_case, mock_repository):
        request = CreateReportRequest(
            title="Minimal Report",
            complaint="Minimal complaint",
            report_type=ReportType.DATA_LEAK,
        )

        response = create_report_use_case.execute(request)

        assert isinstance(response, CreateReportResponse)
        assert response.id is not None
        mock_repository.save.assert_called_once()

    def test_create_report_with_invalid_title(self, create_report_use_case):
        request = CreateReportRequest(title="", complaint="Valid complaint", report_type=ReportType.DATA_LEAK)

        with pytest.raises(InvalidReport, match="title cannot be empty"):
            create_report_use_case.execute(request)

    def test_create_report_with_invalid_complaint(self, create_report_use_case):
        request = CreateReportRequest(title="Valid Title", complaint="", report_type=ReportType.DATA_LEAK)

        with pytest.raises(InvalidReport, match="complaint cannot be empty"):
            create_report_use_case.execute(request)

    def test_create_report_with_invalid_email(self, create_report_use_case):
        request = CreateReportRequest(
            title="Email Test Report",
            complaint="Test complaint",
            report_type=ReportType.DATA_LEAK,
            email="invalid-email",
        )

        with pytest.raises(InvalidReport, match="email is not valid"):
            create_report_use_case.execute(request)

    def test_create_report_with_invalid_report_type(self, create_report_use_case):

        request = CreateReportRequest(
            title="Report Type Test", complaint="Test complaint", report_type="INVALID_TYPE"  # type: ignore
        )

        with pytest.raises(InvalidReport, match="report_type must be a valid ReportType"):
            create_report_use_case.execute(request)

    def test_create_report_with_invalid_report_status(self, create_report_use_case):

        request = CreateReportRequest(
            title="Report Type Test", complaint="Test complaint", report_type=ReportType.DATA_LEAK, report_status="INVALID_STATUS"  # type: ignore
        )

        with pytest.raises(InvalidReport, match="report_status must be a valid ReportStatus"):
            create_report_use_case.execute(request)

    def test_create_report_repository_save_error(self, create_report_use_case, mock_repository):
        mock_repository.save.side_effect = Exception("Repository save failed")

        request = CreateReportRequest(
            title="Repository Error Test",
            complaint="Test complaint",
            report_type=ReportType.DATA_LEAK,
        )

        with pytest.raises(Exception, match="Repository save failed"):
            create_report_use_case.execute(request)
