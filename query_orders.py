import sqlite3
from datetime import datetime, timedelta

def query_customer_orders_with_reviews():
    """
    Query customer order details with product information and review ratings.
    Joins customers, orders, order_items, products, and reviews tables.
    """
    # Connect to database
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Calculate date 90 days ago from today
    # Since our data might be historical, we'll use the most recent order date as reference
    cursor.execute("SELECT MAX(order_date) FROM orders")
    max_order_date = cursor.fetchone()[0]
    
    if max_order_date:
        # Parse the max order date and calculate 90 days before
        max_date = datetime.strptime(max_order_date, '%Y-%m-%d')
        cutoff_date = (max_date - timedelta(days=90)).strftime('%Y-%m-%d')
    else:
        # Fallback to 90 days ago from today
        cutoff_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    # Complex SQL query joining all 5 tables
    query = """
    SELECT 
        c.name AS customer_name,
        o.order_date,
        p.name AS product_name,
        oi.quantity,
        ROUND(p.price, 2) AS unit_price,
        ROUND(COALESCE(AVG(r.rating), 0), 2) AS avg_rating,
        COUNT(r.review_id) AS review_count
    FROM 
        orders o
    INNER JOIN 
        customers c ON o.customer_id = c.customer_id
    INNER JOIN 
        order_items oi ON o.order_id = oi.order_id
    INNER JOIN 
        products p ON oi.product_id = p.product_id
    LEFT JOIN 
        reviews r ON p.product_id = r.product_id
    WHERE 
        o.order_date >= ?
    GROUP BY 
        c.customer_id, o.order_id, o.order_date, p.product_id, p.name, oi.quantity, p.price
    ORDER BY 
        o.order_date DESC, c.name, p.name
    """
    
    # Execute query
    cursor.execute(query, (cutoff_date,))
    results = cursor.fetchall()
    
    # Format results for display
    if results:
        headers = [
            "Customer Name",
            "Order Date",
            "Product Name",
            "Quantity",
            "Unit Price ($)",
            "Avg Rating",
            "Review Count"
        ]
        
        # Format the data
        formatted_results = []
        for row in results:
            formatted_row = [
                row[0],  # customer_name
                row[1],  # order_date
                row[2],  # product_name
                row[3],  # quantity
                f"${row[4]:.2f}",  # unit_price
                f"{row[5]:.1f}" if row[5] > 0 else "N/A",  # avg_rating
                row[6]  # review_count
            ]
            formatted_results.append(formatted_row)
        
        # Print formatted table
        print("=" * 120)
        print("CUSTOMER ORDER DETAILS WITH PRODUCT INFORMATION AND REVIEW RATINGS")
        print(f"Orders from the last 90 days (since {cutoff_date})")
        print("=" * 120)
        print()
        
        # Calculate column widths (with minimum widths)
        min_widths = [15, 12, 25, 10, 15, 12, 13]  # Minimum widths for each column
        col_widths = [max(len(h), min_widths[i]) for i, h in enumerate(headers)]
        for row in formatted_results:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)), min_widths[i])
        
        # Add padding
        col_widths = [w + 2 for w in col_widths]
        
        # Print header with proper alignment
        header_parts = []
        for i, h in enumerate(headers):
            header_parts.append(h.center(col_widths[i]))
        header_row = " | ".join(header_parts)
        print(header_row)
        print("-" * len(header_row))
        
        # Print data rows with proper alignment
        for row in formatted_results:
            data_parts = []
            for i, cell in enumerate(row):
                # Left align text columns, right align numeric columns
                if i in [0, 2]:  # Customer Name, Product Name - left align
                    data_parts.append(str(cell).ljust(col_widths[i]))
                elif i in [3, 4, 5, 6]:  # Numeric columns - right align
                    data_parts.append(str(cell).rjust(col_widths[i]))
                else:  # Date - center align
                    data_parts.append(str(cell).center(col_widths[i]))
            data_row = " | ".join(data_parts)
            print(data_row)
        
        print()
        print(f"Total records: {len(results)}")
    else:
        print("No orders found in the last 90 days.")
    
    # Additional summary statistics
    print("\n" + "=" * 120)
    print("SUMMARY STATISTICS")
    print("=" * 120)
    
    # Total orders in period
    cursor.execute("""
        SELECT COUNT(DISTINCT o.order_id) 
        FROM orders o 
        WHERE o.order_date >= ?
    """, (cutoff_date,))
    total_orders = cursor.fetchone()[0]
    print(f"Total orders in last 90 days: {total_orders}")
    
    # Total customers
    cursor.execute("""
        SELECT COUNT(DISTINCT o.customer_id) 
        FROM orders o 
        WHERE o.order_date >= ?
    """, (cutoff_date,))
    total_customers = cursor.fetchone()[0]
    print(f"Total unique customers: {total_customers}")
    
    # Total products ordered
    cursor.execute("""
        SELECT COUNT(DISTINCT oi.product_id) 
        FROM orders o
        INNER JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date >= ?
    """, (cutoff_date,))
    total_products = cursor.fetchone()[0]
    print(f"Total unique products ordered: {total_products}")
    
    # Products with reviews
    cursor.execute("""
        SELECT COUNT(DISTINCT p.product_id)
        FROM orders o
        INNER JOIN order_items oi ON o.order_id = oi.order_id
        INNER JOIN products p ON oi.product_id = p.product_id
        INNER JOIN reviews r ON p.product_id = r.product_id
        WHERE o.order_date >= ?
    """, (cutoff_date,))
    products_with_reviews = cursor.fetchone()[0]
    print(f"Products with reviews: {products_with_reviews}")
    
    conn.close()

if __name__ == '__main__':
    query_customer_orders_with_reviews()

