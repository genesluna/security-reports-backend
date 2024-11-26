from dataclasses import dataclass

from src.report.domain.value_objects import ReportStatus, ReportType, Email
from src.shared.domain.entity import Entity


@dataclass(eq=False)
class Report(Entity):
    title: str
    complaint: str
    report_type: ReportType
    name: str = ""
    email: str | Email = ""
    report_status: ReportStatus = ReportStatus.PENDING

    def __post_init__(self):
        if isinstance(self.email, str):
            self.email = Email(self.email)
        self.validate()

    def validate(self):
        if len(self.name) > 100:
            self.notification.add_error("name cannot be longer than 100")

        if len(self.title) > 255:
            self.notification.add_error("title cannot be longer than 255")

        if not self.title:
            self.notification.add_error("title cannot be empty")

        if not self.complaint:
            self.notification.add_error("complaint cannot be empty")

        if len(self.complaint) > 1024:
            self.notification.add_error("complaint cannot be longer than 1024")

        if not self.report_type:
            self.notification.add_error("report_type cannot be empty")

        if isinstance(self.email, Email):
            email_errors = self.email.validate()
            if email_errors:
                self.notification.add_errors(email_errors)

        type_errors = ReportType.validate(self.report_type)
        if type_errors:
            self.notification.add_errors(type_errors)

        status_errors = ReportStatus.validate(self.report_status)
        if status_errors:
            self.notification.add_errors(status_errors)

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update_report(
        self,
        title,
        complaint,
        report_type,
        report_status=ReportStatus.PENDING,
        name="",
        email="",
    ):
        self.title = title
        self.complaint = complaint
        self.report_type = report_type
        self.report_status = report_status
        self.name = name
        self.email = Email(email) if isinstance(email, str) else email

        self.validate()

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"<Report {self.title} ({self.id})>"
