from django.shortcuts import render
import traceback

from students import serializers as student_serializer
from students import models as student_models
from students.utils import response_messages as RESPONSE
from students.utils.base_view import StudentBaseView

from rest_framework.request import Request
# Create your views here.

class AddStudentView(StudentBaseView):
	success_return_code = RESPONSE.STUDENT_ADDED_SUCCESS
	error_return_code =RESPONSE.STUDENT_ADDITION_FAILED
	serializer_class = student_serializer.AddStudentSerializer
	permission_classes = []

	def post(self, request: Request):
		try:
			serializer = self.serializer_class(data=request.data)

			if serializer.is_valid():
				first_name = serializer.validated_data["first_name"]
				last_name = serializer.validated_data["last_name"]
				student_id = serializer.validated_data["student_id"]

				if student_models.Student.objects.filter(student_id=student_id).exists():
					return self.get_error_response(result={
						'code':'not_unique_student_id',
						'message':"Please use new student Id as this id is already been used.",
						'data':{}
					})
				student_queryset = student_models.Student.objects.create(
					first_name=first_name.lower(),
					last_name=last_name.lower(),
					student_id=student_id
				)
				return self.get_success_response(result={
					'code':'student_added_successfully',
					'data':{},
					'message':'Added new student successfully.'
				})
			else:
				return self.get_serializer_error_response(
						serializer_errors=serializer.errors
					)

				
		except Exception as e:
			traceback.print_exc()
			return self.get_error_response(result={
					'code':'student_not_added',
					'error':str(e)
				})
		

class UpdateScoreView(StudentBaseView):
	success_return_code = RESPONSE.STUDENT_ADDED_SUCCESS
	error_return_code =RESPONSE.STUDENT_ADDITION_FAILED
	serializer_class = student_serializer.AddScoreSerializer
	permission_classes = []

	def post(self, request):
		try:
			serializer = self.serializer_class(data=request.data)

			if serializer.is_valid():
				first_name = serializer.validated_data["first_name"]
				last_name = serializer.validated_data["last_name"]
				subject = serializer.validated_data['subject_name']
				score = serializer.validated_data['score']

				try:
					subject_queryset = student_models.Subject.objects.get(name=subject)
					print("subject_queryset",subject_queryset)
				except student_models.Subject.DoesNotExist as e:
					return self.get_error_response(result={
						'code':'subject_does_not_exists',
					})		
				student_queryset = student_models.Student.objects.filter(first_name=first_name.lower(),last_name=last_name.lower())
				print("student_queryset",student_queryset)
				if len(student_queryset)>=2:
					studentsubject_serializer = student_serializer.StudentSubjectSerializer(student_queryset, many=True)  
					return self.get_success_response(result={
						'data':studentsubject_serializer.data
					})	
				elif len(student_queryset) <= 0:
					return self.get_success_response(result={
						'data':{}
					})
				else:
					scores = student_models.Score.objects.create(student=student_queryset[0],subject=subject_queryset,score=score)
					return self.get_success_response(result={
						'code':'student_added_successfully',
						'data':{}
					})
			else:
				return self.get_serializer_error_response(
						serializer_errors=serializer.errors
					)
			print(serializer)
				
		except Exception as e:
			traceback.print_exc()
			return self.get_error_response(result={
					'code':'student_not_added',
					'error':str(e)
				})
		
class UpdateScoreView(StudentBaseView):
	success_return_code = RESPONSE.STUDENT_ADDED_SUCCESS
	error_return_code =RESPONSE.STUDENT_ADDITION_FAILED
	serializer_class = student_serializer.AddScoreSerializer
	permission_classes = []

	def post(self, request):
		try:
			serializer = self.serializer_class(data=request.data)

			if serializer.is_valid():
				first_name = serializer.validated_data["first_name"]
				last_name = serializer.validated_data["last_name"]
				subject = serializer.validated_data['subject_name']
				score = serializer.validated_data['score']
				print("score",score)
				try:
					subject_queryset = student_models.Subject.objects.get(name=subject)
					print("subject_queryset",subject_queryset)
				except student_models.Subject.DoesNotExist as e:
					return self.get_error_response(result={
						'code':'subject_does_not_exists',
						'message':'This subject does not exist, available subjects math,science,physics,history',
						'data':{}
					})		
				student_queryset = student_models.Student.objects.filter(first_name=first_name.lower(),last_name=last_name.lower())
				print("student_queryset",student_queryset)
				if len(student_queryset)>=2:
					studentsubject_serializer = student_serializer.StudentSubjectSerializer(student_queryset, many=True)  
					return self.get_error_response(result={
						'data':studentsubject_serializer.data,
						'code':'found_multiple_users',
						'message':'Found multiple users with same name.. Try again with specific information'
					})	
				elif len(student_queryset) <= 0:
					return self.get_error_response(result={
						'data':{},
						'code':'no_user_found',
						'message':'There is no user with for information'
					})
				else:
					scores = student_models.Score.objects.create(student=student_queryset[0],subject=subject_queryset,score=score)
					return self.get_success_response(result={
						'code':'student_added_successfully',
						'message':'Added Score successfully'
					})
			else:
				return self.get_serializer_error_response(
						serializer_errors=serializer.errors
					)
				
		except Exception as e:
			traceback.print_exc()
			return self.get_error_response(result={
					'code':'student_not_added',
					'error':str(e)
				})
		
class SubjectInfoStudentView(StudentBaseView):
	success_return_code = RESPONSE.STUDENT_ADDED_SUCCESS
	error_return_code =RESPONSE.STUDENT_ADDITION_FAILED
	serializer_class = student_serializer.StudentInfoSerializer
	permission_classes = []

	def post(self, request):
		try:
			serializer = self.serializer_class(data=request.data)

			if serializer.is_valid():
				first_name = serializer.validated_data["first_name"]
				last_name = serializer.validated_data["last_name"]
				student_id = serializer.validated_data['student_id']

				
				if student_id:
					student_queryset = student_models.Student.objects.get(student_id=student_id)
				elif first_name and last_name:
					student_queryset = student_models.Student.objects.filter(first_name=first_name.lower(),last_name=last_name.lower())
					print("student_queryset",student_queryset)
					if len(student_queryset)>=2:
						return self.error_return_code(result={
							'data':{},
							'code':'multiple_user_found',
							'message':'Please provided specific student id and multiple student found with same ID.'
						})	
					elif len(student_queryset) <= 0:
						return self.get_success_response(result={
							'data':{},
							'code':'no_user_found',
							'message':" There is not student with this name available, please specify student_id"
						})
					else:
						print(student_queryset)
						student_queryset = student_queryset[0]
				
				subjects = student_models.Score.objects.filter(student=student_queryset)
				print('subjects',subjects)
				subject_serializer = student_serializer.SubjectInfoSerializer(subjects,many=True)
				print('subject_serializer',subject_serializer.data)
				return self.get_success_response(result={
					'data':subject_serializer.data,
					'code':'subject_fetch_success',
					'message': "Subject Of students.."
				})
			else:
				return self.get_serializer_error_response(
				serializer_errors=serializer.errors
			)
						
				
		except Exception as e:
			traceback.print_exc()
			return self.get_error_response(result={
					'code':'student_not_added',
					'error':str(e)
				})
		
class CalculateScoreSubjectsView(StudentBaseView):
	success_return_code = RESPONSE.STUDENT_ADDED_SUCCESS
	error_return_code =RESPONSE.STUDENT_ADDITION_FAILED
	serializer_class = student_serializer.SubjectScoreSerializer
	permission_classes = []

	def post(self, request):
		try:
			serializer = self.serializer_class(data=request.data)

			if serializer.is_valid():
				subject_name = serializer.validated_data['subject_name']
				try:
					subject_queryset = student_models.Subject.objects.get(name=subject_name)
				except student_models.Subject.DoesNotExist as e:
					return self.get_error_response(result={
						'code':'not_subject_found',
						'message':"Please provide correct subject name"
					})			
				score_queryset = student_models.Score.objects.filter(subject=subject_queryset)
				score_serializer = student_serializer.ScoreSerializer(score_queryset,many=True)
				return self.get_success_response(result={
					'data':score_serializer.data,
					'code':'score_fetch_successfully',
					'message': 'Fetched all student score data.'
				})
			else:
				return self.get_serializer_error_response(
				serializer_errors=serializer.errors
			)
						
				
		except Exception as e:
			traceback.print_exc()
			return self.get_error_response(result={
					'code':'student_not_added',
					'error':str(e)
				})
		