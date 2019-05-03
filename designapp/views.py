from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import values
from .models import values_data
from django.contrib import messages
from designapp.vessel import process

# Create your views here.
def home(request):
    return render(request, "home.html")

def vessel_design(request):
    form = values(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            liquid_flux = form.cleaned_data['liquid_flux']
            vapor_flux = form.cleaned_data['vapor_flux']
            liquid_density = form.cleaned_data['liquid_density']
            vapor_density = form.cleaned_data['vapor_density']
            API = form.cleaned_data['API']
            vessel_height, vessel_diameter, vessel_L_D, orientation, Vnozzle, F, K = process(liquid_flux, vapor_flux, liquid_density, vapor_density, API)
            d = values_data(liquid_flux=liquid_flux, vapor_flux=vapor_flux, liquid_density=liquid_density, vapor_density=vapor_density, API=API)
            d.save()
            context = {
                "L": vessel_height,
                "D": vessel_diameter,
                "L_D": vessel_L_D,
                "orientation": orientation
                }
            if Vnozzle > 9 and F > 37.8 and vessel_L_D < 2.5 and K > 0.7:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s, the liquid flux shouldn't be greater than 37.8 lt/min*ft^2, the relationship L/D should be greater than 2.5 and K shouldn't be greater than 0.7", extra_tags="alert")
            elif Vnozzle > 9 and F > 37.8 and vessel_L_D > 6 and K > 0.7:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s, the liquid flux shouldn't be greater than 37.8 lt/min*ft^2, the relationship L/D should be less than 6 and K should't be greater than 0.7", extra_tags="alert")
            elif Vnozzle > 9 and vessel_L_D < 2.5 and K > 0.7:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s, the relationship L/D should be greater than 2.5 and K should't be greater than 0.7", extra_tags="alert")
            elif Vnozzle > 9 and vessel_L_D > 6 and K > 0.7:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s, the relationship L/D should be less than 6 and K should't be greater than 0.7", extra_tags="alert")
            elif F > 37.8 and vessel_L_D < 2.5 and K > 0.7:
                messages.info(request, "The liquid flux shouldn't be greater than 37.8 lt/min*ft^2, the relationship L/D should be greater than 2.5 and K should't be greater than 0.7", extra_tags="alert")
            elif F > 37.8 and vessel_L_D > 6 and K > 0.7:
                messages.info(request, "The liquid flux shouldn't be greater than 37.8 lt/min*ft^2, the relationship L/D should be less than 6 and K should't be greater than 0.7", extra_tags="alert")
            elif vessel_L_D < 2.5 and K > 0.7:
                messages.info(request, "The relationship L/D should be greater than 2.5 and K should't be greater than 0.7", extra_tags="alert")
            elif vessel_L_D > 6 and K > 0.7:
                messages.info(request, "The relationship L/D should be less than 6 and K should't be greater than 0.7", extra_tags="alert")
            elif Vnozzle > 9 and K > 0.7:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s and K should't be greater than 0.7", extra_tags="alert")
            elif F > 37.8 and K > 0.7:
                messages.info(request, "The liquid flux shouldn't be greater than 37.8 lt/min*ft^2 and K should't be greater than 0.7", extra_tags="alert")
            elif Vnozzle > 9 and F > 37.8 and vessel_L_D < 2.5:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s, the liquid flux shouldn't be greater than 37.8 lt/min*ft^2 and the relationship L/D should be greater than 2.5", extra_tags="alert")
            elif Vnozzle > 9 and F > 37.8 and vessel_L_D > 6:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s, the liquid flux shouldn't be greater than 37.8 lt/min*ft^2 and the relationship L/D should be less than 6", extra_tags="alert")
            elif Vnozzle > 9 and vessel_L_D < 2.5:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s and the relationship L/D should be greater than 2.5", extra_tags="alert")
            elif Vnozzle > 9 and vessel_L_D > 6:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s and the relationship L/D should be less than 6", extra_tags="alert")
            elif F > 37.8 and vessel_L_D < 2.5:
                messages.info(request, "The liquid flux shouldn't be greater than 37.8 lt/min*ft^2 and the relationship L/D should be greater than 2.5", extra_tags="alert")
            elif F > 37.8 and vessel_L_D > 6:
                messages.info(request, "The liquid flux shouldn't be greater than 37.8 lt/min*ft^2 and the relationship L/D should be less than 6", extra_tags="alert")
            elif vessel_L_D < 2.5:
                messages.info(request, "The relationship L/D should be greater than 2.5", extra_tags="alert")
            elif vessel_L_D > 6:
                messages.info(request, "The relationship L/D should be less than 6", extra_tags="alert")
            elif Vnozzle > 9:
                messages.info(request, "The permissible inlet velocity shouldn't be greater than 9 m/s", extra_tags="alert")
            elif F > 37.8:
                messages.info(request, "The liquid flux shouldn't be greater than 37.8 lt/min*ft^2", extra_tags="alert")
            elif K > 0.7:
                messages.info(request, "K should't be greater than 0.7", extra_tags="alert")
            else:
                return render(request, "vessel_design_results.html", context)
        else:
            form = values()
    return render(request, "vessel_design.html", {'form': form})

def bibliography(request):
    return render(request, "bibliography.html")

def contact(request):
    return render(request, "contact.html")
