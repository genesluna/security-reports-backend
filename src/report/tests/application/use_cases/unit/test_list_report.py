from unittest.mock import Mock
from uuid import uuid4

import pytest

from src import config
from src.report.application.use_cases.list_report import (
    ListReport,
    ListReportRequest,
    ReportOutput,
)
from src.report.domain.report_repository import ReportRepository
from src.report.domain.value_objects import ReportStatus, ReportType


class MockReport:
    def __init__(
        self,
        id=None,
        name="Test Name",
        email="test@example.com",
        title="Test Title",
        complaint="Test Complaint",
        report_type=ReportType.DATA_LEAK,
        report_status=ReportStatus.PENDING,
    ):
        self.id = id or uuid4()
        self.name = name
        self.email = email
        self.title = title
        self.complaint = complaint
        self.report_type = report_type
        self.report_status = report_status


class TestListReport:
    @pytest.fixture(autouse=True)
    def setup(self, mock_repository):
        self.list_report_use_case = ListReport(mock_repository)
        self.mock_repository = mock_repository

    def test_default_pagination(self):

        mock_reports = [MockReport() for _ in range(15)]
        self.mock_repository.list.return_value = mock_reports

        request = ListReportRequest()
        response = self.list_report_use_case.execute(request)

        assert len(response.data) == config.DEFAULT_PAGINATION_SIZE
        assert response.meta.current_page == 1
        assert response.meta.per_page == config.DEFAULT_PAGINATION_SIZE
        assert response.meta.total == 15
        self.mock_repository.list.assert_called_once_with(
            "title", 1, config.DEFAULT_PAGINATION_SIZE, None
        )

    def test_custom_pagination(self):
        mock_reports = [MockReport() for _ in range(30)]
        self.mock_repository.list.return_value = mock_reports

        request = ListReportRequest(
            current_page=2, per_page=10, order_by="report_type", search_query="test"
        )
        response = self.list_report_use_case.execute(request)

        assert len(response.data) == 10
        assert response.meta.current_page == 2
        assert response.meta.per_page == 10
        assert response.meta.total == 30
        self.mock_repository.list.assert_called_once_with("report_type", 2, 10, "test")

    def test_max_pagination_size(self):
        mock_reports = [MockReport() for _ in range(50)]
        self.mock_repository.list.return_value = mock_reports

        request = ListReportRequest(per_page=config.MAX_PAGINATION_SIZE + 100)
        response = self.list_report_use_case.execute(request)

        assert len(response.data) == config.MAX_PAGINATION_SIZE
        assert response.meta.per_page == config.MAX_PAGINATION_SIZE

    def test_output_mapping(self):
        report_id = uuid4()
        mock_reports = [
            MockReport(
                id=report_id,
                name="John Doe",
                email="john@example.com",
                title="First Report",
                complaint="Detailed complaint",
                report_type=ReportType.DATA_LEAK,
                report_status=ReportStatus.PENDING,
            )
        ]
        self.mock_repository.list.return_value = mock_reports

        request = ListReportRequest()
        response = self.list_report_use_case.execute(request)

        assert len(response.data) == 1
        report_output = response.data[0]
        assert isinstance(report_output, ReportOutput)
        assert report_output.name == "John Doe"
        assert report_output.email == "john@example.com"
        assert report_output.title == "First Report"
        assert report_output.complaint == "Detailed complaint"
        assert report_output.report_type == ReportType.DATA_LEAK
        assert report_output.report_status == ReportStatus.PENDING


@pytest.fixture
def mock_repository():
    repository = Mock(spec=ReportRepository)
    return repository
