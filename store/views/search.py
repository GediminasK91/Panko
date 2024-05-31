from django.shortcuts import render
from store.models.product import Product

def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'search_results.html', {'query': query, 'results': results})
