import csv
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Course, Enrollment
from .forms import StudentForm, CourseForm, EnrollmentForm

staff_required = staff_member_required(login_url="login")

@staff_required
def dashboard(request):
    context = {
        "student_count": Student.objects.count(),
        "active_count": Student.objects.filter(status="Active").count(),
        "course_count": Course.objects.count(),
        "enrollment_count": Enrollment.objects.count(),
        "recent_students": Student.objects.order_by("-created_at")[:6],
        "recent_enrollments": Enrollment.objects.select_related("student","course")[:6],
    }
    return render(request, "records/dashboard.html", context)

@staff_required
def student_list(request):
    q = request.GET.get("q","").strip()
    students = Student.objects.all()
    if q:
        students = students.filter(Q(student_number__icontains=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q)|Q(email__icontains=q)|Q(program__icontains=q))
    return render(request, "records/student_list.html", {"students":students, "q":q})

@staff_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save(); messages.success(request,"Student record added."); return redirect("student_list")
    return render(request,"records/form.html",{"form":form,"heading":"Add Student","back_url":"student_list"})

@staff_required
def student_edit(request, pk):
    obj=get_object_or_404(Student,pk=pk); form=StudentForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save(); messages.success(request,"Student record updated."); return redirect("student_detail",pk=obj.pk)
    return render(request,"records/form.html",{"form":form,"heading":"Edit Student","back_url":"student_list"})

@staff_required
def student_detail(request, pk):
    student=get_object_or_404(Student,pk=pk)
    return render(request,"records/student_detail.html",{"student":student,"enrollments":student.enrollments.select_related("course")})

@staff_required
def student_delete(request, pk):
    obj=get_object_or_404(Student,pk=pk)
    if request.method=="POST":
        obj.delete(); messages.success(request,"Student record deleted."); return redirect("student_list")
    return render(request,"records/confirm_delete.html",{"object":obj,"back_url":"student_list"})

@staff_required
def course_list(request):
    q=request.GET.get("q","").strip(); courses=Course.objects.all()
    if q: courses=courses.filter(Q(code__icontains=q)|Q(title__icontains=q)|Q(instructor__icontains=q))
    return render(request,"records/course_list.html",{"courses":courses,"q":q})

@staff_required
def course_create(request):
    form=CourseForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,"Course added."); return redirect("course_list")
    return render(request,"records/form.html",{"form":form,"heading":"Add Course","back_url":"course_list"})

@staff_required
def course_edit(request,pk):
    obj=get_object_or_404(Course,pk=pk); form=CourseForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,"Course updated."); return redirect("course_list")
    return render(request,"records/form.html",{"form":form,"heading":"Edit Course","back_url":"course_list"})

@staff_required
def course_delete(request,pk):
    obj=get_object_or_404(Course,pk=pk)
    if request.method=="POST":
        if obj.enrollments.exists():
            messages.error(request,"This course has enrollment records. Deactivate it instead."); return redirect("course_list")
        obj.delete(); messages.success(request,"Course deleted."); return redirect("course_list")
    return render(request,"records/confirm_delete.html",{"object":obj,"back_url":"course_list"})

@staff_required
def enrollment_list(request):
    q=request.GET.get("q","").strip(); items=Enrollment.objects.select_related("student","course")
    if q: items=items.filter(Q(student__student_number__icontains=q)|Q(student__last_name__icontains=q)|Q(course__code__icontains=q)|Q(course__title__icontains=q))
    return render(request,"records/enrollment_list.html",{"enrollments":items,"q":q})

@staff_required
def enrollment_create(request):
    form=EnrollmentForm(request.POST or None)
    if form.is_valid(): form.save(); messages.success(request,"Enrollment record created."); return redirect("enrollment_list")
    return render(request,"records/form.html",{"form":form,"heading":"New Enrollment / Grade Entry","back_url":"enrollment_list"})

@staff_required
def enrollment_edit(request,pk):
    obj=get_object_or_404(Enrollment,pk=pk); form=EnrollmentForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,"Enrollment and grades updated."); return redirect("enrollment_list")
    return render(request,"records/form.html",{"form":form,"heading":"Update Enrollment / Grades","back_url":"enrollment_list"})

@staff_required
def enrollment_delete(request,pk):
    obj=get_object_or_404(Enrollment,pk=pk)
    if request.method=="POST": obj.delete(); messages.success(request,"Enrollment removed."); return redirect("enrollment_list")
    return render(request,"records/confirm_delete.html",{"object":obj,"back_url":"enrollment_list"})

@staff_required
def export_students_csv(request):
    response=HttpResponse(content_type="text/csv")
    response["Content-Disposition"]='attachment; filename="student-records.csv"'
    writer=csv.writer(response)
    writer.writerow(["Student Number","First Name","Middle Name","Last Name","Email","Program","Year","Section","Status"])
    for s in Student.objects.all():
        writer.writerow([s.student_number,s.first_name,s.middle_name,s.last_name,s.email,s.program,s.get_year_level_display(),s.section,s.status])
    return response
