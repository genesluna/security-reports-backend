from unittest.mock import Mock
from uuid import uuid4

import pytest

from src.report.application.use_cases.delete_report import (
    DeleteReport,
    DeleteReportRequest,
)
from src.report.application.use_cases.exceptions import ReportNotFound
from src.report.domain.report_repository import ReportRepository


@pytest.fixture
def mock_report():
    class MockReport:
        def __init__(self, id):
            self.id = id

    return MockReport(uuid4())


class TestDeleteReport:
    def test_delete_report_successful(self, mock_report):
        mock_repository = Mock(spec=ReportRepository)
        mock_repository.get_by_id.return_value = mock_report

        delete_report_use_case = DeleteReport(mock_repository)
        request = DeleteReportRequest(id=mock_report.id)

        delete_report_use_case.execute(request)

        mock_repository.get_by_id.assert_called_once_with(mock_report.id)
        mock_repository.delete.assert_called_once_with(mock_report.id)

    def test_delete_report_not_found(self):
        non_existent_id = uuid4()
        mock_repository = Mock(spec=ReportRepository)
        mock_repository.get_by_id.return_value = None

        delete_report_use_case = DeleteReport(mock_repository)
        request = DeleteReportRequest(id=non_existent_id)

        with pytest.raises(ReportNotFound) as exc_info:
            delete_report_use_case.execute(request)

        assert str(exc_info.value) == f"Report with {non_existent_id} not found"
        mock_repository.get_by_id.assert_called_once_with(non_existent_id)
        mock_repository.delete.assert_not_called()

    def test_delete_report_repository_error(self, mock_report):
        mock_repository = Mock(spec=ReportRepository)
        mock_repository.get_by_id.return_value = mock_report
        mock_repository.delete.side_effect = Exception("Repository error")

        delete_report_use_case = DeleteReport(mock_repository)
        request = DeleteReportRequest(id=mock_report.id)

        with pytest.raises(Exception, match="Repository error"):
            delete_report_use_case.execute(request)

        mock_repository.get_by_id.assert_called_once_with(mock_report.id)
        mock_repository.delete.assert_called_once_with(mock_report.id)
