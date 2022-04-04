from flask_testing import TestCase
from website import db
from website.auth import auth
from website.views import views
from website.models import User, Music
import unittest
from flask import Flask
from datetime import date
from flask_login import LoginManager, current_user
from werkzeug.security import check_password_hash

class Test(TestCase):

    SQLALCHEMY_DATABASE_URI = 'sqlite://test.db'
    TESTING = True


    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///test.db'
        db.init_app(app)

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

        return app


    def setUp(self):
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


# Class for testing the User table in the application's database
class Test_User(Test):


    # NOT A TEST. Function to create a user
    def create_test_user(self):
        user = User(email='test@example.com', first_name='Test', password='password')
        db.session.add(user)
        db.session.commit()

        return user


    # Test that user is correctly added to database. Attributes not passed as 
    # parameters should be defaults.
    def test_add_user(self):
        user = self.create_test_user()

        assert user in db.session
        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'
        assert user.password == 'password'
        assert not user.is_admin
        assert user.background_color == '#000000'
        assert user.drum_color == '#dcdcdc'
        assert user.sign_up_date == date.today()

    
    # Test function to change user's email
    def test_set_email(self):
        user = self.create_test_user()
        user.set_email('new_email@example.com')

        assert user.email == 'new_email@example.com'


    # Test function to change user's first name
    def test_set_first_name(self):
        user = self.create_test_user()
        user.set_first_name('Emily')

        assert user.first_name == 'Emily'


    # Test function to change user's password
    def test_set_email(self):
        user = self.create_test_user()
        user.set_password('steelDores')

        assert user.password == 'steelDores'


    # Test function to change user's admin status
    def test_set_admin(self):
        user = self.create_test_user()
        user.set_is_admin(True)

        assert user.is_admin


    # Test function to change user's desired background color
    def test_set_background(self):
        user = self.create_test_user()
        user.set_background('#ffffff')

        assert user.background_color == '#ffffff'

    
    # Test function to change user's desired drum color
    def test_set_drum_color(self):
        user = self.create_test_user()
        user.set_drum_color('#47ffff')

        assert user.drum_color == '#47ffff'


# Class for testing the Music table in the application's database
class Test_Music(Test):


    # NOT A TEST. Function to create a music sample.
    def create_test_music(self):
        music = Music(title='Song Title')
        db.session.add(music)
        db.session.commit()
        return music


    # Test that music is correctly added to database. Attributes not passed as 
    # parameters should be defaults.
    def test_add_music(self):
        music = self.create_test_music()

        assert music in db.session
        assert music.title == 'Song Title'
        assert music.composer == ''
        assert music.genre == ''
        assert music.description == ''
        assert music.pdf_link == ''
        assert music.audio_link == ''
        assert music.user_id == None
        assert music.date == date.today()

    # Test function to change music sample's title
    def test_set_title(self):
        music = self.create_test_music()
        music.set_title('New Title')

        assert music.title == 'New Title'

    # Test function to change music sample's composer
    def test_set_composer(self):
        music = self.create_test_music()
        music.set_composer('Mozart')

        assert music.composer == 'Mozart'

    # Test function to change music sample's genre
    def test_set_genre(self):
        music = self.create_test_music()
        music.set_genre('Classical')

        assert music.genre == 'Classical'


    # Test function to change music sample's description
    def test_set_description(self):
        music = self.create_test_music()
        music.set_description('A very nice tune.')

        assert music.description == 'A very nice tune.'


    # Test function to change music sample's PDF link
    def test_set_pdf(self):
        music = self.create_test_music()
        music.set_pdf('https://musescore.com/classicman/fur-elise')

        assert music.pdf_link == 'https://musescore.com/classicman/fur-elise'


    # Test function to change music sample's PDF link
    def test_set_audio(self):
        music = self.create_test_music()
        music.set_audio('https://www.youtube.com')

        assert music.audio_link == 'https://www.youtube.com'


# Class for testing the web application's forms
class Test_Forms(Test):

    def test_sign_up(self):

        form = {'email':'bill@example.com', 'firstName': 'Bill',
                'password1': 'password', 'password2': 'password'}

        with self.client:
            response = self.client.post('/sign-up', data=form)
            #assert response.request.path == '/menu'

            # Check that a user has been created
            assert db.session.query(User).count() == 1

            # Check that added user has given attributes
            user = User.query.filter_by(email=form['email']).first()
            assert user.email == form['email']
            assert user.first_name == form['firstName']
            assert check_password_hash(user.password, form['password1'])
        
            # Check that user is not an admin
            assert not user.is_admin

            # Check that user is logged in after signing up
            assert current_user.is_authenticated

            # Test that a new user cannot be created with an email that already exists
            with self.assertRaises(Exception) as context:
                self.client.post('/sign-up', data=form)

            # Check that no new users have been created
            assert db.session.query(User).count() == 1

            # Test that email must be greater than 3 characters
            form['email'] = 'no'
            with self.assertRaises(Exception) as context:
                self.client.post('/sign-up', data=form)
            assert db.session.query(User).count() == 1

            # Test that first name must be greater than 1 character
            form['email'] = 'bill@example.com'
            form['firstName'] = 'B'
            with self.assertRaises(Exception) as context:
                self.client.post('/sign-up', data=form)
            assert db.session.query(User).count() == 1

            # Test that passwords must match
            form['firstName'] = 'Bill'
            form['password2'] = 'steeldrum'
            with self.assertRaises(Exception) as context:
                self.client.post('/sign-up', data=form)
            assert db.session.query(User).count() == 1

            # Test that password must be at least 7 characters
            form['password1'] = 'tester'
            form['password2'] = 'tester'
            with self.assertRaises(Exception) as context:
                self.client.post('/sign-up', data=form)
            assert db.session.query(User).count() == 1

    def test_login(self):
        # Create a user in database
        form_user = {'email':'bill@example.com', 'firstName': 'Bill',
                'password1': 'password', 'password2': 'password'}

        self.client.post('/sign-up', data=form_user)
        self.client.get('/logout')

        with self.client:

            # Test that user is not logged in when password is not valid
            form = {'email': 'bill@example.com', 'password': 'incorrect'}
            with self.assertRaises(Exception) as context:
                self.client.post('/sign-up', data=form)
            assert not current_user.is_authenticated

            # Test that user is not logged in if email does not exist
            form['email'] = 'bob@example.com'
            with self.assertRaises(Exception) as context:
                self.client.post('/sign-up', data=form)
            assert not current_user.is_authenticated

            # Test that user is logged in when entering valid info
            form['email'] = 'bill@example.com'
            form['password'] = 'password'
            self.client.post('/login', data=form)

            assert current_user.is_authenticated
            assert current_user.email == form['email']
            assert check_password_hash(current_user.password, form['password'])

    def test_logout(self):
        with self.client:
            form_user = {'email':'bill@example.com', 'firstName': 'Bill',
                'password1': 'password', 'password2': 'password'}

            self.client.post('/sign-up', data=form_user)
            assert current_user.is_authenticated

            # Test that user is logged out correctly
            self.client.get('/logout')
            assert not current_user.is_authenticated

    def test_settings(self):

        # Create a user in database
        form_user = {'email':'bill@example.com', 'firstName': 'Bill',
                'password1': 'password', 'password2': 'password'}

        self.client.post('/sign-up', data=form_user)
        user = User.query.one()

        form = {'background':'#ffffff', 'drum-color': '#000000',
                'new-password': 'new password'}

        self.client.post('/settings', data=form)

        # Check that user settings were changed
        assert user.background_color == '#ffffff'
        assert user.drum_color == '#000000'
        assert check_password_hash(user.password, form['new-password'])

        # Check that password is not changed if nothing is written in field
        form['new-password'] = None
        self.client.post('/settings', data=form)
        assert check_password_hash(user.password, 'new password')

        # Check that password is not changed if new password is less than 7 characters
        form['new-password'] = 'tester'
        with self.assertRaises(Exception) as context:
            self.client.post('/settings', data=form)
        assert check_password_hash(user.password, 'new password')

    def test_add_music_form(self):

        # Create a user in database
        form_user = {'email':'bill@example.com', 'firstName': 'Bill',
                'password1': 'password', 'password2': 'password'}

        self.client.post('/sign-up', data=form_user)

        # Info for new music sample
        form = {'title':'Fur Elise', 'composer':'Beethoven', 'genre':'Classical',
                'description':'A nice tune.', 
                'pdf_link': 'https://musescore.com/classicman/fur-elise',
                'audio_link': 'https://www.youtube.com'}

        self.client.post('/add-music', data=form)

        # Check that a row has been added to the Music table
        assert db.session.query(Music).count() == 1

        sample = Music.query.one()

        # Check that added sample has given attributes
        assert sample.title == form['title']
        assert sample.composer == form['composer']
        assert sample.genre == form['genre']
        assert sample.description == form['description']
        assert sample.pdf_link == form['pdf_link']
        assert sample.audio_link == form['audio_link']

        # Check that title must be entered
        form['title'] = ''
        with self.assertRaises(Exception) as context:
            self.client.post('/add-music', data=form)

        # Check that no new samples have been added
        assert db.session.query(User).count() == 1

    
if __name__ == '__main__':
    unittest.main()