import re
from dataclasses import dataclass

from src.report.domain.value_objects import ReportStatus, ReportType
from src.shared.domain.entity import Entity


@dataclass(eq=False)
class Report(Entity):
    title: str
    complaint: str
    report_type: ReportType
    name: str = ""
    email: str = ""
    report_status: ReportStatus = ReportStatus.PENDING

    def __post_init__(self):
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

        # RFC 5322 Official Standard regex
        rfc_regex = re.compile(
            r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""",
            re.IGNORECASE,
        )
        if self.email and not bool(rfc_regex.match(self.email)):
            self.notification.add_error("email is not valid")

        if len(self.email) > 255:
            self.notification.add_error("email cannot be longer than 255")

        if self.report_type not in ReportType.__members__ and not isinstance(
            self.report_type, ReportType
        ):
            self.notification.add_error("report_type must be a valid ReportType")

        if self.report_status not in ReportStatus.__members__ and not isinstance(
            self.report_status, ReportStatus
        ):
            self.notification.add_error("report_status must be a valid ReportStatus")

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
        self.email = email

        self.validate()

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"<Report {self.title} ({self.id})>"
