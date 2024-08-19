# นายธนธรณ์ จูหลาย 653380131-7 Sec. 1
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, User, Book

# ใช้ฐานข้อมูลจริง
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture สำหรับการเชื่อมต่อฐานข้อมูล
@pytest.fixture(scope="function")
def db_session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)