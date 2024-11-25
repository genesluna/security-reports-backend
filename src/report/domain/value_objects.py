from enum import StrEnum, unique


@unique
class ReportStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"


@unique
class ReportType(StrEnum):
    DATA_LEAK = "DATA LEAK"
    INAPPROPRIATE_PRACTICES = "INAPPROPRIATE PRACTICES"
    SUSPICIOUS_ACTIVITIES = "SUSPICIOUS ACTIVITIES"
    OTHER = "OTHER"
