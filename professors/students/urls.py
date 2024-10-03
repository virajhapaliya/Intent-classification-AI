from django.urls import path,include
from students import views
urlpatterns = [
    # path("", include(router.urls)),
    path("add-student/", views.AddStudentView.as_view(), name="add-student"),
    path("update-score/", views.UpdateScoreView.as_view(), name="update-score"),
    path("get-subject-info-stundet/", views.SubjectInfoStudentView.as_view(), name="add-timestamp"),
    path("calculate-score/", views.CalculateScoreSubjectsView.as_view(), name="add-timestamp"),
    # path("add-student/", views.UpdateTimeStampView.as_view(), name="add-timestamp"),
    # path("add-student/", views.UpdateTimeStampView.as_view(), name="add-timestamp"),
    
]
