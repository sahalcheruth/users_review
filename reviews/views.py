from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework import viewsets, permissions

from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .forms import ReviewForm, RegisterForm
from django.db.models import Q  

# API Views
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_pk'])


# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('/login/')



@login_required
def home_view(request):
    query = request.GET.get('q')  # Get search term from URL
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    
    return render(request, 'reviews/home.html', {
        'products': products,
        'query': query,
    })


# Product Detail + Review View
@login_required
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user_review = Review.objects.filter(product=product, user=request.user).first()
    all_reviews = Review.objects.filter(product=product).select_related('user')
    total_reviews = all_reviews.count()

    if request.method == 'POST':
        if not user_review:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('product_detail', pk=pk)
        else:
            form = None
    else:
        form = ReviewForm() if not user_review else None

    return render(request, 'reviews/product_detail.html', {
        'product': product,
        'form': form,
        'user_review': user_review,
        'average_rating': product.average_rating(),
        'all_reviews': all_reviews,
        'total_reviews': total_reviews,
    })
