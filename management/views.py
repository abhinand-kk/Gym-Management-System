from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.db.models import Q
from .models import ClientProfile, Membership
from .forms import ClientProfileForm, MembershipForm
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from .forms import SimpleUserCreationForm
from django.contrib.auth import login
from django.contrib import messages

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and not getattr(self.request.user, 'is_staff', False)

# ----- ROOT REDIRECT -----
def root_redirect(request):
    if not request.user.is_authenticated:
        return redirect('plans') # Show plans to logged out users
    if getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_superuser', False):
        return redirect('admin_dashboard')
    return redirect('client_dashboard')

# ----- PUBLIC & USER MODULE -----
class PlansView(TemplateView):
    template_name = 'management/plans.html'

class SignUpView(CreateView):
    form_class = SimpleUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        # Auto-login after registration
        login(self.request, self.object)
        return redirect('plans')

class ChooseMembershipView(LoginRequiredMixin, CreateView):
    model = ClientProfile
    form_class = ClientProfileForm
    template_name = 'management/choose_membership.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan = self.request.GET.get('plan', 'Monthly')
        context['plan'] = plan
        if plan == 'Monthly':
            context['fee'] = 50.00
        elif plan == 'Quarterly':
            context['fee'] = 130.00
        elif plan == 'Yearly':
            context['fee'] = 450.00
        return context

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.user.first_name = form.cleaned_data.get('first_name')
        profile.user.last_name = form.cleaned_data.get('last_name')
        profile.user.email = form.cleaned_data.get('email')
        profile.user.save()
        profile.save()
        
        # Create Membership
        plan_type = self.request.GET.get('plan', 'Monthly')
        fee = 50.00
        months = 1
        if plan_type == 'Quarterly':
            fee = 130.00
            months = 3
        elif plan_type == 'Yearly':
            fee = 450.00
            months = 12
            
        start_date = date.today()
        end_date = start_date + relativedelta(months=months)
        
        Membership.objects.create(
            user=self.request.user,
            membership_type=plan_type,
            registration_fee=fee,
            start_date=start_date,
            end_date=end_date,
            payment_status='Pending'
        )
        messages.success(self.request, "Membership created successfully!")
        return redirect('client_dashboard')

class ClientDashboardView(ClientRequiredMixin, TemplateView):
    template_name = 'management/client_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        membership = Membership.objects.filter(user=self.request.user).order_by('-end_date').first()
        context['membership'] = membership
        if membership:
            context['is_active'] = membership.end_date >= today
        try:
            context['profile'] = self.request.user.client_profile
        except ClientProfile.DoesNotExist:
            context['profile'] = None
        return context

# ----- ADMIN MODULE -----
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'management/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        context['total_clients'] = ClientProfile.objects.count()
        all_memberships = Membership.objects.all()
        context['active_memberships'] = all_memberships.filter(end_date__gte=today).count()
        context['expired_memberships'] = all_memberships.filter(end_date__lt=today).count()
        context['recent_registrations'] = all_memberships.order_by('-start_date')[:5]
        return context

class AdminClientListView(AdminRequiredMixin, ListView):
    model = ClientProfile
    template_name = 'management/admin_client_list.html'
    context_object_name = 'clients'
    
    def get_queryset(self):
        queryset = ClientProfile.objects.all()
        query = self.request.GET.get('q')
        m_type = self.request.GET.get('type')
        status = self.request.GET.get('status')
        
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) | 
                Q(user__last_name__icontains=query) | 
                Q(phone_number__icontains=query)
            )
        if m_type:
            queryset = queryset.filter(user__memberships__membership_type=m_type)
        if status:
            today = date.today()
            if status == 'Active':
                queryset = queryset.filter(user__memberships__end_date__gte=today)
            elif status == 'Expired':
                queryset = queryset.filter(user__memberships__end_date__lt=today)
                
        return queryset.distinct()

class AdminMembershipCreateView(AdminRequiredMixin, CreateView):
    model = Membership
    form_class = MembershipForm
    template_name = 'management/membership_form.html'
    success_url = reverse_lazy('admin_client_list')

class AdminMembershipUpdateView(AdminRequiredMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    template_name = 'management/membership_form.html'
    success_url = reverse_lazy('admin_client_list')

class AdminMembershipDeleteView(AdminRequiredMixin, DeleteView):
    model = Membership
    template_name = 'management/membership_confirm_delete.html'
    success_url = reverse_lazy('admin_client_list')

class AdminClientDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'management/client_confirm_delete.html'
    success_url = reverse_lazy('admin_client_list')

