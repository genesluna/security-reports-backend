from uuid import uuid4

import pytest

from src.report.application.use_cases.exceptions import ReportNotFound
from src.report.application.use_cases.get_report import GetReport, GetReportRequest
from src.report.domain.report import Report
from src.report.domain.value_objects import ReportStatus, ReportType


class TestGetReportIntegration:
    @pytest.fixture
    def report_repository(self):
        from src.report.infrastructure.in_memory_report_repository import (
            InMemoryReportRepository,
        )

        return InMemoryReportRepository()

    @pytest.fixture
    def sample_report(self):
        return Report(
            id=uuid4(),
            name="John Doe",
            email="john.doe@example.com",
            title="Sample Integration Report",
            complaint="This is a test integration complaint",
            report_type=ReportType.DATA_LEAK,
            report_status=ReportStatus.PENDING,
        )

    def test_successful_report_retrieval(self, report_repository, sample_report):
        report_repository.save(sample_report)
        get_report_use_case = GetReport(report_repository)
        request = GetReportRequest(id=sample_report.id)

        response = get_report_use_case.execute(request)

        assert response.id == sample_report.id
        assert response.name == sample_report.name
        assert response.email == sample_report.email
        assert response.title == sample_report.title
        assert response.complaint == sample_report.complaint
        assert response.report_type == sample_report.report_type
        assert response.report_status == sample_report.report_status

    def test_report_not_found(self, report_repository):
        non_existent_id = uuid4()
        get_report_use_case = GetReport(report_repository)
        request = GetReportRequest(id=non_existent_id)

        with pytest.raises(ReportNotFound):
            get_report_use_case.execute(request)

    class TestReportVariations:
        @pytest.mark.parametrize("report_type", list(ReportType))
        def test_different_report_types(self, report_repository, report_type):
            report = Report(
                id=uuid4(),
                name="Type Test User",
                email="type@example.com",
                title=f"{report_type} Report",
                complaint="Testing report types",
                report_type=report_type,
                report_status=ReportStatus.PENDING,
            )
            report_repository.save(report)
            get_report_use_case = GetReport(report_repository)
            request = GetReportRequest(id=report.id)

            response = get_report_use_case.execute(request)
            assert response.report_type == report_type

        @pytest.mark.parametrize("report_status", list(ReportStatus))
        def test_different_report_statuses(self, report_repository, report_status):
            report = Report(
                id=uuid4(),
                name="Status Test User",
                email="status@example.com",
                title=f"{report_status} Report",
                complaint="Testing report statuses",
                report_type=ReportType.DATA_LEAK,
                report_status=report_status,
            )
            report_repository.save(report)
            get_report_use_case = GetReport(report_repository)
            request = GetReportRequest(id=report.id)

            response = get_report_use_case.execute(request)
            assert response.report_status == report_status
