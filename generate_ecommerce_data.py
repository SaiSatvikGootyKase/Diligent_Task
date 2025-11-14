import csv
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)

# Generate dates
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)

# Sample data pools
first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor",
    "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Sanchez",
    "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams"
]

domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "company.com", "email.com"]

categories = [
    "Electronics", "Clothing", "Home & Garden", "Books", 
    "Sports & Outdoors", "Beauty & Personal Care", "Toys & Games",
    "Automotive", "Health & Wellness", "Food & Beverages"
]

product_names_by_category = {
    "Electronics": ["Smartphone", "Laptop", "Tablet", "Headphones", "Smart Watch", "Camera", "Speaker", "Monitor", "Keyboard", "Mouse"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers", "Hat", "Sweater", "Shorts", "Coat", "Boots"],
    "Home & Garden": ["Lamp", "Plant Pot", "Garden Tool", "Cushion", "Curtain", "Rug", "Vase", "Frame", "Mirror", "Shelf"],
    "Books": ["Novel", "Biography", "Cookbook", "Textbook", "Comic", "Dictionary", "Atlas", "Guide", "Manual", "Journal"],
    "Sports & Outdoors": ["Basketball", "Tennis Racket", "Yoga Mat", "Dumbbells", "Bicycle", "Tent", "Backpack", "Running Shoes", "Helmet", "Water Bottle"],
    "Beauty & Personal Care": ["Shampoo", "Face Cream", "Perfume", "Lipstick", "Sunscreen", "Toothbrush", "Hair Dryer", "Nail Polish", "Soap", "Lotion"],
    "Toys & Games": ["Board Game", "Action Figure", "Puzzle", "Doll", "RC Car", "LEGO Set", "Card Game", "Building Blocks", "Stuffed Animal", "Art Set"],
    "Automotive": ["Car Battery", "Tire", "Oil Filter", "Brake Pad", "Air Freshener", "Car Mat", "Phone Mount", "Dash Cam", "Jump Starter", "Tool Kit"],
    "Health & Wellness": ["Vitamins", "Protein Powder", "Yoga Block", "Massage Ball", "Foam Roller", "Resistance Band", "Scale", "Thermometer", "First Aid Kit", "Sleep Mask"],
    "Food & Beverages": ["Coffee Beans", "Tea Set", "Chocolate Box", "Snack Mix", "Energy Bar", "Juice", "Honey", "Olive Oil", "Spice Set", "Wine"]
}

review_texts = [
    "Great product! Highly recommend.",
    "Good quality for the price.",
    "Not what I expected, but okay.",
    "Excellent value and fast shipping.",
    "Poor quality, disappointed.",
    "Amazing product, exceeded expectations!",
    "Decent product, nothing special.",
    "Love it! Will buy again.",
    "Average quality, could be better.",
    "Outstanding product, very satisfied!",
    "Not worth the money.",
    "Perfect for my needs.",
    "Good but has some flaws.",
    "Best purchase I've made!",
    "Could be improved.",
    "Very happy with this purchase.",
    "Disappointing quality.",
    "Great features and design.",
    "Works as advertised.",
    "Not recommended."
]

def random_date(start, end):
    """Generate a random date between start and end."""
    time_between = end - start
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start + timedelta(days=random_days)

def generate_email(name):
    """Generate a realistic email from a name."""
    first, last = name.split()[0].lower(), name.split()[-1].lower()
    domain = random.choice(domains)
    return f"{first}.{last}@{domain}"

# Generate Customers (30 customers)
customers = []
customer_ids = []
for i in range(1, 31):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    signup_date = random_date(start_date, end_date - timedelta(days=365))
    customers.append({
        'customer_id': i,
        'name': name,
        'email': generate_email(name),
        'signup_date': signup_date.strftime('%Y-%m-%d')
    })
    customer_ids.append(i)

# Generate Products (35 products)
products = []
product_ids = []
for i in range(1, 36):
    category = random.choice(categories)
    product_base = random.choice(product_names_by_category[category])
    product_name = f"{product_base} {random.choice(['Pro', 'Premium', 'Deluxe', 'Standard', 'Elite', 'Basic', 'Plus', 'Max'])}"
    price = round(random.uniform(9.99, 999.99), 2)
    products.append({
        'product_id': i,
        'name': product_name,
        'category': category,
        'price': price
    })
    product_ids.append(i)

# Generate Orders (25 orders)
orders = []
order_ids = []
customer_signup_dates = {c['customer_id']: datetime.strptime(c['signup_date'], '%Y-%m-%d') for c in customers}

for i in range(1, 26):
    customer_id = random.choice(customer_ids)
    signup_date = customer_signup_dates[customer_id]
    # Order date must be after signup date
    order_date = random_date(signup_date + timedelta(days=1), end_date)
    total_amount = round(random.uniform(20.00, 1500.00), 2)
    orders.append({
        'order_id': i,
        'customer_id': customer_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'total_amount': total_amount
    })
    order_ids.append(i)

# Generate Order Items (40 items)
order_items = []
order_item_id = 1
order_product_map = {}  # Track products per order

for order_id in order_ids:
    # Each order has 1-4 items
    num_items = random.randint(1, 4)
    order_products = random.sample(product_ids, min(num_items, len(product_ids)))
    
    for product_id in order_products:
        quantity = random.randint(1, 5)
        # Get product price
        product_price = next(p['price'] for p in products if p['product_id'] == product_id)
        price = round(product_price * quantity, 2)
        
        order_items.append({
            'order_item_id': order_item_id,
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'price': price
        })
        order_item_id += 1
        order_product_map.setdefault(order_id, []).append(product_id)

# Generate Reviews (30 reviews)
reviews = []
review_id = 1

# Only review products that have been ordered
reviewed_combinations = set()
for _ in range(30):
    # Pick a customer who has made an order
    customer_id = random.choice([o['customer_id'] for o in orders])
    
    # Pick a product that was ordered (by any customer)
    product_id = random.choice(product_ids)
    
    # Avoid duplicate reviews
    combo = (product_id, customer_id)
    if combo in reviewed_combinations:
        continue
    reviewed_combinations.add(combo)
    
    # Review date should be after signup
    signup_date = customer_signup_dates[customer_id]
    review_date = random_date(signup_date + timedelta(days=7), end_date)
    
    rating = random.randint(1, 5)
    review_text = random.choice(review_texts)
    
    reviews.append({
        'review_id': review_id,
        'product_id': product_id,
        'customer_id': customer_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date.strftime('%Y-%m-%d')
    })
    review_id += 1

# Write CSV files
def write_csv(filename, data, fieldnames):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

write_csv('customers.csv', customers, ['customer_id', 'name', 'email', 'signup_date'])
write_csv('products.csv', products, ['product_id', 'name', 'category', 'price'])
write_csv('orders.csv', orders, ['order_id', 'customer_id', 'order_date', 'total_amount'])
write_csv('order_items.csv', order_items, ['order_item_id', 'order_id', 'product_id', 'quantity', 'price'])
write_csv('reviews.csv', reviews, ['review_id', 'product_id', 'customer_id', 'rating', 'review_text', 'review_date'])

print("Generated CSV files:")
print(f"- customers.csv: {len(customers)} rows")
print(f"- products.csv: {len(products)} rows")
print(f"- orders.csv: {len(orders)} rows")
print(f"- order_items.csv: {len(order_items)} rows")
print(f"- reviews.csv: {len(reviews)} rows")
