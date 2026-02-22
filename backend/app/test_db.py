from sqlalchemy import create_engine

DATABASE_URL = "mysql+mysqlconnector://root:porsche718~1%21%40@localhost:3306/pricesenseai"


try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("✅ Connected to MySQL successfully!")
except Exception as e:
    print("❌ Connection failed!")
    print("Error:", e)
