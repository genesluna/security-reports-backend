from src.report.application.use_cases.create_report import (
    CreateReport,
    CreateReportRequest,
)
from src.report.domain.value_objects import ReportStatus, ReportType
from src.report.infrastructure.in_memory_report_repository import (
    InMemoryReportRepository,
)


class TestCreateReport:
    def test_create_report_saves_to_repository(self):
        repository = InMemoryReportRepository()
        create_report_use_case = CreateReport(repository)

        request = CreateReportRequest(
            title="Integration Test Report",
            complaint="This is a test complaint for integration testing",
            report_type=ReportType.DATA_LEAK,
            name="Integration Tester",
            email="integrator@test.com",
        )

        response = create_report_use_case.execute(request)

        assert len(repository.reports) == 1
        saved_report = repository.reports[0]

        assert saved_report.id == response.id
        assert saved_report.title == request.title
        assert saved_report.complaint == request.complaint
        assert saved_report.report_type == request.report_type
        assert saved_report.name == request.name
        assert str(saved_report.email) == request.email
        assert saved_report.report_status == ReportStatus.PENDING

    def test_multiple_report_creation(self):
        repository = InMemoryReportRepository()
        create_report_use_case = CreateReport(repository)

        # Create multiple reports
        reports_data = [
            CreateReportRequest(
                title=f"Report {i}",
                complaint=f"Complaint {i}",
                report_type=ReportType.DATA_LEAK,
            )
            for i in range(3)
        ]

        responses = [create_report_use_case.execute(request) for request in reports_data]

        assert len(repository.reports) == 3
        assert len(set(response.id for response in responses)) == 3  # Unique IDs

    def test_retrieve_created_report_by_id(self):
        repository = InMemoryReportRepository()
        create_report_use_case = CreateReport(repository)

        request = CreateReportRequest(
            title="Retrievable Report",
            complaint="This report should be retrievable",
            report_type=ReportType.DATA_LEAK,
        )

        response = create_report_use_case.execute(request)
        retrieved_report = repository.get_by_id(response.id)

        assert retrieved_report is not None
        assert retrieved_report.id == response.id
        assert retrieved_report.title == request.title
