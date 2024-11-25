from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.report.application.use_cases.exceptions import ReportNotFound
from src.report.application.use_cases.get_report import (
    GetReport,
    GetReportRequest,
    GetReportResponse,
)
from src.report.domain.report_repository import ReportRepository
from src.report.domain.value_objects import ReportStatus, ReportType


class TestGetReport:
    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=ReportRepository)

    @pytest.fixture
    def sample_report_entity(self):
        return Mock(
            id=uuid4(),
            name="John Doe",
            email="john.doe@example.com",
            title="Sample Report",
            complaint="This is a test complaint",
            report_type=ReportType.DATA_LEAK,
            report_status=ReportStatus.PENDING,
        )

    def test_successful_report_retrieval(self, mock_repository, sample_report_entity):
        mock_repository.get_by_id.return_value = sample_report_entity
        use_case = GetReport(mock_repository)
        request = GetReportRequest(id=sample_report_entity.id)

        response = use_case.execute(request)

        assert isinstance(response, GetReportResponse)
        assert response.id == sample_report_entity.id
        assert response.name == sample_report_entity.name
        assert response.email == sample_report_entity.email
        assert response.title == sample_report_entity.title
        assert response.complaint == sample_report_entity.complaint
        assert response.report_type == sample_report_entity.report_type
        assert response.report_status == sample_report_entity.report_status

        mock_repository.get_by_id.assert_called_once_with(sample_report_entity.id)


class TestGetReportErrorHandling:
    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=ReportRepository)

    def test_report_not_found(self, mock_repository):
        non_existent_id = uuid4()
        mock_repository.get_by_id.return_value = None
        use_case = GetReport(mock_repository)
        request = GetReportRequest(id=non_existent_id)

        with pytest.raises(ReportNotFound) as exc_info:
            use_case.execute(request)

        assert str(non_existent_id) in str(exc_info.value)
        mock_repository.get_by_id.assert_called_once_with(non_existent_id)


class TestGetReportVariations:
    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=ReportRepository)

    @pytest.mark.parametrize("report_type", list(ReportType))
    def test_different_report_types(self, mock_repository, report_type):
        report_entity = Mock(
            id=uuid4(),
            name="Test User",
            email="test@example.com",
            title="Type-specific Report",
            complaint="Testing different report types",
            report_type=report_type,
            report_status=ReportStatus.PENDING,
        )
        mock_repository.get_by_id.return_value = report_entity
        use_case = GetReport(mock_repository)
        request = GetReportRequest(id=report_entity.id)

        response = use_case.execute(request)

        assert response.report_type == report_type

    @pytest.mark.parametrize("report_status", list(ReportStatus))
    def test_different_report_statuses(self, mock_repository, report_status):
        report_entity = Mock(
            id=uuid4(),
            name="Status Test User",
            email="status@example.com",
            title="Status-specific Report",
            complaint="Testing different report statuses",
            report_type=ReportType.DATA_LEAK,
            report_status=report_status,
        )
        mock_repository.get_by_id.return_value = report_entity
        use_case = GetReport(mock_repository)
        request = GetReportRequest(id=report_entity.id)

        response = use_case.execute(request)

        assert response.report_status == report_status
