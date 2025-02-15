from ads.models import Category, Ad

def categories(request):
    """Контекстный процессор, возвращающий категории и количество объявлений."""
    categories = Category.objects.all()
    category_counts = {category.name: Ad.objects.filter(category=category).count() for category in categories}
    return {'categories': categories, 'category_counts': category_counts}