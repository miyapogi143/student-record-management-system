from django.core.management.base import BaseCommand
from records.models import Student, Course, Enrollment

class Command(BaseCommand):
    help = "Create realistic sample students, courses, and enrollment records."
    def handle(self, *args, **options):
        courses_data = [
            ("IT101","Introduction to Computing",3,"Prof. Maria Santos"),
            ("IT102","Computer Programming 1",3,"Mr. Daniel Reyes"),
            ("IT203","Database Management Systems",3,"Engr. Angela Cruz"),
            ("IT204","Web Development",3,"Mr. Carlo Mendoza"),
            ("GE101","Purposive Communication",3,"Ms. Liza Garcia"),
            ("MATH201","Discrete Mathematics",3,"Dr. Ramon Dela Peña"),
        ]
        courses={}
        for code,title,units,teacher in courses_data:
            c,_=Course.objects.get_or_create(code=code,defaults={"title":title,"units":units,"instructor":teacher})
            courses[code]=c
        students_data = [
            ("2024-0001","Alyssa","Mae","Reyes","alyssa.reyes@example.com",2,"A"),
            ("2024-0002","Joshua","Miguel","Santos","joshua.santos@example.com",2,"A"),
            ("2023-0015","Nicole","Anne","Cruz","nicole.cruz@example.com",3,"B"),
            ("2022-0042","Mark","Luis","Dela Peña","mark.delapena@example.com",4,"A"),
            ("2025-0008","Sofia","","Mendoza","sofia.mendoza@example.com",1,"A"),
            ("2024-0021","Gabriel","Jose","Garcia","gabriel.garcia@example.com",2,"B"),
            ("2023-0030","Kyla","Rose","Villanueva","kyla.villanueva@example.com",3,"A"),
            ("2022-0061","Nathan","","Aquino","nathan.aquino@example.com",4,"B"),
        ]
        students=[]
        for number,first,middle,last,email,year,section in students_data:
            s,_=Student.objects.get_or_create(student_number=number,defaults={
                "first_name":first,"middle_name":middle,"last_name":last,"email":email,
                "program":"BS Information Technology","year_level":year,"section":section,
                "contact_number":"09XX-XXX-XXXX","gender":"Prefer not to say","address":"Cagayan, Philippines","status":"Active"})
            students.append(s)
        for i,s in enumerate(students):
            for code in (["IT101","GE101"] if i<2 else ["IT203","IT204"] if i<4 else ["IT101","IT102"]):
                Enrollment.objects.get_or_create(student=s,course=courses[code],school_year="2025-2026",semester="1st Semester",
                    defaults={"prelim_grade":88+i%7,"midterm_grade":89+i%6,"final_grade":90+i%5,"remarks":"Passed"})
        self.stdout.write(self.style.SUCCESS("Demo data ready: 8 sample students, 6 courses, and sample enrollments."))
