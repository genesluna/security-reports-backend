from dataclasses import dataclass
from enum import StrEnum, unique
import re


@unique
class ReportStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"

    @classmethod
    def validate(cls, value) -> list[str]:
        errors: list[str] = []
        if value not in cls.__members__ and not isinstance(value, cls):
            errors.append("report_status must be a valid ReportStatus")
        return errors


@unique
class ReportType(StrEnum):
    DATA_LEAK = "DATA LEAK"
    INAPPROPRIATE_PRACTICES = "INAPPROPRIATE PRACTICES"
    SUSPICIOUS_ACTIVITIES = "SUSPICIOUS ACTIVITIES"
    OTHER = "OTHER"

    @classmethod
    def validate(cls, value) -> list[str]:
        errors: list[str] = []
        if value not in cls.__members__ and not isinstance(value, cls):
            errors.append("report_type must be a valid ReportType")
        return errors


@dataclass(frozen=True)
class Email:
    address: str = ""

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.address:
            return errors

        if len(self.address) > 255:
            errors.append("email cannot be longer than 255")

        # RFC 5322 Official Standard regex
        rfc_regex = re.compile(
            r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""",
            re.IGNORECASE,
        )
        if not bool(rfc_regex.match(self.address)):
            errors.append("email is not valid")

        return errors

    def __str__(self) -> str:
        return self.address
