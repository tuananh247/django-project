from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Submission, Question, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Logic xử lý nộp bài
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Quét các câu trả lời
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice_id = value
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
                
        submission.save()
        return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)
    
    return render(request, 'onlinecourse/course_details.html', {'course': course})

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Tính điểm giả lập
    score = 80 # Ví dụ điểm
    passed = score >= 70
    
    context = {
        'course': course,
        'submission': submission,
        'score': score,
        'passed': passed
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
