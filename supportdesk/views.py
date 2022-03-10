# Django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# App
from .models import Request
from .forms import RequestForm
from .decorators import customers_only, agents_only

class PlaceholderHome(TemplateView):
    template_name = "supportdesk/placeholder.html"
    
class RequestList( ListView):
    model = Request
    context_object_name = 'requests'
    template_name='supportdesk/requests.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['requests_count'] = Request.objects.filter(created_by=self.request.user).count() 
        context['users'] =  User.objects.filter(is_staff=True)               
        
        return context  
    
    def get_queryset(self):   
        if self.request.user.is_staff:
            # Ensure agents to see only Requests assigned to them     
            return Request.objects.filter(user_assigned_to=self.request.user)
        else:
            # Ensure customers see only their requests
            return Request.objects.filter(created_by=self.request.user)

@method_decorator([customers_only], name='dispatch')
class RequestCreateView(LoginRequiredMixin, CreateView):    
    form_class = RequestForm
    template_name = "supportdesk/new_request.html"
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.created_by = self.request.user
        form.instance.user_assigned_to = User.objects.filter(is_staff=True).first()
        self.object = form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['requests_count'] = Request.objects.filter(created_by=self.request.user).count()     
        
        return context  

@method_decorator([agents_only], name='dispatch')
class RequestDetailView(DetailView):
    model = Request
    template_name="supportdesk/request_detail.html"
    context_object_name = 'request'
  
@login_required 
def mark_completed(request, pk):
    # This view marks a Request as completed if it is not completed. 
    # If it is already marked as completed, it marks it not as completed
    data = dict()
    try:        
        request_instance = Request.objects.get(pk=pk)
        if request_instance.is_completed:            
            pass
        else:
            # Mark as completed
            request_instance.is_completed = True
            data['response'] = 'completed'
        request_instance.save()        
    except Request.DoesNotExist:
        data['response'] = 'error'
        
    return JsonResponse(data)   
    
def reassign_agent(request, requestID, agentID):    
    # Reassign the task to another agent
    
    try:        
        request_instance = Request.objects.get(pk=requestID)
        request_instance.user_assigned_to = User.objects.get(pk=agentID)
        request_instance.save()       
    except Request.DoesNotExist:
        pass
    return redirect('request_list')
    
