from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required

from .models import LostItem, ClaimVerification
from .forms import LostItemForm, ClaimForm, RegisterForm


# --------- AUTH ---------
def user_logout(request):
    logout(request)
    return redirect('home')   # or 'login' if you prefer


# --------- PUBLIC HOME ---------
def home(request):
    # 1) Read filters from URL
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all')
    # building_filter = request.GET.get('building', 'all')

    # 2) Start with all items
    items = LostItem.objects.all()

    # 3) Apply search filter
    if search_query:
        items = items.filter(
            Q(item_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # 4) Apply status filter
    if status_filter != 'all':
        # if your DB uses "not_found" instead of "lost"
        if status_filter == 'lost':
            items = items.filter(status='not_found')
        else:
            items = items.filter(status=status_filter)

    # 5) Building filter
    # if building_filter != 'all':
    #     items = items.filter(location_lost__icontains=building_filter)

    context = {
        'items': items,
        'search_query': search_query,
        'status_filter': status_filter,
        # 'building_filter': building_filter,
    }
    return render(request, 'lostandfound/home.html', context)


# --------- REPORT ITEM ---------
@login_required
def report_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            # make sure this matches your model field
            item.reported_by = request.user  

            # defaults
            if not item.status:
                item.status = 'not_found'
            if not item.college:
                item.college = 'CCIS'

            item.save()
            return redirect('home')
    else:
        form = LostItemForm()

    return render(request, 'lostandfound/report_item.html', {'form': form})


# --------- ITEM DETAIL + CLAIM ---------
@login_required
def item_detail(request, pk):
    item = get_object_or_404(LostItem, pk=pk)

    if request.method == "POST":
        form = ClaimForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data["answer"].strip().lower()
            correct_answer = (item.security_answer or "").strip().lower()

            if correct_answer and user_answer == correct_answer:
                # owner verified
                item.status = "found"   # or "claimed" if you prefer
                item.save()

                messages.success(
                    request,
                    "Correct answer! Please visit the building security office to pick up your item.",
                )
                return redirect("item_detail", pk=item.pk)
            else:
                messages.error(request, "Incorrect answer. Please try again.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ClaimForm()

    return render(
        request,
        "item_detail.html",
        {
            "item": item,
            "form": form,
        },
    )


# --------- MY REPORTS ---------
@login_required
def my_reports(request):
    # All items reported by this user
    my_items = LostItem.objects.filter(reported_by=request.user).order_by('-created_at')

    active_items = my_items.filter(status='not_found')
    found_items = my_items.filter(status='found')

    context = {
        'my_items': my_items,
        'active_items': active_items,
        'found_items': found_items,
    }
    return render(request, 'lostandfound/my_reports.html', context)


# --------- REGISTER ---------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


# --------- ADMIN DASHBOARD ---------
@staff_member_required   # only staff / superuser can access
def admin_dashboard(request):
    reports = LostItem.objects.all().order_by('-date_lost')  # or '-id' if you prefer

    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    building = request.GET.get('building', '').strip()

    if q:
        reports = reports.filter(
            Q(item_name__icontains=q) |
            Q(description__icontains=q) |
            Q(contact_name__icontains=q)
        )

    if status and status != 'all':
        # map UI "lost" to DB "not_found" if needed
        if status == 'lost':
            reports = reports.filter(status='not_found')
        else:
            reports = reports.filter(status=status)

    if building and building != 'all':
        reports = reports.filter(location_lost__icontains=building)

    today = timezone.now().date()

    context = {
        "reports": reports,
        "total_reports": LostItem.objects.count(),
        "lost_reports": LostItem.objects.filter(status="not_found").count(),
        "found_reports": LostItem.objects.filter(status="found").count(),
        "claimed_reports": LostItem.objects.filter(status="claimed").count(),
        "today_reports": LostItem.objects.filter(date_lost=today).count(),
    }
    return render(request, "admin_dashboard.html", context)

@staff_member_required
def delete_item(request, pk):
    # Get the item or show a 404 error if not found
    item = get_object_or_404(LostItem, pk=pk)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item has been deleted successfully.')
        return redirect('admin_dashboard')
    
    # If someone tries to access via GET, just redirect them back
    return redirect('admin_dashboard')
