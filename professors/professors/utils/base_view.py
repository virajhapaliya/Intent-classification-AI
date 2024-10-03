from rest_framework import status
from rest_framework.response import Response
from typing import Any, List
from professors.utils.base_serializer import get_error_message
from rest_framework.views import APIView
from django.http import HttpResponse


class ProjectBaseView:
    _success_messages_dict: dict
    _error_messages_dict: dict

    success_return_code: str
    error_return_code: str

    _base_success_code: int = status.HTTP_200_OK
    _base_error_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY

    def set_success_code(self, code: int) -> None:
        self._base_success_code = code

    def set_error_code(self, code: int) -> None:
        self._base_error_code = code
    
    def _api_response(
        self,
        message: str,
        status_code: int,
        result: List[Any],
        response: bool = False,
        return_code: str=None,

    ):
        return_response = {
                    # "return_code": return_code,
                    "message": message,
                    "response": response,
                    "result": result,
                }
        # print("return_response",return_response)
        return Response(
               return_response,
                status=status_code,
            )


    def get_success_response(self, result: List[Any] = []) -> Response:

        return self._api_response(
            # return_code=self.success_return_code,
            message=self._success_messages_dict[self.success_return_code],
            status_code=self._base_success_code,
            response=True,
            result=result,
        )

    def get_error_response(self, result: List[Any] = []) -> Response:
        return self._api_response(
            # return_code=self.error_return_code,
            message=self._error_messages_dict[self.error_return_code],
            status_code=self._base_error_code,
            response=False,
            result=result,
        )

    def get_serializer_error_response(self, serializer_errors: dict):
        field_error, field_error_message = get_error_message(
            serializer_errors=serializer_errors,
            error_messages_dict=self._error_messages_dict,
        )
        print("here")

        return self._api_response(
            return_code=field_error,
            message=field_error_message,
            status_code=self._base_error_code,
            response=False,
            result=[],
        )


class BaseView(APIView, ProjectBaseView):
    pass

    def post(self, request):
        pass
