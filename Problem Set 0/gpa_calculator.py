from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    std_id: str = student.id

    sum_hours_grades: float = 0.0
    sum_hours: float = 0.0

    # loop over all courses
    for c in courses:
        grade_letters: str = c.grades.get(std_id, 'not exist')

        # if this student has a grade for this course
        if grade_letters != 'not exist':
            grade_numbers: float = Course.convert_grade_to_points(c.grades[std_id])
            sum_hours_grades += (c.hours * grade_numbers) 
            sum_hours += c.hours
        
    if sum_hours_grades == 0.0:
        return 0.0
    return sum_hours_grades / sum_hours


