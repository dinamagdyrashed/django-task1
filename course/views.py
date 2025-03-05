from django.shortcuts import render ,redirect

# Create your views here.


def courseList(request):
    courses=[{"id":1,"name":"Django"},{"id":2,"name":"React"},{"id":3,"name":"node js"}]
    return render(request,'courseList.html',{"courses":courses})


def addCourse(requset):
    return render(requset,'courseForm.html')

def updateCourse(requset,id):
    print(id)
    return redirect('courseList')

def deleteCourse(requset,id):
    print(id)
    return redirect('courseList')