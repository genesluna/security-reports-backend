import os
import uuid

import django

from src.report.domain.value_objects import ReportStatus
from src.report.serializers import (
    CreateReportRequestSerializer,
    CreateReportResponseSerializer,
    DeleteReportRequestSerializer,
    ListOutputMetaSerializer,
    ListReportResponseSerializer,
    ReportResponseSerializer,
    RetrieveReportRequestSerializer,
    RetrieveReportResponseSerializer,
    UpdateReportRequestSerializer,
)

# Set up Django settings for testing
os.environ["DJANGO_SETTINGS_MODULE"] = "src.settings"
django.setup()


class TestReportResponseSerializer:
    def test_valid_serializer(self):
        data = {
            "id": uuid.uuid4(),
            "title": "Test Report",
            "report_type": "Complaint",
            "report_status": "Pending",
            "name": "John Doe",
            "email": "john@example.com",
            "complaint": "Sample complaint text",
        }
        serializer = ReportResponseSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_invalid_email(self):
        data = {
            "id": uuid.uuid4(),
            "title": "Test Report",
            "report_type": "Complaint",
            "report_status": "Pending",
            "name": "John Doe",
            "email": "invalid-email",
            "complaint": "Sample complaint text",
        }
        serializer = ReportResponseSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors


class TestListOutputMetaSerializer:
    def test_valid_serializer(self):
        data = {"current_page": 1, "per_page": 10, "total": 50}
        serializer = ListOutputMetaSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_invalid_negative_values(self):
        data = {"current_page": -1, "per_page": -10, "total": -50}
        serializer = ListOutputMetaSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data


class TestListReportResponseSerializer:
    def test_valid_serializer(self):
        report_data = {
            "id": str(uuid.uuid4()),
            "title": "Test Report",
            "report_type": "Complaint",
            "report_status": "Pending",
            "name": "John Doe",
            "email": "john@example.com",
            "complaint": "Sample complaint text",
        }
        data = {
            "data": [report_data],
            "meta": {"current_page": 1, "per_page": 10, "total": 50},
        }
        serializer = ListReportResponseSerializer(data=data)
        assert serializer.is_valid()


class TestRetrieveReportRequestSerializer:
    def test_valid_serializer(self):
        report_id = uuid.uuid4()
        data = {"id": report_id}
        serializer = RetrieveReportRequestSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["id"] == report_id

    def test_invalid_id_format(self):
        data = {"id": "not-a-uuid"}
        serializer = RetrieveReportRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "id" in serializer.errors


class TestRetrieveReportResponseSerializer:
    def test_valid_serializer(self):
        report_data = {
            "id": str(uuid.uuid4()),
            "title": "Test Report",
            "report_type": "Complaint",
            "report_status": "Pending",
            "name": "John Doe",
            "email": "john@example.com",
            "complaint": "Sample complaint text",
        }
        serializer = RetrieveReportResponseSerializer(data={"data": report_data})
        assert serializer.is_valid()


class TestCreateReportRequestSerializer:
    def test_valid_serializer_with_all_fields(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "title": "Test Report",
            "report_type": "Complaint",
            "report_status": ReportStatus.PENDING,
            "complaint": "Sample complaint text",
        }
        serializer = CreateReportRequestSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_valid_serializer_with_optional_fields(self):
        data = {
            "title": "Test Report",
            "report_type": "Complaint",
            "complaint": "Sample complaint text",
        }
        serializer = CreateReportRequestSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data.get("name") is None
        assert serializer.validated_data.get("email") is None
        assert serializer.validated_data["report_status"] == ReportStatus.PENDING

    def test_invalid_serializer_missing_required_fields(self):
        data = {"name": "John Doe", "email": "john@example.com"}
        serializer = CreateReportRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "title" in serializer.errors
        assert "report_type" in serializer.errors
        assert "complaint" in serializer.errors


class TestCreateReportResponseSerializer:
    def test_valid_serializer(self):
        report_id = uuid.uuid4()
        data = {"id": report_id}
        serializer = CreateReportResponseSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["id"] == report_id


class TestUpdateReportRequestSerializer:
    def test_valid_serializer(self):
        data = {
            "id": uuid.uuid4(),
            "name": "John Doe",
            "email": "john@example.com",
            "title": "Updated Report",
            "report_type": "Complaint",
            "report_status": "In Progress",
            "complaint": "Updated complaint text",
        }
        serializer = UpdateReportRequestSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_invalid_serializer_missing_required_fields(self):
        data = {"id": uuid.uuid4(), "name": "John Doe"}
        serializer = UpdateReportRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "title" in serializer.errors
        assert "report_type" in serializer.errors
        assert "report_status" in serializer.errors
        assert "complaint" in serializer.errors


class TestDeleteReportRequestSerializer:
    def test_valid_serializer(self):
        report_id = uuid.uuid4()
        data = {"id": report_id}
        serializer = DeleteReportRequestSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["id"] == report_id

    def test_invalid_id_format(self):
        data = {"id": "not-a-uuid"}
        serializer = DeleteReportRequestSerializer(data=data)
        assert not serializer.is_valid()
        assert "id" in serializer.errors
