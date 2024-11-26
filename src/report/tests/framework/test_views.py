import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.report.domain.value_objects import ReportStatus, ReportType
from src.report.models import ReportModel


@pytest.mark.django_db
class TestReportViews:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def report_data(self):
        return {
            "title": "Test Report",
            "complaint": "This is a test complaint.",
            "report_type": ReportType.OTHER,
            "name": "Test User",
            "email": "test@example.com",
            "report_status": ReportStatus.PENDING,
        }

    @pytest.fixture
    def create_report(self, report_data):
        def make_report(**kwargs):
            data = {**report_data, **kwargs}
            return ReportModel.objects.create(**data)

        return make_report

    def test_list_reports(self, api_client, create_report):
        create_report()
        url = reverse("report-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "data" in response.json()

    def test_retrieve_report(self, api_client, create_report):
        report = create_report()
        url = reverse("report-detail", args=[report.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["id"] == str(report.id)

    def test_create_report(self, api_client):
        url = reverse("report-list")
        data = {
            "title": "New Report",
            "complaint": "This is a new complaint.",
            "report_type": ReportType.DATA_LEAK.name,
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.json()

    def test_update_report(self, api_client, create_report):
        report = create_report()
        url = reverse("report-detail", args=[report.id])
        data = {
            "title": "Updated Report",
            "complaint": "Updated complaint.",
            "report_type": ReportType.INAPPROPRIATE_PRACTICES.name,
            "report_status": ReportStatus.PROCESSING.name,
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_partial_update_report(self, api_client, create_report):
        report = create_report()
        url = reverse("report-detail", args=[report.id])
        data = {
            "report_status": ReportStatus.COMPLETED.name,
        }
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_report(self, api_client, create_report):
        report = create_report()
        url = reverse("report-detail", args=[report.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ReportModel.objects.filter(id=report.id).exists()
