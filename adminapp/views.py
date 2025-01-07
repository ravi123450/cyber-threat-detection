from django.shortcuts import render,redirect
from userapp.models import User
from adminapp.models import Dataset
import pandas as pd
from django.contrib import messages
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import math
from adminapp.models import Dataset

# Create your views here.


def index(request):
    t_users = User.objects.all()
    a_users = User.objects.filter(status="Accepted")
    p_users = User.objects.filter(status="Verified")
    context ={
        't_users':len(t_users),
        'a_users':len(a_users),
        'p_users':len(p_users),

    }
    return render(request,'admin/index.html', context)


def all_users(request):
    user = User.objects.filter(status = "Accepted")
    context = {
        'user':user,
    }
    return render(request,'admin/all-users.html',context)



def attacks_analysis(request):
    return render(request, 'admin/attacks-analysis.html', {})







def upload_dataset(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file') 
        if csv_file:
            Dataset.objects.all().delete()
            dataset = Dataset(title=csv_file.name, file=csv_file)
            dataset.save()
            return redirect('view_dataset')
    return render(request,'admin/upload-dataset.html')



def view_dataset(request):
    datasets = Dataset.objects.all()
    data_list = []
    
    for dataset in datasets:
        df = pd.read_csv(dataset.file)
        df = df.head(1000)
        data = df.to_html(index=False)
        data_list.append({
            'title': dataset.title,
            'data': data
        })
        dataset.save()
    return render(request,'admin/view-dataset.html',{'data_list': data_list})


def pending_users(request):
    user = User.objects.filter(status = "Verified")
    print(user)
    context = {
        'user':user,
    }
    return render(request,'admin/pending-users.html',context)


def alg1(request):
    return render(request, 'admin/algorithm-one.html',{})



def alg2(request):
    return render(request,'admin/algorithm-two.html',{})



def alg3(request):
    return render(request, 'admin/algorithm-three.html', {})




def alg4(request):
    return render(request,'admin/algorithm-four.html',{})



def alg5(request):
    return render(request, 'admin/algorithm-five.html', {})







def graph_analysis(request):
    return render(request,'admin/graph-analasis.html',{})





def accept_user(request,user_id):
    user = User.objects.get(user_id=user_id)
    user.status = 'Accepted'
    user.save()
    return redirect('pending_users')

def reject_user(request,user_id):
    user = User.objects.get(user_id = user_id)
    user.delete()
    return redirect('pending_users')


def delete_user(request,user_id):
    user = User.objects.get(user_id = user_id)
    user.delete()
    return redirect('all_users')

