from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q #
from django.views.decorators.http import require_http_methods # telling what crud functionality a particular view method could have


from .forms import ContactForm

# Create your views here.
@login_required # authenticated user comes from 'request.user'
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {'contacts':contacts, 'form':ContactForm()}
    return render(request, 'contacts.html', context)

@login_required
def search_contacts(request):
    import time
    time.sleep(2)
    query = request.GET.get('search','') # looking for a query named 'search' same name as input

    # use the query to filter contacts by name or email
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query) # looking for name, email icontains is for looking up
    )

    return render(request, 'partials/contact-list.html', {'contacts' : contacts})

@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form = ContactForm(request.POST, request.FILES, initial={'user':request.user})
    if form.is_valid():
        contact = form.save(commit=False) #initially we don't save to db because we should assign user first
        contact.user = request.user
        contact.save()
        # return partial containing a new row for our user
        # that we can add to the table
        context = {'contact':contact}
        response =  render(request, 'partials/contact-row.html',context)
        response["HX-Trigger"] = 'success' # send HX-Trigger = success as a header
        print("FILES:", request.FILES)
        return response
    else:
        response =  render(request, 'partials/add-contact-modal.html',{'form':form})
        response['HX-Retarget'] = '#contact_modal' 
        # HX-Retarget is an HTMX response header that allows the server 
        # to specify a CSS selector to redirect 
        # the target of an AJAX update to a 
        # different element on the page. 
        # It is used to override the default client-side hx-target,
        # commonly for updating error messages or swapping different content based on server-side logic.
        response["HX-Reswap"] = 'outerHTML'
        response["HX-Trigger-After-Settle"] = 'fail'
        #to use the modal still opens if the form is invalid
        return response

