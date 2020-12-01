from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='ali')
        u.set_password('aliveli')
        self.assertFalse(u.check_password('veliveli'))
        self.assertTrue(u.check_password('aliveli'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='ali', email='ali@ali.com')
        u2 = User(username='veli', email='veli@veli.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'veli')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'ali')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u1.followers.count(), 0)


    def test_follow_posts(self):
        # creating four users
        u1 = User(username='ali', email='ali@ali.com')
        u2 = User(username='veli', email='veli@veli.com')
        u3 = User(username='ayse', email='ayse@ayse.com')
        u4 = User(username='fatma', email='fatma@fatma.com')
        db.session.add_all([u1, u2, u3, u3])

        # creating four posts
        now = datetime.utcnow()
        p1 = Post(body='hello from ali', author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body='hello from veli', author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body='hello from ayse', author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body='hello from fatma', author=u4,
                  timestamp=now + timedelta(seconds=2))
        
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        #setting up the followers
        u1.follow(u2)   # Ali follow Veli
        u1.follow(u4)   # Ali follows Fatma
        u2.follow(u3)   # Veli follows Ayse
        u3.follow(u4)   # Ayse follows Fatma
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)

        