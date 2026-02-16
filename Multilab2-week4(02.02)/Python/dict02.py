
from collections import defaultdict

def categorize_products(products):
    result = defaultdict(lambda: {'items': [], 'prices': []})
    print(result)
    
    for p in products:
        result[p['category']]['items'].append(p['name'])
        result[p['category']]['prices'].append(p['price'])
    
    for cat in result:
        prices = result[cat]['prices']
        result[cat]['min'] = min(prices)
        result[cat]['max'] = max(prices)
        result[cat]['avg'] = sum(prices) // len(prices)
        del result[cat]['prices']
    
    return dict(result)

# Использование
products = [
    {'name': 'футболка', 'category': 'одежда', 'price': 1500},
    {'name': 'джинсы', 'category': 'одежда', 'price': 3500},
    {'name': 'ноутбук', 'category': 'электроника', 'price': 55000},
    {'name': 'мышка', 'category': 'электроника', 'price': 1500}
]
result = categorize_products(products)
print(result)