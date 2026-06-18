from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class Student(models.Model):
    """
    Student Model
    
    This model represents a student in the system.
    Students have personal information and can be enrolled in courses.
    
    Security:
    - Managers: Full access
    - Users: Read-only access to active students
    """
    
    _name = 'student.student'
    _description = 'Student'
    _rec_name = 'name'
    _order = 'name ASC'
    
    # ==================== Basic Information ====================
    name = fields.Char(
        string='Full Name',
        required=True,
        index=True,
        help='Full name of the student'
    )
    
    email = fields.Char(
        string='Email',
        required=True,
        help='Email address of the student'
    )
    
    phone = fields.Char(
        string='Phone Number',
        help='Contact phone number'
    )
    
    birth_date = fields.Date(
        string='Date of Birth',
        help='Birth date of the student'
    )
    
    # ==================== Computed Fields ====================
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
        help='Age calculated from birth date'
    )
    
    # ==================== Status & Classification ====================
    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('graduated', 'Graduated'),
            ('dropped', 'Dropped Out'),
        ],
        string='Status',
        default='new',
        required=True,
        help='Current status of the student'
    )
    
    registration_number = fields.Char(
        string='Registration Number',
        unique=True,
        required=True,
        help='Unique registration/roll number'
    )
    
    # ==================== Relations ====================
    # Many to One - Student belongs to one department
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        help='Department the student belongs to'
    )
    
    # Many to Many - Student can be enrolled in multiple courses
    course_ids = fields.Many2many(
        'course.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Enrolled Courses',
        help='Courses student is enrolled in'
    )
    
    # ==================== Additional Information ====================
    notes = fields.Text(
        string='Notes',
        help='Additional notes about the student'
    )
    
    is_active = fields.Boolean(
        string='Is Active',
        default=True,
        help='Whether student is active'
    )
    
    enrollment_count = fields.Integer(
        string='Course Count',
        compute='_compute_enrollment_count',
        store=False,
        help='Number of courses enrolled'
    )
    
    # ==================== Timestamps ====================
    created_date = fields.Datetime(
        string='Created Date',
        default=lambda self: fields.Datetime.now(),
        readonly=True,
        help='When the record was created'
    )
    
    modified_date = fields.Datetime(
        string='Modified Date',
        default=lambda self: fields.Datetime.now(),
        readonly=True,
        help='Last modification date'
    )
    
    # ==================== SQL Constraints ====================
    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Email must be unique!'),
        ('registration_unique', 'UNIQUE(registration_number)', 'Registration number must be unique!'),
    ]
    
    # ==================== Computed Fields Logic ====================
    @api.depends('birth_date')
    def _compute_age(self):
        """Calculate age from birth date"""
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year
                # Adjust if birthday hasn't occurred this year
                if (today.month, today.day) < (record.birth_date.month, record.birth_date.day):
                    record.age -= 1
            else:
                record.age = 0
    
    @api.depends('course_ids')
    def _compute_enrollment_count(self):
        """Count number of enrolled courses"""
        for record in self:
            record.enrollment_count = len(record.course_ids)
    
    # ==================== Validations & Constraints ====================
    @api.constrains('email')
    def _check_email_format(self):
        """Validate email format"""
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError('Invalid email format! Email must contain @')
    
    @api.constrains('birth_date')
    def _check_birth_date(self):
        """Validate birth date is not in future"""
        for record in self:
            if record.birth_date and record.birth_date > date.today():
                raise ValidationError('Birth date cannot be in the future!')
    
    @api.constrains('age')
    def _check_age(self):
        """Validate minimum age"""
        for record in self:
            if record.age and record.age < 5:
                raise ValidationError('Student must be at least 5 years old!')
    
    # ==================== Custom Methods ====================
    def action_activate(self):
        """Activate student"""
        self.write({
            'status': 'active',
            'is_active': True,
            'modified_date': fields.Datetime.now()
        })
        return True
    
    def action_deactivate(self):
        """Deactivate student"""
        self.write({
            'status': 'inactive',
            'is_active': False,
            'modified_date': fields.Datetime.now()
        })
        return True
    
    def action_graduate(self):
        """Mark student as graduated"""
        self.write({
            'status': 'graduated',
            'modified_date': fields.Datetime.now()
        })
        return True
    
    def get_enrollment_count(self):
        """Get number of courses enrolled"""
        return len(self.course_ids)
    
    def get_age_category(self):
        """Get age category of student"""
        if not self.age:
            return 'Unknown'
        elif self.age < 12:
            return 'Primary'
        elif self.age < 18:
            return 'Secondary'
        else:
            return 'Senior'
    
    # ==================== Override Methods ====================
    @api.model_create_multi
    def create(self, vals_list):
        """Override create method"""
        # Add created_date to each record
        for vals in vals_list:
            if 'created_date' not in vals:
                vals['created_date'] = fields.Datetime.now()
            if 'modified_date' not in vals:
                vals['modified_date'] = fields.Datetime.now()
        
        return super().create(vals_list)
    
    def write(self, vals):
        """Override write method to track modifications"""
        vals['modified_date'] = fields.Datetime.now()
        return super().write(vals)
    
    def unlink(self):
        """Override unlink method"""
        # Could add additional logic before deletion
        return super().unlink()
    
    @api.onchange('status')
    def _onchange_status(self):
        """Handle status change"""
        if self.status == 'graduated':
            # Could add warning or additional logic
            pass
    
    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        """Handle birth date change"""
        if self.birth_date and self.birth_date > date.today():
            return {
                'warning': {
                    'title': 'Invalid Date',
                    'message': 'Birth date cannot be in the future!'
                }
            }
