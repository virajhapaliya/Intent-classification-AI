from rest_framework import serializers
from professors.utils.base_serializer import BaseSerializerSerializer
from students import models as student_models

class AddStudentSerializer(BaseSerializerSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    student_id = serializers.CharField()

class AddScoreSerializer(BaseSerializerSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    subject_name = serializers.CharField()
    score = serializers.CharField()

class SubjectScoreSerializer(BaseSerializerSerializer):
    subject_name = serializers.CharField()

class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = student_models.Student
        fields = ['first_name','last_name','student_id']  

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = student_models.Subject
        fields = ['name'] 


class SubjectInfoSerializer(serializers.ModelSerializer):
    # subject_name = SubjectSerializer()
    subject_name = serializers.SerializerMethodField()
    # student_name = serializers.SerializerMethodField()
    class Meta:
        model = student_models.Score
        fields = ['subject_name']  
    def get_subject_name(self, obj):
        return obj.subject.name
    
    # def get_student_name(self,obj):
    #     return obj.student.first_name +" "+ obj.student.last_name
    
class ScoreSerializer(serializers.ModelSerializer):
    # subject_name = SubjectSerializer()
    subject_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = student_models.Score
        fields = ['subject_name','score','student_name']  
    def get_subject_name(self, obj):
        return obj.subject.name
    
    def get_student_name(self,obj):
        return obj.student.first_name +" "+ obj.student.last_name

class StudentInfoSerializer(BaseSerializerSerializer):
    first_name = serializers.CharField(required=False,allow_blank=True)
    last_name = serializers.CharField(required=False,allow_blank=True)
    student_id = serializers.CharField(required=False,allow_blank=True)
