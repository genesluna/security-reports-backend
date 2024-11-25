import uuid
from unittest.mock import Mock

import pytest

from src.report.domain.report import Report
from src.report.models import ReportModel
from src.report.repository import DjangoORMReportRepository, ReportModelMapper


@pytest.fixture
def sample_report():
    return Report(
        id=uuid.uuid4(),
        title="Test Report",
        complaint="Sample complaint",
        name="John Doe",
        email="john@example.com",
        report_type="DATA_LEAK",
        report_status="PENDING",
    )


@pytest.fixture
def mock_report_model(sample_report):
    mock_model = Mock(spec=ReportModel)
    mock_model.id = sample_report.id
    mock_model.title = sample_report.title
    mock_model.complaint = sample_report.complaint
    mock_model.name = sample_report.name
    mock_model.email = sample_report.email
    mock_model.report_type = sample_report.report_type
    mock_model.report_status = sample_report.report_status
    return mock_model


class TestReportModelMapper:
    def test_to_entity(self, mock_report_model):
        report = ReportModelMapper.to_entity(mock_report_model)

        assert report.id == mock_report_model.id
        assert report.title == mock_report_model.title
        assert report.complaint == mock_report_model.complaint
        assert report.name == mock_report_model.name
        assert report.email == mock_report_model.email
        assert report.report_type == mock_report_model.report_type
        assert report.report_status == mock_report_model.report_status

    def test_to_model(self, sample_report):
        report_model = ReportModelMapper.to_model(sample_report)

        assert report_model.id == sample_report.id
        assert report_model.title == sample_report.title
        assert report_model.complaint == sample_report.complaint
        assert report_model.name == sample_report.name
        assert report_model.email == sample_report.email
        assert report_model.report_type == sample_report.report_type
        assert report_model.report_status == sample_report.report_status


class TestDjangoORMReportRepository:
    @pytest.mark.django_db
    def test_save(self, db, sample_report):
        repository = DjangoORMReportRepository()
        repository.save(sample_report)

        saved_report = ReportModel.objects.get(id=sample_report.id)
        assert saved_report is not None
        assert saved_report.title == sample_report.title

    @pytest.mark.django_db
    def test_get_by_id(self, db, sample_report):
        repository = DjangoORMReportRepository()
        repository.save(sample_report)

        retrieved_report = repository.get_by_id(sample_report.id)
        assert retrieved_report is not None
        assert retrieved_report.id == sample_report.id

    @pytest.mark.django_db
    def test_get_by_id_not_found(self, db):
        repository = DjangoORMReportRepository()
        non_existent_id = uuid.uuid4()

        retrieved_report = repository.get_by_id(non_existent_id)
        assert retrieved_report is None

    @pytest.mark.django_db
    def test_delete(self, db, sample_report):
        repository = DjangoORMReportRepository()
        repository.save(sample_report)

        repository.delete(sample_report.id)
        with pytest.raises(ReportModel.DoesNotExist):
            ReportModel.objects.get(id=sample_report.id)

    @pytest.mark.django_db
    def test_list_no_filters(self, db, sample_report):
        repository = DjangoORMReportRepository()
        repository.save(sample_report)

        reports = repository.list()
        assert len(reports) > 0
        assert any(report.id == sample_report.id for report in reports)

    @pytest.mark.django_db
    def test_list_with_search_query(self, db, sample_report):
        repository = DjangoORMReportRepository()
        repository.save(sample_report)

        reports = repository.list(search_query="John")
        assert len(reports) > 0
        assert any(report.id == sample_report.id for report in reports)

    @pytest.mark.django_db
    def test_list_with_ordering(self, db, sample_report):
        repository = DjangoORMReportRepository()
        repository.save(sample_report)

        reports = repository.list(order_by="title")
        assert len(reports) > 0

        reports_desc = repository.list(order_by="-title")
        assert len(reports_desc) > 0

    @pytest.mark.django_db
    def test_list_with_pagination(self, db, sample_report):
        repository = DjangoORMReportRepository()
        repository.save(sample_report)

        reports = repository.list(current_page=1, per_page=10)
        assert len(reports) > 0

    @pytest.mark.django_db
    def test_update(self, db, sample_report):
        repository = DjangoORMReportRepository()
        repository.save(sample_report)

        updated_report = Report(
            id=sample_report.id,
            title="Updated Report",
            complaint=sample_report.complaint,
            name=sample_report.name,
            email=sample_report.email,
            report_type=sample_report.report_type,
            report_status="COMPLETED",
        )

        repository.update(updated_report)

        retrieved_report = repository.get_by_id(sample_report.id)
        assert retrieved_report.title == "Updated Report"
        assert retrieved_report.report_status == "COMPLETED"
