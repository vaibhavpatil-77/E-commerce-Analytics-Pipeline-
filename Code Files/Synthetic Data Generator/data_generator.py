import pandas as pd
import numpy as np
from faker import Faker
import random
import time
import multiprocessing

# Initialize Faker instance
fake = Faker()

# Function to generate customers
def generate_customers(num_customers):
    customer_ids = np.arange(1, num_customers + 1)
    names = [fake.name() for _ in range(num_customers)]
    emails = [fake.email() for _ in range(num_customers)]
    phone_numbers = [fake.phone_number() for _ in range(num_customers)]
    addresses = [fake.address() for _ in range(num_customers)]
    registration_dates = [fake.date_this_decade() for _ in range(num_customers)]

    customers = pd.DataFrame({
        'customer_id': customer_ids,
        'name': names,
        'email': emails,
        'phone_number': phone_numbers,
        'address': addresses,
        'registration_date': registration_dates
    })
    return customers

# Function to generate products
def generate_products(num_products):
    product_ids = np.arange(1, num_products + 1)
    names = [fake.word().capitalize() for _ in range(num_products)]
    categories = random.choices(['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Toys', 'Sports'], k=num_products)
    prices = np.round(np.random.uniform(10.0, 1000.0, num_products), 2)
    stock_quantities = np.random.randint(1, 1000, num_products)

    products = pd.DataFrame({
        'product_id': product_ids,
        'name': names,
        'category': categories,
        'price': prices,
        'stock_quantity': stock_quantities
    })
    return products

# Function to generate orders (simulating purchases)
def generate_orders(num_orders, customers_df, products_df):
    order_ids = np.arange(1, num_orders + 1)
    customer_ids = random.choices(customers_df['customer_id'], k=num_orders)
    product_ids = random.choices(products_df['product_id'], k=num_orders)
    quantities = np.random.randint(1, 5, num_orders)
    prices = [products_df[products_df['product_id'] == pid]['price'].values[0] for pid in product_ids]
    total_amounts = np.multiply(prices, quantities)
    order_dates = [fake.date_this_year() for _ in range(num_orders)]
    shipping_addresses = [fake.address() for _ in range(num_orders)]
    statuses = random.choices(['Shipped', 'Processing', 'Delivered', 'Cancelled'], k=num_orders)

    orders = pd.DataFrame({
        'order_id': order_ids,
        'customer_id': customer_ids,
        'product_id': product_ids,
        'quantity': quantities,
        'price': prices,
        'total_amount': total_amounts,
        'order_date': order_dates,
        'shipping_address': shipping_addresses,
        'status': statuses
    })
    return orders

# Function to generate transactions
def generate_transactions(num_transactions, orders_df, products_df):
    transaction_ids = np.arange(1, num_transactions + 1)
    order_ids = random.choices(orders_df['order_id'], k=num_transactions)
    product_ids = random.choices(orders_df['product_id'], k=num_transactions)  # Get product_id from orders
    quantities = [orders_df[orders_df['order_id'] == oid]['quantity'].values[0] for oid in order_ids]
    prices = [products_df[products_df['product_id'] == pid]['price'].values[0] for pid in product_ids]
    total_amounts = np.multiply(prices, quantities)
    timestamps = [fake.date_this_year() for _ in range(num_transactions)]
    payment_methods = random.choices(['Card', 'UPI', 'Cash'], k=num_transactions)
    statuses = random.choices(['Success', 'Failed'], k=num_transactions)

    transactions = pd.DataFrame({
        'transaction_id': transaction_ids,
        'order_id': order_ids,
        'product_id': product_ids,
        'quantity': quantities,
        'price': prices,
        'total_amount': total_amounts,
        'transaction_timestamp': timestamps,
        'payment_method': payment_methods,
        'status': statuses
    })
    return transactions

# Function to write data in chunks
def write_csv_in_chunks(df, filename, chunk_size=100000):
    df.to_csv(filename, index=False, header=True, chunksize=chunk_size)

# Number of records to generate (optimized for performance)
num_customers = 100000  # ~400 MB for customers
num_products = 200000   # ~700 MB for products
num_orders = 400000  # ~900 MB for orders
num_transactions = 600000 # ~2 GB for transactions

# Function to generate and write all data
def generate_data():
    start_time = time.time()

    # Generate data
    customers_df = generate_customers(num_customers)
    products_df = generate_products(num_products)
    orders_df = generate_orders(num_orders, customers_df, products_df)
    transactions_df = generate_transactions(num_transactions, orders_df, products_df)

    # Write to CSV files in chunks
    write_csv_in_chunks(customers_df, 'customers.csv')
    write_csv_in_chunks(products_df, 'products.csv')
    write_csv_in_chunks(orders_df, 'orders.csv')
    write_csv_in_chunks(transactions_df, 'transactions.csv')

    print(f"Data generation completed in {time.time() - start_time} seconds.")

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    process = multiprocessing.Process(target=generate_data)
    process.start()
    process.join()
