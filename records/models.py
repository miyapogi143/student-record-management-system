from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Student(models.Model):
    YEAR_LEVELS = [(1,"1st Year"),(2,"2nd Year"),(3,"3rd Year"),(4,"4th Year"),(5,"5th Year")]
    STATUS = [("Active","Active"),("Inactive","Inactive"),("Graduated","Graduated"),("Transferred","Transferred")]
    student_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    program = models.CharField(max_length=120, default="BS Information Technology")
    year_level = models.PositiveSmallIntegerField(choices=YEAR_LEVELS, default=1)
    section = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.student_number} — {self.last_name}, {self.first_name}"

    @property
    def full_name(self):
        return " ".join(p for p in [self.first_name, self.middle_name, self.last_name] if p)

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=180)
    units = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(12)])
    instructor = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.title}"

class Enrollment(models.Model):
    TERMS = [("1st Semester","1st Semester"),("2nd Semester","2nd Semester"),("Summer","Summer")]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="enrollments")
    school_year = models.CharField(max_length=9, help_text="Example: 2025-2026")
    semester = models.CharField(max_length=20, choices=TERMS, default="1st Semester")
    prelim_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    midterm_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    remarks = models.CharField(max_length=30, blank=True)
    enrolled_at = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["student__last_name", "course__code"]
        constraints = [models.UniqueConstraint(fields=["student","course","school_year","semester"], name="unique_student_course_term")]

    def __str__(self):
        return f"{self.student.student_number} / {self.course.code}"

    @property
    def average(self):
        grades = [g for g in [self.prelim_grade, self.midterm_grade, self.final_grade] if g is not None]
        return round(sum(grades) / len(grades), 2) if grades else None
