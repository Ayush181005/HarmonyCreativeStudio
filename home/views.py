from django.shortcuts import render, HttpResponse, redirect
from datetime import date, datetime
from home.models import Contact, Testimonial, Portfolio, Client, TeamMember, broadcasted_message
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from math import ceil
from django.core.mail import send_mail
# import smtplib

def home(request):
    # GMAIL_ID = ''
    # GMAIL_PSWD = ''

    current_date = date.today()
    current_year = current_date.year
    experience = current_year - 2002

    isPost = False
    isHome = True

    allPosts = Post.objects.all()
    for post in allPosts:
        t1 = datetime.strptime('10/18/2005', "%m/%d/%Y")
        t2 = datetime.strptime('10/16/2005', "%m/%d/%Y")
        deltaTwo = t1 - t2
        # diff = current_date-post.timeStamp.date()
        # if(diff<=deltaTwo):
        #     isPost = True
        if current_date-post.timeStamp.date()<=deltaTwo:
            isPost = True
    
    if(isPost):
        messages.info(request, 'There is a <a class="text-dark" href="/blog/'+post.slug+'">Post</a> uploaded by HarmonyCreativeStudio in last 2 days, to view that go to the <a class="text-dark" href="/blog">Blog Page</a>!')

    allTestimonials = Testimonial.objects.all()
    allClients = Client.objects.all()
    allPortfolios = Portfolio.objects.all()
    allTeamMembers = TeamMember.objects.all()
    allBroadcastedMessages = broadcasted_message.objects.all()

    for broadcastedMessage in allBroadcastedMessages:
        t1 = datetime.strptime('10/18/2005', "%m/%d/%Y")
        t2 = datetime.strptime('10/'+str(18 - broadcastedMessage.activeDays)+'/2005', "%m/%d/%Y")
        deltaTwo = t1 - t2
        if current_date-broadcastedMessage.timeStamp.date() < deltaTwo:
            messages.info(request, broadcastedMessage.msg)

    params = {'experience':experience, 'allTestimonials':allTestimonials, 'allClients': allClients, 'allPortfolios': allPortfolios, 'isHome': isHome, 'allTeamMembers': allTeamMembers}

    messageForContact = False

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        content = request.POST['content']
        if len(name)<2 or len(content)<4:
            messages.error(request, 'The length of name must be 2 characters or content must have atleast 4 characters!')
            isError = True
        else:
            contact = Contact(name=name, email=email, subject=subject, content=content)
            contact.save()

            send_mail("Contact Recieved", f"There is a message from {contact.name} through the Contact Us form on harmonycreativestudio.in.\nMailID of Contact: {contact.email}\nSubject: {contact.subject}\nMessage: {contact.content}", 'hcstudio14@gmail.com', ['info@harmonycreativestudio.in'], fail_silently=False)

            messages.success(request, 'Your message has been sent! We will get back to you shortly!')
            isError = False
        messageForContact = True
        params2 = {'messageForContact': messageForContact}
        params.update(params2)
        if isError:
            params.update({'isError': isError, 'errName':name, 'errEmail':email, 'errSubject':subject, 'errContent':content})
    return render(request, 'home/index.html', params)

def portfolio(request):
    allPortfolios = Portfolio.objects.all()
    params = {'allPortfolios': allPortfolios}
    return render(request, 'home/portfolio.html', params)

def dispPortfolio(request, slug):
    allPortfolios = Portfolio.objects.all()
    portfolio = Portfolio.objects.filter(slug=slug).first()
    portfolio.save()

    nextSno = 1
    prevSno = 1
    currentSno = portfolio.sno
    if len(allPortfolios) == currentSno:
        nextSno = 1
    else:
        nextSno = currentSno + 1
    if currentSno == 1:
        prevSno = len(allPortfolios)
    else:
        prevSno = currentSno - 1
    nextPortfolio = Portfolio.objects.filter(sno=nextSno).first()
    nextPortfolio.save()
    prevPortfolio = Portfolio.objects.filter(sno=prevSno).first()
    prevPortfolio.save()

    params = {'portfolio': portfolio, 'nextPortfolio': nextPortfolio, 'prevPortfolio': prevPortfolio}
    return render(request, 'home/dispPortfolio.html', params)

def handleSignup(request):
    # GMAIL_ID = ''
    # GMAIL_PSWD = ''

    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        orgName = request.POST['orgName']

        # Check for errorneous inputs
        if len(username) >= 10:
            messages.error(request, 'Username must be under 10 characters.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        if not username.isalnum():           # It should be alpha numeric
            messages.error(request, 'Username should only contain letters and numbers.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        if User.objects.filter(username=username).exists():
            messages.error(request, 'The username is already taken by someone else! Please try another one.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        # Create the User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = name
        myuser.last_name = ''
        myuser.orgName = orgName
        myuser.save()

        send_mail("Someone Signed Up on harmonycreativestudio.in", f"Name: {name}\nusername: {username}\nPhone No.: {phone}\nEmailID: {email}\nOrganisation: {orgName}", 'hcstudio14@gmail.com', ['info@harmonycreativestudio.in'], fail_silently=False)

        user = authenticate(username=username, password=pass1)
        login(request, user)
        messages.success(request, 'Your HarmonyCreativeStudio account has been successfully created and logged in successfully!')

        return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        return HttpResponse('Request Not Found', status=404)

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginUsername']
        loginpassword = request.POST['pass']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        else:
            messages.error(request, 'Invalid Credentials, Please try Again.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

    else:
        return HttpResponse('Request Not Found', status=404)

def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def deleteAccount(request):
    request.user.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def updateAccount(request):
    if request.method == 'POST':
        nameUpdate = request.POST['nameUpdate']
        usernameUpdate = request.POST['usernameUpdate']
        emailUpdate = request.POST['emailUpdate']
        isError = False

        if len(usernameUpdate) >= 10:
            messages.error(request, 'Username must be under 10 characters.')
            isError = True
        if not usernameUpdate.isalnum():
            messages.error(request, 'Username should only contain letters and numbers.')
            isError = True
        if User.objects.filter(username=usernameUpdate).exists():
            messages.error(request, 'The username is already taken by someone else! Please try another one.')
            isError = True

        if not isError:
            user = User.objects.get(username = request.user.username)
            user.first_name = nameUpdate
            user.last_name = ''
            user.username = usernameUpdate
            user.email = emailUpdate
            user.save()

        return redirect(request.META.get('HTTP_REFERER', 'myAccount'))

def myAccount(request):
    if request.user.is_authenticated:
        return render(request, 'home/account/myAccount.html', {'footerInAir':True})
    else:
        return HttpResponse("Access Denied", status=401)

def page_not_found_view(request, exception):
    return render(request, 'home/custom_errors/page_not_found.html', {'footerInAir':True})

def internal_server_error_view(request):
    return render(request, 'home/custom_errors/internal_server_error.html')

def unauthorized_view(request):
    return render(request, 'home/custom_errors/unauthorized.html')

def broadCastMsg(request):
    if request.user.is_superuser:
        if request.method=='POST':
            msg = request.POST['msg']
            activeDays = request.POST['activeDays']
            broadCastMessage = broadcasted_message(msg=msg, activeDays=activeDays)
            broadCastMessage.save()
        return render(request, 'home/broadCastMsg.html', {'footerInAir':True})
    else:
        return HttpResponse("Access Denied", status=401)