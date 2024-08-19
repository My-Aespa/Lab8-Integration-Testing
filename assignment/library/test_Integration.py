# นายธนธรณ์ จูหลาย 653380131-7 Sec. 1
import pytest
from fastapi.testclient import TestClient
from main import app, get_db, User, Book, Borrowlist

# Create a test client to interact with the API
@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_borrowlist(client, db_session):
    # Create a user and a book for the borrowlist
    user = User(username="test_user_for_borrow", fullname="Test User For Borrow")
    db_session.add(user)
    db_session.commit()

    book = Book(title="Test Book For Borrow", firstauthor="Test Author", isbn="3344556677")
    db_session.add(book)
    db_session.commit()

    # Create a borrowlist entry by sending a POST request to the /borrowlist/ endpoint
    response = client.post("/borrowlist/", params={"user_id": user.id, "book_id": book.id})

    # Check that the API request was successful
    assert response.status_code == 200

    # Check that the borrowlist entry was successfully added to the database
    assert db_session.query(Borrowlist).filter_by(user_id=user.id, book_id=book.id).first()

def test_get_borrowlist(client, db_session):
    # Create a user and a book
    user = User(username="test_user_for_list", fullname="Test User For List")
    db_session.add(user)
    db_session.commit()

    book = Book(title="Test Book For List", firstauthor="Test Author", isbn="5566778899")
    db_session.add(book)
    db_session.commit()

    # Create a borrowlist entry
    borrowlist = Borrowlist(user_id=user.id, book_id=book.id)
    db_session.add(borrowlist)
    db_session.commit()

    # Retrieve the borrowlist of the user
    response = client.get(f"/borrowlist/{user.id}")
    assert response.status_code == 200

    # Check that the borrowlist contains the borrowed book
    borrowlist_items = response.json()
    assert len(borrowlist_items) > 0
    assert borrowlist_items[0]["user_id"] == user.id
    assert borrowlist_items[0]["book_id"] == book.id
