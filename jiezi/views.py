"""
This view serves only the basic website structure like index page
"""
from django.shortcuts import render, redirect, reverse
from django.http.response import Http404
from classroom.models import Student
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


def index(request):
    if request.user.is_staff and \
            not (request.user.is_student or request.user.is_teacher):
        request.user.is_student = True
        Student.of(request.user)
        request.user.save()

    if not request.user.is_authenticated:
        return render(request, 'unauthenticated_index.html')
    elif request.user.is_student:
        return redirect(reverse('student_dashboard'))
    elif request.user.is_teacher:
        return redirect(reverse('class_list'))
    else:
        raise Http404("You not a student or teacher")


def about_us(request):
    return render(request, 'about_us.html')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user_detail': reverse('user_detail', request=request, format=format),
    })
