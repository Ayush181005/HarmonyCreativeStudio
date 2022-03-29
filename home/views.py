from django.shortcuts import render, HttpResponse, redirect
from datetime import date, datetime, timedelta
from home.models import Contact, Testimonial, Portfolio, Client, TeamMember, broadcasted_message
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from decouple import config as envread
import json
import requests

def home(request):
    experience = date.today().year - 2002

    isHome = True

    allPosts = Post.objects.all()
    for post in allPosts:
        if not post.isOld:
            messages.info(request, f'There is a <a class="text-dark" href="/blog/post/{post.slug}">Post - {post.title}</a> uploaded by HarmonyCreativeStudio in last 2 days, to view that go to the <a class="text-dark" href="/blog">Blog Page</a>!')

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

    # giving recaptcha site key to template when GET request
    RECAPTCHA_SITE_KEY = envread('RECAPTCHA_SITE_KEY')
    params.update({'recaptchaSiteKey': RECAPTCHA_SITE_KEY})

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        content = request.POST['content']

        # Google Recaptcha
        siteKey = request.POST['g-recaptcha-response']
        secretKey = envread('RECAPTCHA_SECRET_KEY')
        recaptchaData = {
            'secret': secretKey,
            'response': siteKey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptchaData) # sending POST request to google recaptcha server
        response = json.loads(r.text)
        verify = response["success"]

        if len(name)<2 or len(content)<4:
            messages.error(request, 'The length of name must be 2 characters or content must have atleast 4 characters!')
            isError = True
        elif not verify:
            messages.error(request, 'Please verify that you are not a robot!')
            isError = True
        else:
            contact = Contact(name=name, email=email, subject=subject, content=content)
            contact.save()
            send_mail("Contact Recieved", f"There is a message from {contact.name} through the Contact Us form on harmonycreativestudio.in.\nMailID of Contact: {contact.email}\nSubject: {contact.subject}\nMessage: {contact.content}", 'hcstudio14@gmail.com', ['info@harmonycreativestudio.in'], fail_silently=False)

            messages.success(request, 'Your message has been sent! We will get back to you shortly!')
            isError = False
        messageForContact = True
        params.update({'messageForContact': messageForContact})
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
        user = User.objects.create_user(username, email, pass1)
        user.first_name = name
        user.last_name = ''
        user.orgName = orgName
        user.save()

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
    messages.success(request, 'Your account has been deleted successfully. We are sad to see you go!')
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
        if User.objects.filter(username=usernameUpdate).exists() and len(User.objects.filter(username=usernameUpdate))>1:
            messages.error(request, 'The username is already taken by someone else! Please try another one.')
            isError = True

        if not isError:
            user = User.objects.get(username = request.user.username)
            user.first_name = nameUpdate
            user.last_name = ''
            user.username = usernameUpdate
            user.email = emailUpdate
            user.save()
            messages.info(request, "It may take several seconds to update info...<script>setTimeout(()=>{document.getElementById('nameUpdate').value = '"+user.first_name+"';document.getElementById('usernameUpdate').value = '"+user.username+"';document.getElementById('emailUpdate').value = '"+user.email+"';document.getElementById('userFullName').innerText = '"+user.first_name+"';document.getElementById('userUsername').innerText = '"+user.username+"';document.getElementById('userEmail').innerText = '"+user.email+"';}, 3000);</script>")

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