from utils.tests_helpers import TestMixin, AssertsMixin


class TestViews(TestMixin, AssertsMixin):
    def test_index_redirect(self):
        response = self.login('driver')
        self.assert_with_message(200, response, '(Driver)')
        self.assert_with_message(200, response, 'Taskboard')
