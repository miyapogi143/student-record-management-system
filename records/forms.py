from django import forms
from .models import Student, Course, Enrollment

class DateInput(forms.DateInput):
    input_type = "date"

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_number","first_name","middle_name","last_name","email","contact_number","birth_date","gender","address","program","year_level","section","status"]
        widgets = {"birth_date": DateInput(), "address": forms.Textarea(attrs={"rows": 2})}

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["code","title","units","instructor","description","is_active"]
        widgets = {"description": forms.Textarea(attrs={"rows": 2})}

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["student","course","school_year","semester","prelim_grade","midterm_grade","final_grade","remarks"]
        widgets = {"student": forms.Select(attrs={"class":"form-select"}), "course": forms.Select(attrs={"class":"form-select"})}


# Apply consistent styling to all generated controls.
for form_class in (StudentForm, CourseForm, EnrollmentForm):
    for field in form_class.base_fields.values():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.setdefault("class", "form-check-input")
        elif isinstance(field.widget, forms.Select):
            field.widget.attrs.setdefault("class", "form-select")
        else:
            field.widget.attrs.setdefault("class", "form-control")
