from odoo.tests.common import TransactionCase


class CourseTestCase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.course_model = self.env['course.course']

    def test_create_course(self):
        course = self.course_model.create({
            'name': 'Test Course',
            'code': 'TC-001',
            'duration_weeks': 4,
        })

        self.assertEqual(course.name, 'Test Course')
        self.assertEqual(course.code, 'TC-001')