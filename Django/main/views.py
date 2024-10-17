from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *

from .forms import ParkingForm

def create_parking(request):
    if request.method == 'POST':
        form = ParkingForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('parking_list') 
    else:
        form = ParkingForm()
    
    return render(request, 'create_parking.html', {'form': form})

def edit_parking(request, parking_id):
    parking = get_object_or_404(Parking, id=parking_id)  # Fetch the Parking instance
    if request.method == 'POST':
        form = ParkingForm(request.POST, instance=parking)  # Bind the form to the instance
        if form.is_valid():
            form.save()  # Save the updated Parking record
            return redirect('parking_list')  # Redirect to the parking list page
    else:
        form = ParkingForm(instance=parking)  # Pre-fill the form with the current instance data
    
    return render(request, 'edit_parking.html', {'form': form, 'parking': parking})

def test(request):
    html = '<h1> Hello world! </h1>'
    return HttpResponse(html)


def model_list(request):
    models = Model.objects.select_related('manufacture').all()
    return render(request, 'model_list.html', {'models': models})

def parking_list(request):
    parkings = Parking.objects.all()
    return render(request, 'parking_list.html', {'parkings': parkings})