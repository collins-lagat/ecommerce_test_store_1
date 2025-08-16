from products.models import Category


def load_categories(request):
    categories = Category.objects.all()

    lookup = {
        category.id: {"id": category.id, "name": category.name, "children": []}
        for category in categories
    }
    root_categories = []

    for category in categories:
        if category.parent_id:
            lookup[category.parent_id]["children"].append(category)
        else:
            root_categories.append(lookup[category.id])

    return {"categories": root_categories}
