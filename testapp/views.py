from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'testapp/index.html')


def userlogin(request):

    return render(request, 'homepage/signin.html', context={'login-status' : 0})
    #return render(request, 'homepage/signin.html', context={'login-status' : 0})

def chkimgs(request):
    # img1 = request.POST['img1']
    # img2 = request.POST['img2']


    return render(request, 'testapp/index.html')