import uuid

import pytest

from src.report.domain.report import Report
from src.report.domain.value_objects import ReportStatus, ReportType


class TestReportEntity:
    def test_valid_report_creation(self):
        report_type = ReportType.DATA_LEAK
        report = Report(
            id="test-id",
            title="Valid Report",
            complaint="This is a valid complaint",
            name="John Doe",
            email="john.doe@example.com",
            report_type=report_type,
        )

        assert report.title == "Valid Report"
        assert report.complaint == "This is a valid complaint"
        assert report.name == "John Doe"
        assert str(report.email) == "john.doe@example.com"
        assert report.report_type == report_type
        assert report.report_status == ReportStatus.PENDING

    def test_report_must_be_created_with_id_as_uuid_by_default(self):
        report_type = ReportType.DATA_LEAK
        report = Report(
            title="Original Title",
            complaint="Original Complaint",
            report_type=report_type,
        )
        assert isinstance(report.id, uuid.UUID)

    def test_empty_title_raises_error(self):
        report_type = ReportType.DATA_LEAK
        with pytest.raises(ValueError) as excinfo:
            Report(
                id="test-id",
                title="",
                complaint="Valid complaint",
                report_type=report_type,
            )
        assert "title cannot be empty" in str(excinfo.value)

    def test_empty_complaint_raises_error(self):
        report_type = ReportType.DATA_LEAK
        with pytest.raises(ValueError) as excinfo:
            Report(id="test-id", title="Valid Title", complaint="", report_type=report_type)
        assert "complaint cannot be empty" in str(excinfo.value)

    def test_title_too_long_raises_error(self):
        report_type = ReportType.DATA_LEAK
        long_title = "a" * 256
        with pytest.raises(ValueError) as excinfo:
            Report(
                id="test-id",
                title=long_title,
                complaint="Valid complaint",
                report_type=report_type,
            )
        assert "title cannot be longer than 255" in str(excinfo.value)

    def test_complaint_too_long_raises_error(self):
        report_type = ReportType.DATA_LEAK
        long_complaint = "a" * 1025
        with pytest.raises(ValueError) as excinfo:
            Report(
                id="test-id",
                title="Valid Title",
                complaint=long_complaint,
                report_type=report_type,
            )
        assert "complaint cannot be longer than 1024" in str(excinfo.value)

    def test_name_too_long_raises_error(self):
        report_type = ReportType.DATA_LEAK
        long_name = "a" * 101
        with pytest.raises(ValueError) as excinfo:
            Report(
                id="test-id",
                title="Valid Title",
                complaint="Valid complaint",
                name=long_name,
                report_type=report_type,
            )
        assert "name cannot be longer than 100" in str(excinfo.value)

    def test_invalid_email_raises_error(self):
        report_type = ReportType.DATA_LEAK
        invalid_emails = [
            "invalid-email",
            "invalid@email",
            "invalid@email.",
            "@invalid.com",
            "invalid@.com",
        ]

        for invalid_email in invalid_emails:
            with pytest.raises(ValueError) as excinfo:
                Report(
                    id="test-id",
                    title="Valid Title",
                    complaint="Valid complaint",
                    email=invalid_email,
                    report_type=report_type,
                )
            assert "email is not valid" in str(excinfo.value)

    def test_email_too_long_raises_error(self):
        report_type = ReportType.DATA_LEAK
        long_email = "a" * 255 + "@example.com"
        with pytest.raises(ValueError) as excinfo:
            Report(
                id="test-id",
                title="Valid Title",
                complaint="Valid complaint",
                email=long_email,
                report_type=report_type,
            )
        assert "email cannot be longer than 255" in str(excinfo.value)


class TestUpdateReport:
    def test_update_report_method(self):
        report_type = ReportType.DATA_LEAK
        report = Report(
            id="test-id",
            title="Original Title",
            complaint="Original Complaint",
            report_type=report_type,
        )

        report.update_report(
            title="Updated Title",
            complaint="Updated Complaint",
            report_type=report_type,
            report_status=ReportStatus.PROCESSING,
            name="Genes Luna",
            email="genesluna@gmail.com",
        )

        assert report.title == "Updated Title"
        assert report.complaint == "Updated Complaint"
        assert report.report_status == ReportStatus.PROCESSING
        assert report.name == "Genes Luna"
        assert str(report.email) == "genesluna@gmail.com"

    def test_update_report_method_validates(self):
        report_type = ReportType.DATA_LEAK
        report = Report(
            id="test-id",
            title="Original Title",
            complaint="Original Complaint",
            report_type=report_type,
        )

        with pytest.raises(ValueError):
            report.update_report(
                title="",
                complaint="Updated Complaint",
                report_type=report_type,  # Empty title should raise an error
            )

    def test_str_and_repr_methods(self):
        report_type = ReportType.DATA_LEAK
        report = Report(
            id="test-id",
            title="Test Report",
            complaint="Test Complaint",
            report_type=report_type,
        )

        assert str(report) == "Test Report"
        assert repr(report) == "<Report Test Report (test-id)>"


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        report_type = ReportType.DATA_LEAK
        common_id = uuid.uuid4()
        report_1 = Report(
            id=common_id,
            title="Test Report",
            complaint="Test Complaint",
            report_type=report_type,
        )
        report_2 = Report(
            id=common_id,
            title="Test Report2",
            complaint="Test Complaint2",
            report_type=report_type,
        )

        assert report_1 == report_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        report_type = ReportType.DATA_LEAK
        category = Report(title="Test Report", complaint="Test Complaint", report_type=report_type)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
