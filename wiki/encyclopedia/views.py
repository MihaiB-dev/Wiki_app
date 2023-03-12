from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
import random
from . import util
# https://shell.cloud.google.com/?pli=1&show=ide&environment_deployment=ide
class CreateNewPageForm(forms.Form):

    title=forms.CharField(label="Title")
    content=forms.CharField(widget= forms.Textarea(attrs={'rows':4, 'cols':3}), label="Content")

class EditPageForm(forms.Form):
    content=forms.CharField(widget= forms.Textarea, label="content")


def index(request):
    if request.method == "POST":
        search = request.POST['q']
        return Search(request, search,type = 1)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def Search(request, title,type = 0):
    if title.lower() in [element.lower() for element in util.list_entries()]:
            return render(request, "encyclopedia/elements.html",{
        "title" : title,
        "elements" : util.get_entry(title)
    })
    elif type == 1: #where I'm searching and Is not what I want
        results = []
        for element in util.list_entries():
             if element.lower().find(title) != -1:
                  results.append(element.lower())
                  
        return render(request, "encyclopedia/search.html",{
             "search": title,
             "results":results
        })
    else: #where the user types in the link wrong
        return render(request,f"encyclopedia/error.html",{
            "error_name": "Your requested page was not found",
        })

def Create(request):
    if request.method == "POST":
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title= form.cleaned_data["title"]
            content= form.cleaned_data["content"]  
            if title.lower() in title.lower() in [element.lower() for element in util.list_entries()]:
                messages.info(request,'The entry already exists with this title')
                return render(request, "encyclopedia/new_page.html",{
                "form":CreateNewPageForm(request.POST),
                }) 
            else:
                util.save_entry(title,content)
                messages.info(request,'successfully added your new page')
                return HttpResponseRedirect(reverse("index"))
    else:    
        return render(request, "encyclopedia/new_page.html",{
                "form":CreateNewPageForm()
        }) 
    
def Edit(request,title):
    Edit_form = EditPageForm({'content':util.get_entry(title)})

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            changed_content=form.cleaned_data["content"] #user new input
            util.save_entry(title,changed_content) #change the data

            messages.info(request,'changes successfully saved')
            return HttpResponseRedirect(reverse("search",args=[title])) 

    return render(request, "encyclopedia/edit_page.html",{
        "title" : title,
        "form":Edit_form
    })

def Random_page(request):
    random_page = random.choice(util.list_entries())
    return Search(request, random_page)