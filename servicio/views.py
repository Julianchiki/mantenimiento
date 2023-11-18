from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Cars, Appointments, Record
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import AddQuote

# Create your views here.

def signin(request):
    if request.method == 'GET':
        return render(request, 'authentication/login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'authentication/login.html', {'error': 'Credenciales incorrectas'})
        else:
            login(request, user)
            if user.groups.filter(name='Mecánico').exists():
                return redirect('request')
            else:
                return redirect('quote')
                
        
def register(request):
    if request.method == 'GET':
        return render(request, 'authentication/register.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=request.POST['password1'], email=request.POST['email'])
                
                # Asignar el usuario al grupo "Cliente"
                cliente_group, created = Group.objects.get_or_create(name='Cliente')
                user.groups.add(cliente_group)

                user.save()
                login(request, user)
                return redirect('login')
            except:
                return render(request, 'authentication/register.html', {'error': 'El usuario ya existe'})
        return render(request, 'authentication/register.html', {'error': 'No coinciden las contraseñas ingresadas'})

def signout(request):
    logout(request)
    return redirect('login')

def car(request):
    title = 'Autos'
    user_id = request.user.id
    cars = Cars.objects.filter(user_id = user_id)
    return render(request, 'client/cars/index.html', {'title': title, 'cars': cars})

def add_car(request):
    title = 'Autos'
    cars = Cars.objects.all()
    if request.method == 'POST':
        plate = request.POST['plate']
        model = request.POST['model']
        color = request.POST['color']
        user_id = request.user.id
        if plate:
            Cars.objects.create(plate=plate, model=model, color=color, user_id=user_id)
            # Puedes redirigir a una página de éxito o hacer lo que necesites aquí.
            return redirect('car')  # Cambia 'exito' por la URL a la que deseas redirigir.
        # Si los datos del formulario no son válidos, puedes manejar los errores aquí.
    return render(request, 'client/cars/index.html', {'title': title, 'cars': cars})  # Cambia 'tu_template.html' por el nombre de tu plantilla modal.

def edit_car(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        plate = request.POST.get('plate')
        model = request.POST['model']
        color = request.POST['color']
        
        # Obtener el objeto de la categoría a editar
        car = get_object_or_404(Cars, id=car_id)
        
        # Actualizar los datos
        car.plate = plate
        car.model = model
        car.color = color
        car.save()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('car')
    else:
        return JsonResponse({'error': 'Método no permitido'})
    
def delete_car(request):
    if request.method == 'POST':
        car_id = request.POST.get('delete_car_id')
        
        # Obtener el objeto de la categoría a editar
        car = get_object_or_404(Cars, id=car_id)
        
        # Actualizar los datos
        car.delete()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('car')
    else:
        return JsonResponse({'error': 'Método no permitido'})

def request(request):
    title = 'Citas'
    appointments = Appointments.objects.all()
    return render(request, 'mechanic/request.html', {'title': title, 'appointments': appointments})

def quote(request):
    title = 'Apartar Citas'
    user = request.user  # Obtener el usuario actual
    form = AddQuote(user=user)

    # Obtener el ID del usuario actual
    user_id = request.user.id

    # Filtrar los autos asociados al usuario actual
    cars = Cars.objects.filter(user_id=user_id)

    # Inicializar la variable appointments con un queryset vacío
    appointments = Appointments.objects.none()

    # Si hay al menos un auto asociado al usuario, obtener el primer auto y las citas asociadas
    if cars.exists():
        car = cars.first()
        appointments = Appointments.objects.filter(car=car)

    return render(request, 'client/quotes/index.html', {'title': title, 'form': form, 'appointments': appointments})

def add_quote(request):
    title = 'Apartar Citas'
    user = request.user  # Obtener el usuario actual
    form = AddQuote(user=user)
    appointments = Appointments.objects.all()
    if request.method == 'POST':
        date = request.POST['date']
        car_id = request.POST['car_id']
        observation = request.POST['observation']
        state = 'PENDIENTE'
        if car_id:
            Appointments.objects.create(date=date, car_id=car_id, observation=observation, state=state)
            # Puedes redirigir a una página de éxito o hacer lo que necesites aquí.
            return redirect('quote')  # Cambia 'exito' por la URL a la que deseas redirigir.
        # Si los datos del formulario no son válidos, puedes manejar los errores aquí.
    return render(request, 'client/quotes/index.html', {'title': title, 'form': form, 'appointments': appointments})  # Cambia 'tu_template.html' por el nombre de tu plantilla modal.

def cancel_quote(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        
        # Obtener el objeto de la categoría a editar
        quote = get_object_or_404(Appointments, id=quote_id)
        
        # Actualizar los datos
        quote.state = 'CANCELADO'
        quote.save()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('quote')
    else:
        return JsonResponse({'error': 'Método no permitido'})

def procces(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        
        # Obtener el objeto de la categoría a editar
        quote = get_object_or_404(Appointments, id=quote_id)
        
        # Actualizar los datos
        quote.state = 'PROCESO'
        quote.save()
        
        # Redirigir al usuario a la página deseada, por ejemplo:
        return redirect('request')
    else:
        return JsonResponse({'error': 'Método no permitido'})

def complete(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        observation = request.POST['observation']
        user_id = request.user.id
        if quote_id:
            quote = get_object_or_404(Appointments, id=quote_id)
            # Actualizar los datos
            quote.state = 'COMPLETADO'
            quote.save()

            Record.objects.create(observation=observation, appointment_id=quote_id, user_id=user_id)
            
            # Redirigir al usuario a la página deseada, por ejemplo:
            return redirect('request')
    else:
        return JsonResponse({'error': 'Método no permitido'})

def record(request):
    title = 'Mis historiales'
    mechanic =  request.user.id
    records = Record.objects.filter(user_id = mechanic)
    return render(request, 'mechanic/my_quotes.html', {'title': title,'records': records})
