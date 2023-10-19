from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tests.common import SingleTransactionCase


class TestDemoOdooSingleTransactionCase(SingleTransactionCase):
    def setUp(self, *args, **kwargs):
        """setUp"""
        super(TestDemoOdooSingleTransactionCase, self).setUp(*args, **kwargs)
        print("Run setUp")

    # 第一個測試
    def test_hello_world(self):
        print("--------------第一個測試 : singletransactioncase-----------------")
        """test_hello_world"""
        self.assertEqual(0, 0, "test hello world")

    # 第二個測試
    def test_datetime_validation(self):
        print("--------------第二個測試 : singletransactioncase-----------------")
        """test_datetime_validation"""
        values = {
            "name": "hello",
            "start_datetime": "2020-02-01",
            "stop_datetime": "2020-01-01",
        }
        with self.assertRaises(ValidationError):
            self.env["twturbiks_first_demo.twturbiks_first_demo"].create(values)

    # 第三個測試
    def test_field_compute_demo(self):
        print("--------------第三個測試 : singletransactioncase-----------------")
        """test_field_compute_demo"""
        values = {
            "name": "hello",
            "input_number": 2,
            "start_datetime": "2020-02-01",
            "stop_datetime": "2020-04-01",
        }
        data = self.env["twturbiks_first_demo.twturbiks_first_demo"].create(values)
        self.assertEqual(data.field_compute_demo, data.input_number * 1000)
