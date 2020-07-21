from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request):
    allPosts= Post.objects.all()
    context={'allPosts':allPosts}
    return render(request, 'home/home.html',context)

def about(request):
    return render(request, 'home/about.html')
    
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,"Your message has been sent successfully")
    return render(request, 'home/contact.html')

def search(request):
    query=request.GET['query']
    if len(query)>78 or len(query)==0:
        allPosts = Post.objects.none()
    else:
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPosts= allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.warning(request, "No search found. Please refine your query")
    params={'allPosts': allPosts, 'query':query}
    return render(request,'home/search.html',params)

def handleSignup(request):
    if request.method == 'POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #check for error

        if len(username)>15:
            messages.error(request,"Username should not exceed 15 character")
            return redirect('home')

        if not username.isalnum():
            messages.error(request,"Username should only contain alphanumeric characters")
            return redirect('home')
        if len(pass1) < 8:
            messages.error(request,"Your password should always contains atleast 8 characters")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,"Your Password does not matched")
            return redirect('home')
        #create user
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your Popgut account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']
        user= authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request,"Logged In Successfully")
            return redirect('home')
        else:
            messages.error(request,"Your Username and Password does not match")
            return redirect('home')

    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('home')