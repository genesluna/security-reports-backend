import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from src.report.domain.value_objects import ReportStatus, ReportType


@pytest.mark.django_db
class TestReportE2E:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_complete_report_lifecycle(self, api_client):
        # 1. Create a new report
        create_url = reverse("report-list")
        create_data = {
            "title": "Security Breach Report",
            "complaint": "Detected unauthorized access attempts",
            "report_type": ReportType.DATA_LEAK.name,
            "name": "John Smith",
            "email": "john@example.com",
        }

        create_response = api_client.post(create_url, create_data, format="json")
        assert create_response.status_code == status.HTTP_201_CREATED
        report_id = create_response.json()["id"]

        # 2. Verify report creation
        detail_url = reverse("report-detail", args=[report_id])
        get_response = api_client.get(detail_url)
        assert get_response.status_code == status.HTTP_200_OK
        report_data = get_response.json()["data"]
        assert report_data["title"] == create_data["title"]
        assert report_data["report_status"] == ReportStatus.PENDING.name

        # 3. Update report status
        update_data = {"report_status": ReportStatus.PROCESSING.name}
        update_response = api_client.patch(detail_url, update_data, format="json")
        assert update_response.status_code == status.HTTP_204_NO_CONTENT

        # 4. Verify update
        get_response = api_client.get(detail_url)
        assert (
            get_response.json()["data"]["report_status"] == ReportStatus.PROCESSING.name
        )

        # 5. List and search
        list_url = reverse("report-list")
        search_response = api_client.get(f"{list_url}?search_query=Security")
        assert search_response.status_code == status.HTTP_200_OK
        assert len(search_response.json()["data"]) > 0

        # 6. Delete report
        delete_response = api_client.delete(detail_url)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # 7. Verify deletion
        get_response = api_client.get(detail_url)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_report_error_scenarios(self, api_client):
        # Test invalid data
        create_url = reverse("report-list")
        invalid_data = {"title": "", "report_type": "INVALID_TYPE"}  # Empty title
        response = api_client.post(create_url, invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Test non-existent report
        detail_url = reverse(
            "report-detail", args=[str("00000000-0000-0000-0000-000000000000")]
        )
        response = api_client.get(detail_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_report_status_transitions(self, api_client):
        # Create report
        create_url = reverse("report-list")
        create_data = {
            "title": "Test Status Transitions",
            "complaint": "Testing status workflow",
            "report_type": ReportType.OTHER.name,
        }

        response = api_client.post(create_url, create_data, format="json")
        report_id = response.json()["id"]
        detail_url = reverse("report-detail", args=[report_id])

        # Test status transitions
        status_sequence = [ReportStatus.PROCESSING.name, ReportStatus.COMPLETED.name]

        for new_status in status_sequence:
            update_data = {"report_status": new_status}
            response = api_client.patch(detail_url, update_data, format="json")
            assert response.status_code == status.HTTP_204_NO_CONTENT
            get_response = api_client.get(detail_url)
            assert get_response.json()["data"]["report_status"] == new_status
