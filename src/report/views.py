from uuid import UUID

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from src import config
from src.report.application.use_cases.create_report import (
    CreateReport,
    CreateReportRequest,
)
from src.report.application.use_cases.delete_report import (
    DeleteReport,
    DeleteReportRequest,
)
from src.report.application.use_cases.exceptions import ReportNotFound
from src.report.application.use_cases.get_report import GetReport, GetReportRequest
from src.report.application.use_cases.list_report import (
    ListReport,
    ListReportRequest,
    ListReportResponse,
)
from src.report.application.use_cases.update_report import (
    UpdateReport,
    UpdateReportRequest,
)
from src.report.repository import DjangoORMReportRepository
from src.report.serializers import (
    CreateReportRequestSerializer,
    CreateReportResponseSerializer,
    DeleteReportRequestSerializer,
    ListReportResponseSerializer,
    RetrieveReportRequestSerializer,
    RetrieveReportResponseSerializer,
    UpdateReportRequestSerializer,
)


class ReportViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "order_by",
                openapi.IN_QUERY,
                description="Field to order by. Prefix with '-' for descending order (e.g. '-title')",
                type=openapi.TYPE_STRING,
                required=False,
                example="title",
            ),
            openapi.Parameter(
                "current_page",
                openapi.IN_QUERY,
                description="Current page number",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1,
            ),
            openapi.Parameter(
                "per_page",
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10,
            ),
            openapi.Parameter(
                "search_query",
                openapi.IN_QUERY,
                description="Search in title, complaint, email, report_type and status",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            200: ListReportResponseSerializer,
        },
        operation_description="List and filter reports with pagination support",
    )
    def list(self, request: Request) -> Response:
        use_case = ListReport(repository=DjangoORMReportRepository())
        output: ListReportResponse = use_case.execute(
            request=ListReportRequest(
                order_by=request.query_params.get("order_by", "title"),
                current_page=int(request.query_params.get("current_page", 1)),
                per_page=int(
                    request.query_params.get(
                        "per_page",
                        config.DEFAULT_PAGINATION_SIZE,
                    )
                ),
                search_query=request.query_params.get("search_query", None),
            )
        )
        response_serializer = ListReportResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    @swagger_auto_schema(
        responses={200: RetrieveReportResponseSerializer, 404: "Report not found"},
        operation_description="Get a specific report",
    )
    def retrieve(self, request: Request, pk: UUID = None) -> Response:
        serializer = RetrieveReportRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        input = GetReportRequest(**serializer.validated_data)
        use_case = GetReport(repository=DjangoORMReportRepository())

        try:
            output = use_case.execute(request=input)
        except ReportNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        response_serializer = RetrieveReportResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data,
        )

    @swagger_auto_schema(
        request_body=CreateReportRequestSerializer,
        responses={201: CreateReportResponseSerializer},
        operation_description="Create a new report",
    )
    def create(self, request: Request) -> Response:
        serializer = CreateReportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateReportRequest(**serializer.validated_data)
        use_case = CreateReport(repository=DjangoORMReportRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateReportResponseSerializer(output).data,
        )

    @swagger_auto_schema(
        request_body=UpdateReportRequestSerializer,
        responses={204: "No content", 404: "Report not found"},
        operation_description="Update a report",
    )
    def update(self, request: Request, pk: UUID = None):
        serializer = UpdateReportRequestSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateReportRequest(**serializer.validated_data)
        use_case = UpdateReport(repository=DjangoORMReportRepository())
        try:
            use_case.execute(request=input)
        except ReportNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=UpdateReportRequestSerializer,
        responses={204: "No content", 404: "Report not found"},
        operation_description="Partially update a report",
    )
    def partial_update(self, request, pk: UUID = None):
        serializer = UpdateReportRequestSerializer(
            data={
                **request.data,
                "id": pk,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        input = UpdateReportRequest(**serializer.validated_data)
        use_case = UpdateReport(repository=DjangoORMReportRepository())
        try:
            use_case.execute(request=input)
        except ReportNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={204: "No content", 404: "Report not found"},
        operation_description="Delete a report",
    )
    def destroy(self, request: Request, pk: UUID = None):
        request_data = DeleteReportRequestSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteReportRequest(**request_data.validated_data)
        use_case = DeleteReport(repository=DjangoORMReportRepository())
        try:
            use_case.execute(input)
        except ReportNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
