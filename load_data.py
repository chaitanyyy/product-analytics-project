# load_data.py

import pandas as pd
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

# ⚠️ PUT YOUR MYSQL PASSWORD BELOW
# If no password just leave it empty like: ""
MYSQL_PASSWORD = "chaitany41"

print("="*50)
print("STEP 1: Connecting to MySQL...")
try:
    engine = create_engine(
        f'mysql+pymysql://root:{MYSQL_PASSWORD}@localhost:3306/product_analytics'
    )
    # Test connection
    with engine.connect() as conn:
        print("✅ Connected to MySQL!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("Check your MySQL password!")
    exit()

print("\nSTEP 2: Reading CSV file...")
df = pd.read_csv(
    r'C:\Users\Mane Chaitanya\Desktop\product-analytics-project\data\raw\online_retail_II.csv',
    encoding='utf-8',
    on_bad_lines='skip'
)
print(f"✅ Loaded {len(df):,} rows")

print("\nSTEP 3: Cleaning data...")

# Rename YOUR columns to our table columns
df.columns = [
    'invoice_no', 'stock_code', 'description',
    'quantity', 'invoice_date', 'unit_price',
    'customer_id', 'country'
]

# Remove rows with no customer
df = df.dropna(subset=['customer_id'])

# Remove cancelled orders (start with C)
df = df[~df['invoice_no'].astype(str).str.startswith('C')]

# Remove bad quantities and prices
df = df[(df['quantity'] > 0) & (df['unit_price'] > 0)]

# Calculate revenue
df['revenue'] = df['quantity'] * df['unit_price']

# Fix data types
df['customer_id']  = df['customer_id'].astype(int).astype(str)
df['invoice_date'] = pd.to_datetime(
    df['invoice_date']
).dt.date
df['stock_code']   = df['stock_code'].astype(str).str.strip()
df['description']  = df['description'].astype(str).str.strip()

print(f"✅ After cleaning: {len(df):,} rows")

print("\nSTEP 4: Loading transactions into MySQL...")
print("(Please wait 2-3 minutes...)")
df[[
    'invoice_no','stock_code','customer_id',
    'invoice_date','quantity','unit_price','revenue','country'
]].to_sql(
    'transactions', engine,
    if_exists='replace',
    index=False,
    chunksize=500
)
print("✅ Transactions loaded!")

print("\nSTEP 5: Loading customers...")
customers = df.groupby('customer_id').agg(
    first_seen_date=('invoice_date','min'),
    country=('country','first')
).reset_index()
customers.to_sql(
    'customers', engine,
    if_exists='replace',
    index=False
)
print(f"✅ Customers loaded: {len(customers):,} rows")

print("\nSTEP 6: Loading products...")
products = (
    df[['stock_code','description']]
    .drop_duplicates('stock_code')
)
products.to_sql(
    'products', engine,
    if_exists='replace',
    index=False
)
print(f"✅ Products loaded: {len(products):,} rows")

print("\n" + "="*50)
print("🎉 ALL DATA LOADED INTO MYSQL!")
print("="*50)
print(f"\nSummary:")
print(f"  Transactions : {len(df):,}")
print(f"  Customers    : {len(customers):,}")
print(f"  Products     : {len(products):,}")