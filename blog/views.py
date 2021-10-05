from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
from math import ceil
from django.db.models import Q
# from time import time

def blogHome(request):
    posts_per_page = 5
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    allPosts = Post.objects.all()
    length = len(allPosts)
    allPosts = Post.objects.order_by('-timeStamp')
    allPosts =allPosts[(page-1)*posts_per_page: page*posts_per_page]

    if page>1:
        previousPage = page-1
    else:
        previousPage = None

    if page<ceil(length/posts_per_page):
        nextPage = page+1
    else:
        nextPage = None

    isBlog = True
    newest = True
    if(length>0):
        footerInAir = False
    else:
        footerInAir = True

    allPossiblePosts = Post.objects.all()
    possibleQueries = []
    for possiblePost in allPossiblePosts:
        possibleQueries.append(possiblePost.title)
        keywords = possiblePost.keywords
        for keyword in keywords.split(", "):
            possibleQueries.append(keyword)

    context = {'allPosts': allPosts, 'prev': previousPage, 'nxt': nextPage, 'status': 'newestFirst', 'isBlog': isBlog, 'newest': newest, 'footerInAir': footerInAir, 'possibleQueries': possibleQueries}
    return render(request, 'blog/index.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.save()

    # Comments and Replies Logic
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)

    isBlog = True

    # Getting no. of unique views
    def getIP(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = getIP(request)
    uniqueVisitors = post.uniqueVisitorIPs
    if(ip in uniqueVisitors):
        pass
    else:
        post.uniqueVisitorIPs = uniqueVisitors + " " + ip
        post.save()
    post.views = len(uniqueVisitors.split())
    post.save()

    params = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': repDict, 'isBlog': isBlog}
    return render(request, 'blog/blogPost.html', params)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')

        if parentSno == "":
            comment = BlogComment(comments = comment, user = user, post = post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comments = comment, user = user, post = post , parent = parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")

def oldestFirst(request):
    posts_per_page = 5
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    
    allPosts = Post.objects.all()
    length = len(allPosts)
    allPosts = Post.objects.order_by('timeStamp')
    allPosts = allPosts[(page-1)*posts_per_page: page*posts_per_page]

    if page>1:
        previousPage = page-1
    else:
        previousPage = None

    if page<ceil(length/posts_per_page):
        nextPage = page+1
    else:
        nextPage = None

    isBlog = True
    newest = False
    if(length>0):
        footerInAir = False
    else:
        footerInAir = True

    allPossiblePosts = Post.objects.all()
    possibleQueries = []
    for possiblePost in allPossiblePosts:
        possibleQueries.append(possiblePost.title)
        keywords = possiblePost.keywords
        for keyword in keywords.split(", "):
            possibleQueries.append(keyword)

    context = {'allPosts': allPosts, 'status': 'oldestFirst', 'prev': previousPage, 'nxt': nextPage, 'isBlog': isBlog, 'newest': newest, 'footerInAir': footerInAir, 'possibleQueries': possibleQueries}
    return render(request, 'blog/index.html', context)

def mostPopular(request):
    posts_per_page = 5
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    
    allPosts = Post.objects.all()
    length = len(allPosts)
    allPosts = Post.objects.order_by('-views')
    allPosts = allPosts[(page-1)*posts_per_page: page*posts_per_page]

    if page>1:
        previousPage = page-1
    else:
        previousPage = None

    if page<ceil(length/posts_per_page):
        nextPage = page+1
    else:
        nextPage = None

    isBlog = True
    popular = True
    if(length>0):
        footerInAir = False
    else:
        footerInAir = True

    allPossiblePosts = Post.objects.all()
    possibleQueries = []
    for possiblePost in allPossiblePosts:
        possibleQueries.append(possiblePost.title)
        keywords = possiblePost.keywords
        for keyword in keywords.split(", "):
            possibleQueries.append(keyword)

    context = {'allPosts': allPosts, 'status': 'popularFirst', 'prev': previousPage, 'nxt': nextPage, 'isBlog': isBlog, 'popular': popular, 'footerInAir': footerInAir, 'possibleQueries': possibleQueries}
    return render(request, 'blog/index.html', context)

def search(request):
    # startTime = time()

    if(len(Post.objects.all()) == 0):
        return redirect('/blog/')

    query = request.GET['query']
    if len(query) > 100 or len(query) < 3:
        allPosts = Post.objects.none()
        messages.warning(request, 'No Search Results found for your query, Please try the following suggestions!')
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostKeyword = Post.objects.filter(keywords__icontains=query)
        allPosts = (allPostsTitle.union(allPostKeyword)).union(allPostsContent)
        allPosts = allPosts.order_by('-timeStamp')

    # endTime = time()
    # executionTime = endTime - startTime
    # queries = allPosts.length()
    isBlog = True

    allPossiblePosts = Post.objects.all()
    possibleQueries = []
    for possiblePost in allPossiblePosts:
        possibleQueries.append(possiblePost.title)
        keywords = possiblePost.keywords
        for keyword in keywords.split(", "):
            possibleQueries.append(keyword)

    params = {'allPosts': allPosts, 'query': query, 'isBlog': isBlog, 'possibleQueries': possibleQueries}
    return render(request,'blog/search.html', params)
