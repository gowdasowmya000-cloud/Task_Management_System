from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from .models import PasswordResetOTP



# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):

    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user=request.user)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):

    print("DATA:", request.data)
    print("USER:", request.user)

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    print(serializer.errors)
    return Response(serializer.errors)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, id):

    task = Task.objects.get(id=id)
    serializer = TaskSerializer(task, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

    return Response(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request,id):

    task = Task.objects.get(id=id)
    task.delete()

    return Response({"message":"Task deleted"})

@api_view(['POST'])
def login_api(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)

    if user:

        login(request,user)
        return Response({'success':True})

    return Response({'success':False})

@api_view(['GET'])
def logout_api(request):

    logout(request)
    return Response({'success':True})


@api_view(['POST'])
def send_otp(request):

    # print("SEND OTP API CALLED")
    # print("REQUEST DATA:", request.data)

    email = request.data.get('email')

    print("EMAIL:", email)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email'})

    otp = str(random.randint(100000,999999))

    # print("Sending OTP to:", user.email)
    # print("OTP:", otp)

    PasswordResetOTP.objects.create(
        user=user,
        otp=otp
    )

    send_mail(
        'Password Reset OTP',
        f'Your OTP is {otp}',
        'gowdasowmya000@gmail.com',
        [user.email],
        fail_silently=False,
    )

    # print("Email Sent Successfully")

    return Response({'message': 'OTP sent'})


@api_view(['POST'])
def verify_otp(request):

    email = request.data.get('email')
    otp = request.data.get('otp')

    try:
        user = User.objects.get(email=email)

        record = PasswordResetOTP.objects.filter(
            user=user,
            otp=otp
        ).last()

        if record:
            return Response({'success':True})

        return Response({'success':False})

    except:
        return Response({'error':'Invalid'})
    

@api_view(['POST'])
def reset_password(request):

    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.get(email=email)
    user.set_password(password)
    user.save()

    return Response({'message':'Password Reset Successful'})


def login_page(request):
    return render(request,'login.html')

@login_required
def dashboard_page(request):
    return render(request,'dashboard.html')

def add_task_page(request):
    return render(request,'add_task.html')

def update_task_page(request,id):
    return render(request,'update_task.html')

@login_required
def profile_page(request):

    if request.user.is_superuser:
        task_count = Task.objects.all().count()
    else:
        task_count = Task.objects.filter(user=request.user).count()

    return render(request,'profile.html',{
        'task_count':task_count
    })


