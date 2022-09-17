from django.shortcuts import render,redirect
from django.views.generic import View
from todoapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todoapp.models import Todo

# Create your views here.

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=forms.RegistrationForm()
        return render(request,'registration.html',{"form":form})

    def post(self,request,*args,**kwargs):
        # print(request.POST.get("firstname"))
        # print(request.POST.get("lastname"))
        form=forms.RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("signin")
        else:
            return render(request, 'registration.html',{"form":form})

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,'login.html',{"form":form})

    def post(self,request,*args,**kwargs):
        # print(request.POST.get("password"))
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("login success")
                return redirect("index")
            else:
                print("invalid credentials")
                return render(request,"login.html",{"form":form})
        return render(request,'login.html')

class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'home.html')

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

class TodoAddView(View):
    def get(self,request,*args,**kwargs):
        form=forms.TodoForm()
        return render(request,"add-todo.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=forms.TodoForm(request.POST)    #works only if view is modelview  otherwise >>
        if form.is_valid():                  #Todo.object.create(**form.cleaned_data,user=request.user)  #import todo from Todo
            form.instance.user=request.user
            form.save()
            return redirect("index")
        else:
            return render(request,"add-todo.html",{"form":form})

class TodoListView(View):
    def get(self,request,*args,**kwargs):
        all_todos=Todo.objects.filter(user=request.user)
        return render(request,"todolist.html",{"todos":all_todos})

# localhost:8000/todos/remove/<int:id>
def delete_todo(request,*args,**kwargs):
    id=kwargs.get("id")
    Todo.objects.get(id=id).delete()
    return redirect("todos-list")

class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        todo=Todo.objects.get(id=id)
        return render(request,"todo-detail.html",{"todo":todo})