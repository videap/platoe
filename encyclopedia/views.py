from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django import forms
from django.urls import reverse
from . import search
from random import randrange
import markdown2
from . import util

class NewSearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "search", "placeholder": "Search Encyclopedia"}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title ")
    content = forms.CharField(label="Content ", widget=forms.Textarea, )


def index(request):
    if request.method =="POST":
        data_form = NewSearchForm(request.POST)
        if data_form.is_valid():
            search_value = data_form.cleaned_data["q"]
            return HttpResponseRedirect(reverse('show_entry', kwargs={'title': search_value}))
        else:
            return HttpResponseServerError('<h1>Server Error.</h1>')
    
    else:
        entries = util.list_entries()      
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "search_form": NewSearchForm(),
            "block_title": "Encyclopedia",
            "page_title": "All Pages",
            "random": entries[0]
        })

#view of a content page
def show_entry(request, title):

    entry_content = util.get_entry(title)

    #if there is no page with the title requested
    if entry_content is None:
        #search substrings
        substrings = search.search_string(title, util.list_entries())
        if substrings == []:
            return HttpResponseNotFound("<h1>Page Not Found.</h1>")
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": substrings,
                "search_form": NewSearchForm(),
                "block_title": "Encyclopedia",
                "page_title": "Are you looking for one of these pages?"
            })
    #if there is a page with the title requested, show page      
    else:
        return render(request, "encyclopedia/entry_page.html", {
            "title": title,
            "entry_content": markdown2.markdown(entry_content),
            "search_form": NewSearchForm()
        })

def new_page(request):
    
    #if it is a request to submit a new page 
    if request.method == "POST":
        data_form = NewPageForm(request.POST)

        #to valid and save data to cleaned_data
        if data_form.is_valid():
            
            #if there is no entry with the same title, save new page
            if util.get_entry(data_form.cleaned_data["title"].capitalize()) != None:
                return HttpResponseServerError("<h1>The page already exists.")
            else: 
                new_title = data_form.cleaned_data["title"].capitalize()
                util.save_entry(new_title, data_form.cleaned_data["content"])
                return HttpResponseRedirect(reverse('show_entry', kwargs={'title': new_title}))

        else:
            return HttpResponseServerError("<h1>Server Error.")    

    return render(request, "encyclopedia/new_page.html", {
        "newpage_form": NewPageForm,
        "block_title": "New Page",
        "page_title": "Create a New Page:",
        "search_form": NewSearchForm()
    })

def edit_page(request, edit_entry):

    #check if there is a matching entry to be edited

    if util.get_entry(edit_entry) != None:

        if request.method == "POST":
            EditForm = NewPageForm(request.POST)
            if EditForm.is_valid():
                util.save_entry(EditForm.cleaned_data["title"], EditForm.cleaned_data["content"])
                return HttpResponseRedirect(reverse('show_entry', kwargs={'title': EditForm.cleaned_data["title"]}))

        else:
            EditForm = NewPageForm({"title": edit_entry, "content": util.get_entry(edit_entry)})

            return render(request, "encyclopedia/edit_page.html", {
                "newpage_form": EditForm,
                "block_title": edit_entry,
                "page_title": "Edit",
                "search_form": NewSearchForm()
            })
    else:
        return HttpResponseRedirect(reverse('show_entry', kwargs={'title': edit_entry}))

def random(request):
    entries = util.list_entries()
    random_int = randrange(0,len(entries))
    
    return HttpResponseRedirect(reverse('show_entry', kwargs={'title': entries[random_int]}))
