from professors.utils.base_view import BaseView
from students.utils.response_messages import ResponseMessages
from rest_framework.permissions import IsAuthenticated,AllowAny


class StudentBaseView(BaseView):
    permission_classes = [AllowAny]
    _success_messages_dict = ResponseMessages._success_messages
    _error_messages_dict = ResponseMessages._error_messages
