from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView
from todoapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from todoapp.models import Todo
from django.contrib import messages


# Create your views here.

# ctrl + alt + L ==  Align code

class SignUpView(CreateView):
    model = User
    form_class = forms.RegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"Your Account has been created")
        return super().form_valid(form)


    # def get(self, request, *args, **kwargs):
    #     form = forms.RegistrationForm()
    #     return render(request, 'registration.html', {"form": form})
    #
    # def post(self, request, *args, **kwargs):
    #     # print(request.POST.get("firstname"))
    #     # print(request.POST.get("lastname"))
    #     form = forms.RegistrationForm(request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         messages.success(request, "Your Account has been created")
    #         return redirect("signin")
    #     else:
    #         messages.error(request, "Registration Failed")
    #         return render(request, 'registration.html', {"form": form})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request, *args, **kwargs):
        # print(request.POST.get("password"))
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user = authenticate(request, username=uname, password=pwd)
            if user:
                login(request, user)
                print("login success")
                return redirect("index")
            else:
                messages.error(request, "Invalid Usename or Password")
                print("invalid credentials")
                return render(request, "login.html", {"form": form})
        return render(request, 'login.html')


class IndexView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):  # to add(render) extra contexts
        context=super().get_context_data(**kwargs)
        context["todos"]=Todo.objects.filter(user=self.request.user,status=False)
        return context
    # def get(self,request,*args,**kwargs):
    #     return render(request,'home.html')


class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")


class TodoAddView(CreateView):
    model = Todo
    form_class = forms.TodoForm
    template_name = "add-todo.html"
    success_url = reverse_lazy("todos-list")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request, "todo has been added")
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     form = forms.TodoForm()
    #     return render(request, "add-todo.html", {"form": form})
    #
    # def post(self, request, *args, **kwargs):
    #     form = forms.TodoForm(request.POST)  # works only if form is modelform  otherwise >>
    #     if form.is_valid():  # Todo.object.create(**form.cleaned_data,user=request.user)  #import todo from Todo
    #         form.instance.user = request.user
    #         form.save()
    #         messages.success(request, "Todo has been Added")
    #         return redirect("index")
    #     else:
    #         messages.error(request, "Failed to Add Todo")
    #         return render(request, "add-todo.html", {"form": form})


class TodoListView(ListView):
    model = Todo
    context_object_name = "todos"
    template_name = "todolist.html"

    def get_queryset(self):  # to customize queryset we should override get_queryset
        return Todo.objects.filter(user=self.request.user)

    # def get(self,request,*args,**kwargs):
    #     all_todos=Todo.objects.filter(user=request.user)
    #     return render(request,"todolist.html",{"todos":all_todos})


# localhost:8000/todos/remove/<int:id>
def delete_todo(request, *args, **kwargs):
    id = kwargs.get("id")
    Todo.objects.get(id=id).delete()
    messages.success(request, "Todo has been deleted")
    return redirect("todos-list")


class TodoDetailView(DetailView):
    model = Todo
    context_object_name = "todo"
    template_name = "todo-detail.html"
    pk_url_kwarg = "id"

    # def get(self, request, *args, **kwargs):
    #     id = kwargs.get("id")
    #     todo = Todo.objects.get(id=id)
    #     return render(request, "todo-detail.html", {"todo": todo})


class TodoEditView(UpdateView):
    model = Todo
    form_class = forms.TodoChangeForm
    template_name = "todo_edit.html"
    pk_url_kwarg = "id"
    success_url = reverse_lazy("todos-list")

    def form_valid(self, form):
        messages.success(self.request,"todo has been updated")
        return super().form_valid(form)


    # def get(self, request, *args, **kwargs):
    #     id = kwargs.get("id")
    #     todo = Todo.objects.get(id=id)
    #     form = forms.TodoChangeForm(instance=todo)
    #     return render(request, "todo_edit.html", {"form": form})
    #
    # def post(self, request, *args, **kwargs):
    #     id = kwargs.get("id")
    #     todo = Todo.objects.get(id=id)
    #     form = forms.TodoChangeForm(request.POST, instance=todo)
    #     if form.is_valid():
    #         form.save()
    #         msg = "todo has been changed"
    #         messages.success(request, msg)
    #         return redirect("todos-list")
    #     else:
    #         msg = "todo update failed!"
    #         messages.error(request, msg)
    #         return render(request, 'todo_edit.html', {'form': form})

# create  ==> class CreateView()
# edit    ==> class UpdateView()
# list    ==> class ListView()
# delete  ==> class Delete()
# detail  ==> class DetailView()

# class TemplateView()  to render template
# class FormView()
