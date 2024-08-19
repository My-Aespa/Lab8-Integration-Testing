import pytest
from main import User, Book, Borrowlist

def test_create_borrowlist(client, db_session):
    # สร้างผู้ใช้และหนังสือเพื่อเชื่อมโยงกับรายการยืม
    user = User(username="test_user_for_borrow", fullname="Test User For Borrow")
    db_session.add(user)
    db_session.commit()

    book = Book(title="Test Book For Borrow", firstauthor="Test Author", isbn="3344556677")
    db_session.add(book)
    db_session.commit()

    # ทำการ POST request ไปยัง /borrowlist/ endpoint เพื่อสร้างรายการยืมหนังสือ
    response = client.post("/borrowlist/", json={"user_id": user.id, "book_id": book.id})

    # ตรวจสอบว่า API request สำเร็จ
    assert response.status_code == 200

    # ตรวจสอบว่า user_id และ book_id ที่ส่งไปตรงกับที่ได้รับจาก API
    borrowlist_data = response.json()
    assert borrowlist_data["user_id"] == user.id
    assert borrowlist_data["book_id"] == book.id

    # ตรวจสอบว่ารายการยืมถูกเพิ่มลงในฐานข้อมูลเรียบร้อยแล้ว
    assert db_session.query(Borrowlist).filter_by(user_id=user.id, book_id=book.id).first()

def test_get_borrowlist(client, db_session):
    # สร้างผู้ใช้และหนังสือ
    user = User(username="test_user_for_list", fullname="Test User For List")
    db_session.add(user)
    db_session.commit()

    book = Book(title="Test Book For List", firstauthor="Test Author", isbn="5566778899")
    db_session.add(book)
    db_session.commit()

    # สร้างรายการยืมหนังสือ
    borrowlist = Borrowlist(user_id=user.id, book_id=book.id)
    db_session.add(borrowlist)
    db_session.commit()

    # ดึงข้อมูลรายการยืมหนังสือของผู้ใช้
    response = client.get(f"/borrowlist/{user.id}")
    assert response.status_code == 200

    # ตรวจสอบว่ามีรายการยืมหนังสือที่ผู้ใช้ยืมอยู่
    borrowlist_items = response.json()
    assert len(borrowlist_items) > 0
    assert borrowlist_items[0]["user_id"] == user.id
    assert borrowlist_items[0]["book_id"] == book.id
