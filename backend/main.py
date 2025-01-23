from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.middleware.cors import CORSMiddleware

# SQLite Database Connection
DB_URL = "sqlite:///./chatbot.db"  # SQLite database file
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Models
class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    contact_info = Column(Text)
    product_categories_offered = Column(Text)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    brand = Column(String(100))
    price = Column(Float)
    category = Column(String(100))
    description = Column(Text)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))

# Create Database Tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Utility Function to Fetch Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize Database with Sample Data
def init_db():
    db = SessionLocal()
    # Add Suppliers
    supplier1 = Supplier(name="Daksh Electronics", contact_info="contact@daksh.com", product_categories_offered="Electronics, Laptops")
    supplier2 = Supplier(name="hariom telecom", contact_info="contact@hariom.comcontact@hariom.com", product_categories_offered="Mobile Phones, Tablets")
    db.add_all([supplier1, supplier2])
    db.commit()

    # Add Products
    product1 = Product(name="Yoga", brand="Lenovo", price=899.99, category="Laptops", description="High performance laptop", supplier_id=1)
    product2 = Product(name="Galaxy Phone", brand="Samsung", price=699.99, category="Mobile Phones", description="Latest smartphone model", supplier_id=2)
    db.add_all([product1, product2])
    db.commit()
    db.close()

# Initialize the database (run once)
try:
    init_db()
except:
    pass

@app.get("/query")
def handle_query(user_input: str):
    """
    Process user input and return appropriate data.
    """
    db = next(get_db())

    # Basic Query Parsing
    if "products under" in user_input.lower():
        brand = user_input.lower().split("products under")[-1].strip()
        products = db.query(Product).filter(Product.brand.ilike(f"%{brand}%")).all()
        if not products:
            raise HTTPException(status_code=404, detail=f"No products found under brand {brand}.")
        return [{"id": p.id, "name": p.name, "brand": p.brand, "price": p.price} for p in products]

    elif "price of" in user_input.lower():
        product_name = user_input.lower().split("price of")[-1].strip()
        product = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"No product found with name {product_name}.")
        return {"id": product.id, "name": product.name, "price": product.price}

    else:
        raise HTTPException(status_code=400, detail="Query not understood. Please rephrase.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
