import unittest
from app import app, db, User, Conference, Submission

class CMTTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            from seed import seed_database
            seed_database()

    def login_as_admin(self):
        with self.client.session_transaction() as sess:
            admin = User.query.filter_by(role='admin').first()
            if admin:
                sess['user_id'] = admin.id
                sess['user_name'] = admin.name
                sess['user_role'] = admin.role

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Current Conferences', response.data)

    def test_upcoming_page(self):
        response = self.client.get('/upcoming')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upcoming Conferences', response.data)

    def test_archive_page(self):
        response = self.client.get('/archive')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Past Conferences Archive', response.data)

    def test_login_and_admin_settings_flow(self):
        with app.app_context():
            self.login_as_admin()
            response = self.client.get('/admin')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Administrator Dashboard', response.data)

            # Test Change Admin ID (email) and Password
            response = self.client.post('/admin/settings', data={
                'name': 'Chief Administrator',
                'email': 'superadmin@ljku.edu.in',
                'current_password': 'admin123',
                'new_password': 'newpassword123',
                'confirm_password': 'newpassword123'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            admin_user = User.query.filter_by(email='superadmin@ljku.edu.in').first()
            self.assertIsNotNone(admin_user)
            self.assertTrue(admin_user.check_password('newpassword123'))
            print("Admin ID and Password update verified!")

            # Restore default admin creds for other tests
            admin_user.email = 'admin@ljku.edu.in'
            admin_user.set_password('admin123')
            db.session.commit()

    def test_author_signup_and_submission(self):
        with app.app_context():
            response = self.client.post('/signup', data={
                'name': 'Dr. Priya Patel',
                'email': 'priya.patel@test.org',
                'password': 'priyapassword',
                'institution': 'LJKU Research Lab',
                'phone': '+91 9123456789'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            user = User.query.filter_by(email='priya.patel@test.org').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.role, 'author')

    def test_paper_submission_flow(self):
        with app.app_context():
            conf = Conference.query.first()
            response = self.client.post('/submit', data={
                'conference_id': conf.id,
                'author_name': 'Test Author',
                'author_email': 'test.author@example.com',
                'author_phone': '+91 9999988888',
                'institution': 'Test Institute',
                'presentation_type': 'Paper Presentation',
                'paper_title': 'Unit Test Paper Title',
                'abstract_text': 'This is a test abstract summary for automated verification.'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            sub = Submission.query.filter_by(author_email='test.author@example.com').first()
            self.assertIsNotNone(sub)
            self.assertTrue(sub.abstract_id.startswith('CMT-'))
            print("Generated Abstract ID:", sub.abstract_id)

    def test_add_conference_with_datepicker(self):
        with app.app_context():
            self.login_as_admin()
            response = self.client.post('/admin', data={
                'action': 'add_conference',
                'title': 'Interactive Date Picker Test Summit',
                'acronym': 'IDP-2026',
                'department_code': 'CSE',
                'state': 'upcoming',
                'start_date': '2026-10-15',
                'end_date': '2026-10-17',
                'submission_deadline': '2026-09-30',
                'registration_fee': '1500',
                'venue': 'LJKU Main Hall',
                'description': 'Testing date picker formatting.'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            conf = Conference.query.filter_by(acronym='IDP-2026').first()
            self.assertIsNotNone(conf)
            self.assertEqual(conf.start_date, 'October 15, 2026')
            self.assertEqual(conf.end_date, 'October 17, 2026')
            self.assertEqual(conf.submission_deadline, 'September 30, 2026')
            print("Date Picker Formatting Verified:", conf.start_date)

if __name__ == '__main__':
    unittest.main()
