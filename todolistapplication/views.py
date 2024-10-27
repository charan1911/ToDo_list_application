from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib import messages 
from . models import todolist 
from django.contrib.auth.decorators import login_required


def logoutpage(request):
    logout(request)
    return redirect("login-page")


@login_required
def deletetask(request, name):
    get_todo = todolist.objects.filter(user=request.user, todo_name=name).first()  # Get the first matching todo
    if get_todo:  # Check if a task exists
        get_todo.delete()
    return redirect("todolist-page")



@login_required
def taskmark(request, name):
    get_todo = todolist.objects.filter(user=request.user, todo_name=name).first()  # Get the first matching task
    
    if get_todo:
        get_todo.status = True
        get_todo.save()
        messages.success(request, "Task marked as complete.")
    else:
        messages.error(request, "Task not found.")
    
    return redirect("todolist-page")

# Home Page 
def login(request):
    if request.user.is_authenticated:
        return redirect('todolist-page')
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get("pass")

        check_user_exists = authenticate(username=username, password=password)
        if check_user_exists is not None:
            auth_login(request, check_user_exists)
            messages.error(request, "Successfully loggedin.")
            return redirect("todolist-page")
        else:
            messages.error(request, "Wrong details/User not exist.")
            return redirect("login-page")
    return render(request, "loginpage.html")

#Register page
def register(request):
    if request.user.is_authenticated:
        return redirect('todolist-page')
    if request.method == "POST" :
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if len(password) < 3:
            messages.error(request, "Password must be atleast two Characters.")
            return redirect("register-page")
        
        existed_username = User.objects.filter(username=username)
        if existed_username:
            messages.error(request, "username already exist's")
            return redirect("register-page")


        #print(username,email,password)  
        #Above line will Print the username,Email,Password in CMD

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.error(request, "Account created.")
        return redirect("login-page")
    return render(request, "registerpage.html", {})





@login_required
def todolists(request):
    if request.method == "POST":
        task = request.POST.get('task')
        if task:  # Check if task is not empty
            new_todo = todolist(user=request.user, todo_name=task)
            new_todo.save()
            messages.success(request, "Task added successfully.")
        else:
            messages.error(request, "Task cannot be empty.")
        
        # After saving, redirect to prevent form resubmission on refresh
        return redirect("todolist-page")

    # Get all tasks for the logged-in user
    all_tasks = todolist.objects.filter(user=request.user)
    content = {
        "todos": all_tasks,
        "username": request.user.username
    }

    return render(request, "todolistpage.html", content)

"""
def todolist(request):
    if request.method == "POST":
        task = request.POST.get('task')
        new_todo = todolist(User=request.user, todo_name=task)  
        new_todo.save()

    return render(request, "todolistpage.html", {})"""
