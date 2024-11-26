from typing import Optional
from uuid import UUID

from django.db.models import Q

from src.report.domain.report import Report
from src.report.domain.report_repository import ReportRepository
from src.report.models import ReportModel


class DjangoORMReportRepository(ReportRepository):
    def __init__(self, model: ReportModel | None = None):
        self.model = model or ReportModel

    def save(self, report: Report) -> None:
        report_model = ReportModelMapper.to_model(report)
        report_model.save()

    def get_by_id(self, id: UUID) -> Report | None:
        try:
            report_model = self.model.objects.get(id=id)
            return ReportModelMapper.to_entity(report_model)

        except self.model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def list(
        self,
        order_by: Optional[str] = None,
        current_page: Optional[int] = None,
        per_page: Optional[int] = None,
        search_query: Optional[str] = None,
    ) -> list[Report]:

        queryset = self.model.objects.all()

        # Search
        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query)
                | Q(title__icontains=search_query)
                | Q(complaint__icontains=search_query)
                | Q(report_type__icontains=search_query)
                | Q(report_status__icontains=search_query)
            )

        # Ordering
        if order_by:
            if order_by.startswith("-"):
                order_by = order_by[1:]
                queryset = queryset.order_by(f"-{order_by}")
            else:
                queryset = queryset.order_by(order_by)

        # Pagination
        if current_page is not None and per_page is not None:
            start = (current_page - 1) * per_page
            end = start + per_page
            queryset = queryset[start:end]

        return [ReportModelMapper.to_entity(report) for report in list(queryset)]

    def update(self, report: Report) -> None:
        self.model.objects.filter(pk=report.id).update(
            id=report.id,
            title=report.title,
            complaint=report.complaint,
            name=report.name,
            email=report.email,
            report_type=report.report_type,
            report_status=report.report_status,
        )


class ReportModelMapper:
    @staticmethod
    def to_entity(model: ReportModel) -> Report:
        return Report(
            id=model.id,
            title=model.title,
            complaint=model.complaint,
            name=model.name,
            email=model.email,
            report_type=model.report_type,
            report_status=model.report_status,
        )

    @staticmethod
    def to_model(entity: Report) -> ReportModel:
        return ReportModel(
            id=entity.id,
            title=entity.title,
            complaint=entity.complaint,
            name=entity.name,
            email=entity.email,
            report_type=entity.report_type,
            report_status=entity.report_status,
        )
