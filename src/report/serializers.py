from rest_framework import serializers

from src.report.domain.value_objects import ReportStatus


class ReportResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    report_type = serializers.CharField(max_length=50)
    report_status = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    complaint = serializers.CharField(max_length=1024)


class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class ListReportResponseSerializer(serializers.Serializer):
    data = ReportResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()


class RetrieveReportRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveReportResponseSerializer(serializers.Serializer):
    data = ReportResponseSerializer(source="*")


class CreateReportRequestSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=False
    )
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=False)
    title = serializers.CharField(
        max_length=255, required=True, allow_blank=False, allow_null=False
    )
    report_type = serializers.CharField(
        max_length=50, required=True, allow_blank=False, allow_null=False
    )
    report_status = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        allow_null=False,
        default=ReportStatus.PENDING,
    )
    complaint = serializers.CharField(
        max_length=1024, required=True, allow_blank=False, allow_null=False
    )


class CreateReportResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateReportRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(
        max_length=100, required=False, allow_blank=True, allow_null=False
    )
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=False)
    title = serializers.CharField(
        max_length=255, required=True, allow_blank=False, allow_null=False
    )
    report_type = serializers.CharField(
        max_length=50, required=True, allow_blank=False, allow_null=False
    )
    report_status = serializers.CharField(
        max_length=50, required=True, allow_blank=False, allow_null=False
    )
    complaint = serializers.CharField(
        max_length=1024, required=True, allow_blank=False, allow_null=False
    )


class DeleteReportRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
