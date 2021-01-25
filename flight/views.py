from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from .forms import CustomUserCreationForm,FlightForm,ContactForm,UserEditForm,InputDataForm
from .models import Flight,Input_Data,Contact
from flight.recommender import flightRecommender
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
import pandas as pd 
import json 
from django.views.decorators.csrf import csrf_exempt
from flight.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

# Create your views here.
def homepage(request):
	return render(
			request,
			'main/home.html'
		)
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                dj_login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                if request.user.is_superuser:
                    return render(
                    request,
                    'main/cpanel.html'
                                    )
                else:
                    return render(
                    request,
                    'main/cpanel1.html')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(
            request,
            'main/home.html'
        )

def signup(request):
    

    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
        
            return HttpResponseRedirect('/')
        else:
            print(form.errors)
        
    else:
        form = CustomUserCreationForm()
        args = {'form' : form }

            
        return render(
         request,
         'main/signup.html',args
        )
@login_required
def cpanel(request):
    return render(
        request,
        "main/cpanel.html"
        )

@login_required
def cpanel1(request):
    return render(
        request,
        "main/cpanel1.html"
        )
@login_required
def show_flight(request):
    return render(
        request,
        "main/show_flight.html"
        )

'''@login_required
def book_flight(request):
    if request.method == "POST":
        selectedfrom = request.POST.get('flying_from')
        selectedto = request.POST.get('flying_to')
        selecteddate = request.POST.get('departing')
        selectedclass = request.POST.get('travel_class')
        filter_flight = Travelling.objects.filter(From_place = selectedfrom, To_place = selectedto, Date = selecteddate,Travel_class = selectedclass)
        filter_flight = Flight.objects.filter(From_place = selectedfrom, To_place = selectedto,Date = selecteddate,Travel_class = selectedclass)
        print(request.POST)

    return render(request,
        'main/Restaurant_Order_Form.html',
         {'all_flight': filter_flight}
        )'''

@login_required
def book_flight(request):
    if request.method=="POST":
        selectedfrom = request.POST.get('flying_from')
        selectedto = request.POST.get('flying_to')
        selecteddate = request.POST.get('departing')
        selectedclass = request.POST.get('travel_class')
        selectedpassenger=request.POST.get('passenger')
        request.session['selectedpassenger'] = selectedpassenger
        filter_flight = Flight.objects.filter(From_place = selectedfrom, To_place = selectedto,Date = selecteddate,Travel_class = selectedclass,Available__gte = selectedpassenger)
        print(filter_flight)
        user1=request.user
        mylist=Input_Data.objects.filter(user_name=user1).values('airline_name','overall_rating')
        list_flight=[]
        for t in filter_flight:
            list_flight.append(t.Flight)
        r1=flightRecommender()
        userSubsetgroup,inputflights,user_df=r1.preprocessing(mylist,list_flight)
        result = r1.recommend(userSubsetgroup,inputflights,user_df)
        #print(result['airline_name'])
        #print(filter_flight.values())
        df=pd.DataFrame((filter_flight.values()))

        df=df[df['Flight'].isin(result['airline_name'])]
        #print(df)
        df1=df.merge(result,left_on='Flight',right_on='airline_name')
        #print(df1)
        #print(list(df1.columns))
        #json_records = result.reset_index().to_json(orient ='records') 
        #data = [] 
        #data = json.loads(json_records) 
        json_records1=df1.reset_index().to_json(orient='records')
        flight=[]
        flight=json.loads(json_records1)
        
        context = {'f':flight}
        return render(request, 'main/result1.html', context)
    


class Book(LoginRequiredMixin,View):
    model=Flight
    template='main/book1.html'
    
    def get(self,request,pk):
        flight=get_object_or_404(self.model,pk=pk)
        
        form=FlightForm(instance=flight)
        context={'form':form}
        return render(request,self.template,context)
    def post(self,request,pk):
        flight=get_object_or_404(self.model,pk=pk)
        selectedpassenger = request.session['selectedpassenger']

        flight.Available=flight.Available-int(selectedpassenger)
        print(flight.Available)
        flight.save()
        return redirect("/cpanel1")
class Manage_flight(LoginRequiredMixin,View):

    template='main/manage_flight2.html'
    def get(self,request):
        flight=Flight.objects.all()
        context={'flight_list':flight}
        
        return render(request,self.template,context)
class Create_flight(LoginRequiredMixin,View):
    """docstring for Manage_flight"""
    template ='main/create_flight.html'
    def get(self,request):
        form=FlightForm()
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request):
        form=FlightForm(request.POST)
        if not form.is_valid():
            context={form:form}
            return render(request,self.template,context)

        form.save()
        return redirect('/manage')


class Update_flight(LoginRequiredMixin,View):
    """docstring for ClassName"""
    model=Flight
    template='main/update_flight.html'
    def get(self,request,pk):
        flight=get_object_or_404(self.model,pk=pk)
        form=FlightForm(instance=flight)
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request,pk):
        flight=get_object_or_404(self.model,pk=pk)
        form=FlightForm(request.POST,instance=flight)
        if not form.is_valid():
            context={'form':form}
            return render(request,self.template,context)

        form.save()
        return redirect('/manage')

class Delete_flight(LoginRequiredMixin,View):
    """docstring for Delete_flight"""
    model=Flight
    template='main/confirm_delete_flight.html'
    def get(self,request,pk):
        flight=get_object_or_404(self.model,pk=pk)
        form=FlightForm(instance=flight)
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request,pk):
        flight=get_object_or_404(self.model,pk=pk)
        flight.delete()
        return redirect('/manage')
        

class Profile(LoginRequiredMixin,View):
    """docstring for Profile"""
    
    template='main/profile.html'
    def get(self,request):
        user1=request.user
        print(user1.id)
        context={'user_list':user1}
        
        return render(request,self.template,context)  
        
class Profile_update(LoginRequiredMixin,View):
    """docstring for ClassName"""
    model=User
    template='main/profile_update.html'
    def get(self,request,pk):
        user1=get_object_or_404(self.model,pk=pk)
        form=CustomUserCreationForm(instance=user1)
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request,pk):
        user1=get_object_or_404(self.model,pk=pk)
        form=CustomUserCreationForm(request.POST,instance=user1)
        if not form.is_valid():
            context={'form':form}
            return render(request,self.template,context)

        form.save()
        return redirect('/profile')



class Contact(LoginRequiredMixin,View):
    template ='main/contact.html'
    def get(self,request):
        form=ContactForm()
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request):
        form=ContactForm(request.POST)
        if not form.is_valid():
            context={form:form}
            return render(request,self.template,context)

        form.save()
        return redirect('/')



    """docstring for Profile"""
@login_required
def View_Ratings(request):
    user1=request.user
    print(user1.username)
    mylist=Input_Data.objects.filter(user_name=user1).values()
    context={'input':mylist}
        
    return render(request,'main/view_ratings.html',context)  
class Add_Ratings(LoginRequiredMixin,View):
    """docstring for Manage_flight"""
    template ='main/add_ratings.html'
    def get(self,request):
        form=InputDataForm()
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request):
        form=InputDataForm(request.POST)
        if not form.is_valid():
            context={'form':form}
            return render(request,self.template,context)

        form.save()
        return redirect('/rating')