import unittest
from new_app import new_app, db, Sum
from faker import Faker

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = new_app.test_client()
        new_app.app_context().push()
        db.create_all()

        db.session.add(Sum(num1=1, num2=1, result=2))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_sum(self):
        fake = Faker()
        num1 = fake.random_number(digits=3)
        num2 = fake.random_number(digits=3)
        print(num1, num2)
        payload = {'num1': num1, 'num2': num2}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()

        self.assertIsNotNone(data)
        self.assertEqual(data['result'], num1 + num2)

# Write a negative test case: test the new endpoint with an invalid filter value
    def test_invalid_filter_value(self):
        response = self.app.get('/sum/results/999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])


if __name__ == '__main__':
    unittest.main()


