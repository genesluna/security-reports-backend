import uuid

from django.db import models

from src.report.domain.value_objects import ReportStatus, ReportType


class ReportModel(models.Model):
    STATUS_CHOICES = [(status.name, status.value) for status in ReportStatus]
    COMPLAINT_TYPE_CHOICES = [
        (complaint_type.name, complaint_type.value) for complaint_type in ReportType
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=COMPLAINT_TYPE_CHOICES)
    complaint = models.TextField()
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    report_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=ReportStatus.PENDING
    )

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"
        db_table = "report"

    def __str__(self):
        return f"{self.title} - {self.status}"
