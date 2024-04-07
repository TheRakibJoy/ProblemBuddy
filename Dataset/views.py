from django.shortcuts import render,redirect
from .models import Handle
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages
from .add_data import Data_Entry
def Train(request):
    if request.method == 'POST':
        handle = request.POST.get('handle')
        if (handle is not None):
            print(handle)
            handle = handle.lower()
            try:
                obj = Handle.objects.get(handle=handle)
                messages.error(request, "Handle Data Already Trained.")
                return redirect('train')
            except Handle.DoesNotExist:
                ob = Handle(
                    handle=handle
                )
                ob.save()
                Data_Entry(handle, 0, 1200)
                Data_Entry(handle, 1201, 1400)
                Data_Entry(handle, 1401, 1600)
                Data_Entry(handle, 1601, 1900)
                Data_Entry(handle, 1901, 2100)
                messages.success(request,"Data Trained for Handle : "+handle)
                return redirect('train')
        else:
            messages.error(request, "Handle Not Found.")
    else:
        return render(request, 'input_handle.html')