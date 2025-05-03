from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, AdForm
from .models import Ad, ExchangeProposal


def index(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль.')
        return render(request, 'forms/index.html')

    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    condition = request.GET.get('condition', '')
    sort_by = request.GET.get('sort', '-created_at')

    offer_id = request.GET.get('offer')
    offer_ad = None
    if offer_id:
        try:
            offer_ad = Ad.objects.get(id=offer_id)
        except Ad.DoesNotExist:
            offer_ad = None

    ads = Ad.objects.exclude(user=request.user)
    user_ads = Ad.objects.filter(user=request.user)

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    ads = ads.order_by(sort_by)
    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'forms/index.html', {
        'ads': page_obj,
        'query': query,
        'category': category,
        'condition': condition,
        'sort_by': sort_by,
        'user_ads': user_ads,
        'offer_ad': offer_ad
    })


@login_required
def my_ads(request):
    sort_by = request.GET.get('sort', '-created_at')
    user_ads = Ad.objects.filter(user=request.user).order_by(sort_by)
    return render(request, 'forms/my_ads.html', {'user_ads': user_ads, 'sort_by': sort_by})


def home_redirect(request):
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'forms/register.html', {'form': form})


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('index')
    else:
        form = AdForm()
    return render(request, 'forms/create_ad.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return redirect('index')


@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('my_ads')
    else:
        form = AdForm(instance=ad)
    return render(request, 'forms/edit_ad.html', {'form': form})


@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user != request.user:
        messages.error(request, 'Вы не можете удалить это объявление.')
    else:
        ad.delete()
        messages.success(request, 'Объявление удалено.')
    return redirect('index')


@login_required
def create_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, id=ad_id)
    user_ads = Ad.objects.filter(user=request.user)
    if request.method == 'POST':
        ad_sender_id = request.POST.get('ad_sender')
        comment = request.POST.get('comment')
        ad_sender = get_object_or_404(Ad, id=ad_sender_id, user=request.user)

        ExchangeProposal.objects.create(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver,
            comment=comment,
            status='PENDING'
        )
        return redirect('index')

    return render(request, 'forms/create_proposal.html', {
        'ad_receiver': ad_receiver,
        'user_ads': user_ads
    })


def all_proposals(request):
    filter_column = request.GET.get('filter_column', '')
    filter_value = request.GET.get('filter_value', '')
    status = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '-created_at')

    proposals = ExchangeProposal.objects.all()

    if request.user.is_authenticated:
        proposals = proposals.filter(ad_receiver__user=request.user)

    if filter_column and filter_value:
        if filter_column == 'sender':
            proposals = proposals.filter(ad_sender__user__username__icontains=filter_value)
        elif filter_column == 'receiver':
            proposals = proposals.filter(ad_receiver__user__username__icontains=filter_value)
        elif filter_column == 'comment':
            proposals = proposals.filter(comment__icontains=filter_value)
        elif filter_column == 'status':
            proposals = proposals.filter(status__icontains=filter_value)

    if status:
        proposals = proposals.filter(status=status)

    proposals = proposals.order_by(sort_by)

    paginator = Paginator(proposals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'forms/all_proposals.html', {
        'page_obj': page_obj,
        'filter_column': filter_column,
        'filter_value': filter_value,
        'status': status,
        'sort_by': sort_by,
        'ads': Ad.objects.all()
    })


def update_proposal_status(request, proposal_id):
    if request.method == 'POST':
        proposal = ExchangeProposal.objects.get(id=proposal_id)

        if proposal.ad_receiver.user == request.user:
            status = request.POST.get('status')
            if status in dict(ExchangeProposal.STATUES_CHOICES).keys():
                proposal.status = status
                proposal.save()

                return redirect('all_proposals')
            else:
                return redirect('all_proposals')
        else:
            return redirect('all_proposals')
    return redirect('all_proposals')
