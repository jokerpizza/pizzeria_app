
import unittest
from app import app, db
from models import User, Sale, Cost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        with app.app_context():
            user = User(username='testuser', password_hash='hashed')
            db.session.add(user)
            db.session.commit()
            self.assertEqual(User.query.count(), 1)

    def test_schema_update(self):
        with app.app_context():
            # Ensure the columns exist
            result = db.engine.execute("PRAGMA table_info(sales);")
            columns = [row[1] for row in result.fetchall()]
            self.assertIn("user_id", columns)

if __name__ == '__main__':
    unittest.main()
