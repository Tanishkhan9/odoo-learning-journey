from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class StudentTestCase(TransactionCase):
    """Test cases for Student Model"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        super().setUpClass()
        
        # Create test data
        cls.student_model = cls.env['student.student']
        
    def setUp(self):
        """Set up test environment before each test"""
        super().setUp()
        
        # Create a test student
        self.test_student = self.student_model.create({
            'name': 'Test Student',
            'registration_number': 'TEST-001',
            'email': 'test@example.com',
            'phone': '1234567890',
            'birth_date': '2006-01-01',
            'status': 'new',
            'is_active': True,
        })
    
    # ==================== Create Tests ====================
    
    def test_create_student(self):
        """Test creating a student record"""
        student = self.student_model.create({
            'name': 'John Doe',
            'registration_number': 'STU-001',
            'email': 'john@example.com',
            'birth_date': '2005-05-15',
            'status': 'new',
        })
        
        self.assertTrue(student)
        self.assertEqual(student.name, 'John Doe')
        self.assertEqual(student.status, 'new')
        self.assertTrue(student.created_date)
    
    def test_create_multiple_students(self):
        """Test creating multiple student records"""
        students = self.student_model.create([
            {
                'name': 'Student 1',
                'registration_number': 'STU-101',
                'email': 'student1@example.com',
            },
            {
                'name': 'Student 2',
                'registration_number': 'STU-102',
                'email': 'student2@example.com',
            }
        ])
        
        self.assertEqual(len(students), 2)
        self.assertEqual(students[0].name, 'Student 1')
        self.assertEqual(students[1].name, 'Student 2')
    
    # ==================== Read Tests ====================
    
    def test_read_student(self):
        """Test reading student record"""
        student = self.student_model.browse(self.test_student.id)
        
        self.assertEqual(student.name, 'Test Student')
        self.assertEqual(student.email, 'test@example.com')
        self.assertEqual(student.status, 'new')
    
    def test_search_student_by_name(self):
        """Test searching student by name"""
        students = self.student_model.search([('name', '=', 'Test Student')])
        
        self.assertEqual(len(students), 1)
        self.assertEqual(students.name, 'Test Student')
    
    def test_search_student_by_status(self):
        """Test searching students by status"""
        # Create additional students with different statuses
        self.student_model.create({
            'name': 'Active Student',
            'registration_number': 'TEST-002',
            'email': 'active@example.com',
            'status': 'active',
        })
        
        active_students = self.student_model.search([('status', '=', 'active')])
        new_students = self.student_model.search([('status', '=', 'new')])
        
        self.assertEqual(len(active_students), 1)
        self.assertGreaterEqual(len(new_students), 1)
    
    def test_search_with_domain_and_limit(self):
        """Test searching with domain and limit"""
        students = self.student_model.search([], limit=1)
        
        self.assertEqual(len(students), 1)
    
    # ==================== Update Tests ====================
    
    def test_update_student(self):
        """Test updating student record"""
        self.test_student.write({
            'status': 'active',
            'phone': '9876543210'
        })
        
        self.assertEqual(self.test_student.status, 'active')
        self.assertEqual(self.test_student.phone, '9876543210')
    
    def test_update_multiple_students(self):
        """Test updating multiple students"""
        student2 = self.student_model.create({
            'name': 'Another Student',
            'registration_number': 'TEST-003',
            'email': 'another@example.com',
        })
        
        students = self.student_model.browse([self.test_student.id, student2.id])
        students.write({'status': 'active'})
        
        for student in students:
            self.assertEqual(student.status, 'active')
    
    # ==================== Delete Tests ====================
    
    def test_delete_student(self):
        """Test deleting student record"""
        student_id = self.test_student.id
        self.test_student.unlink()
        
        student = self.student_model.search([('id', '=', student_id)])
        self.assertEqual(len(student), 0)
    
    # ==================== Field Validation Tests ====================
    
    def test_email_uniqueness_constraint(self):
        """Test email uniqueness constraint"""
        with self.assertRaises(Exception):
            self.student_model.create({
                'name': 'Duplicate Email',
                'registration_number': 'TEST-DUP',
                'email': 'test@example.com',  # Same email
            })
    
    def test_registration_number_uniqueness(self):
        """Test registration number uniqueness constraint"""
        with self.assertRaises(Exception):
            self.student_model.create({
                'name': 'Duplicate Reg',
                'registration_number': 'TEST-001',  # Same registration number
                'email': 'unique@example.com',
            })
    
    def test_invalid_email_format(self):
        """Test invalid email format validation"""
        with self.assertRaises(ValidationError):
            self.student_model.create({
                'name': 'Invalid Email',
                'registration_number': 'TEST-INVALID',
                'email': 'invalid-email-without-at',
            })
    
    def test_future_birth_date_validation(self):
        """Test birth date cannot be in future"""
        future_date = date.today() + timedelta(days=1)
        
        with self.assertRaises(ValidationError):
            self.student_model.create({
                'name': 'Future Birth',
                'registration_number': 'TEST-FUTURE',
                'email': 'future@example.com',
                'birth_date': future_date,
            })
    
    # ==================== Computed Fields Tests ====================
    
    def test_age_computation(self):
        """Test age is computed correctly from birth date"""
        today = date.today()
        birth_date = date(today.year - 18, today.month, today.day)
        
        student = self.student_model.create({
            'name': 'Age Test Student',
            'registration_number': 'TEST-AGE',
            'email': 'agetest@example.com',
            'birth_date': birth_date,
        })
        
        self.assertEqual(student.age, 18)
    
    def test_enrollment_count_computation(self):
        """Test enrollment count is computed correctly"""
        self.assertEqual(self.test_student.enrollment_count, 0)
    
    # ==================== Action Tests ====================
    
    def test_action_activate(self):
        """Test activate action"""
        self.test_student.action_activate()
        
        self.assertEqual(self.test_student.status, 'active')
        self.assertTrue(self.test_student.is_active)
    
    def test_action_deactivate(self):
        """Test deactivate action"""
        self.test_student.action_deactivate()
        
        self.assertEqual(self.test_student.status, 'inactive')
        self.assertFalse(self.test_student.is_active)
    
    def test_action_graduate(self):
        """Test graduate action"""
        self.test_student.action_graduate()
        
        self.assertEqual(self.test_student.status, 'graduated')
    
    # ==================== Custom Methods Tests ====================
    
    def test_get_enrollment_count(self):
        """Test get enrollment count method"""
        count = self.test_student.get_enrollment_count()
        
        self.assertEqual(count, 0)
    
    def test_get_age_category(self):
        """Test get age category method"""
        # Create students of different ages
        student_young = self.student_model.create({
            'name': 'Young Student',
            'registration_number': 'TEST-YOUNG',
            'email': 'young@example.com',
            'birth_date': '2018-01-01',
        })
        
        student_teen = self.student_model.create({
            'name': 'Teen Student',
            'registration_number': 'TEST-TEEN',
            'email': 'teen@example.com',
            'birth_date': '2010-01-01',
        })
        
        # Categories depend on age calculation
        # This is a placeholder test
        self.assertTrue(hasattr(student_young, 'age'))
        self.assertTrue(hasattr(student_teen, 'age'))
    
    # ==================== Timestamp Tests ====================
    
    def test_created_date_set(self):
        """Test created date is set automatically"""
        self.assertTrue(self.test_student.created_date)
        self.assertLessEqual(
            (self.env.context.get('now', fields.Datetime.now()) - self.test_student.created_date).total_seconds(),
            10
        )
    
    def test_modified_date_updated(self):
        """Test modified date is updated on write"""
        original_modified = self.test_student.modified_date
        
        # Update the student
        self.test_student.write({'name': 'Updated Name'})
        
        self.assertGreaterEqual(self.test_student.modified_date, original_modified)
    
    # ==================== Edge Cases ====================
    
    def test_create_student_with_minimal_data(self):
        """Test creating student with only required fields"""
        student = self.student_model.create({
            'name': 'Minimal Student',
            'registration_number': 'TEST-MINIMAL',
            'email': 'minimal@example.com',
        })
        
        self.assertTrue(student)
        self.assertEqual(student.status, 'new')
        self.assertTrue(student.is_active)
    
    def test_search_returns_empty(self):
        """Test search returns empty list when no matches"""
        students = self.student_model.search([('name', '=', 'Non Existent Student')])
        
        self.assertEqual(len(students), 0)
