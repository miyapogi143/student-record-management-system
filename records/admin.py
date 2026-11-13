from django.contrib import admin
from .models import Student, Course, Enrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=("student_number","last_name","first_name","program","year_level","status")
    list_filter=("program","year_level","status")
    search_fields=("student_number","first_name","last_name","email")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=("code","title","units","instructor","is_active")
    list_filter=("is_active",)
    search_fields=("code","title","instructor")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display=("student","course","school_year","semester","prelim_grade","midterm_grade","final_grade","remarks")
    list_filter=("school_year","semester","remarks")
    search_fields=("student__student_number","student__last_name","course__code")
