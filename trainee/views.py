# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView
)
from rest_framework import viewsets
from django.contrib import messages
from .models import Trainee
from course.models import Course
from .forms import TraineeForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from trainee.serializers import TraineeSerializer
from rest_framework import generics
from rest_framework.decorators import api_view


class TraineeListView(ListView):
    model = Trainee
    template_name = 'listtrainee.html'
    context_object_name = 'trainees'

    def get_queryset(self):
        return Trainee.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(status=True)
        return context
        return context


class TraineeDetailView(DetailView):
    model = Trainee
    template_name = 'trainee_detail.html'
    context_object_name = 'trainee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(status=True)
        return context


class TraineeDeleteView(SuccessMessageMixin, DeleteView):
    model = Trainee
    template_name = 'trainee_confirm_delete.html'
    success_url = reverse_lazy('traineeList')
    success_message = "Trainee was successfully deactivated."

    def delete(self, request, *args, **kwargs):
        # Soft delete instead of actual deletion
        trainee = self.get_object()
        trainee.status = False
        trainee.save()
        return super().delete(request, *args, **kwargs)


class TraineeCreateView(SuccessMessageMixin, CreateView):
    model = Trainee
    form_class = TraineeForm
    template_name = 'addTrainee.html'
    success_url = reverse_lazy('traineeList')
    success_message = "Trainee was created successfully."

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class TraineeUpdateView(SuccessMessageMixin, UpdateView):
    model = Trainee
    form_class = TraineeForm
    template_name = 'editTrainee.html'
    success_url = reverse_lazy('traineeList')
    success_message = "Trainee was updated successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(status=True)
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


def deleteTrainee(request, id):
    trainee = get_object_or_404(Trainee, id=id)
    trainee.status = False
    trainee.save()
    messages.success(request, 'Trainee deactivated successfully!')
    return redirect('traineeList')


class TraineeListCreateView(APIView):
    def get(self, request):
        trainees = Trainee.objects.all()
        serializer = TraineeSerializer(trainees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TraineeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TraineeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer


@api_view(['GET'])
def track_update(request, pk):
    try:
        trainee = Trainee.objects.get(pk=pk)
    except Trainee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TraineeSerializer(trainee)
        return Response(serializer.data)


class TraineeListCreateView(APIView):
    def get(self, request):
        trainees = Trainee.objects.all()
        serializer = TraineeSerializer(trainees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TraineeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TraineeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer


@api_view(['GET'])
def track_update(request, pk):
    try:
        trainee = Trainee.objects.get(pk=pk)
    except Trainee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TraineeSerializer(trainee)
        return Response(serializer.data)


class TraineeViewSet(viewsets.ModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer