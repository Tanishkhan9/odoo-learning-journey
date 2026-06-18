# ORM Cheatsheet

## What is ORM?

ORM (Object-Relational Mapping) allows you to interact with the database using Python objects instead of writing SQL queries.

## Creating Models

### Basic Model Definition

```python
from odoo import models, fields

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Information'
    
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    birth_date = fields.Date(string='Birth Date')
    is_active = fields.Boolean(string='Active', default=True)
```

## Field Types

### Text Fields
```python
name = fields.Char(string='Name', size=100)
description = fields.Text(string='Description')
```

### Numeric Fields
```python
age = fields.Integer(string='Age')
salary = fields.Float(string='Salary', digits=(10, 2))
percentage = fields.Float(string='Percentage')
```

### Date/Time Fields
```python
birth_date = fields.Date(string='Birth Date')
created_at = fields.Datetime(string='Created')
```

### Boolean Fields
```python
is_active = fields.Boolean(string='Active', default=True)
```

### Selection Fields
```python
status = fields.Selection([
    ('draft', 'Draft'),
    ('submitted', 'Submitted'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
], string='Status', default='draft')
```

### Relational Fields
```python
# Many to One (Foreign Key)
department_id = fields.Many2one('hr.department', string='Department')

# One to Many (Reverse relation)
employee_ids = fields.One2many('hr.employee', 'department_id', string='Employees')

# Many to Many (Join table)
course_ids = fields.Many2many('course.course', string='Courses')
```

## Common Field Attributes

```python
field = fields.Char(
    string='Field Label',           # Display name
    help='Help text',              # Tooltip
    required=True,                 # Mandatory field
    readonly=True,                 # Read-only
    store=True,                    # Store in database
    compute='_compute_field',      # Computed field
    default='value',               # Default value
    size=255,                      # Max length
    index=True,                    # Database index
    translate=True                 # Translatable
)
```

## CRUD Operations

### Create
```python
# Method 1: create() method
student = self.env['student.student'].create({
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '1234567890'
})

# Method 2: Using + operator
values = {
    'name': 'Jane Doe',
    'email': 'jane@example.com'
}
student = self.env['student.student'].create(values)
```

### Read
```python
# Get single record by ID
student = self.env['student.student'].browse(1)

# Search records
students = self.env['student.student'].search([
    ('name', '=', 'John')
])

# Search with limit
first_student = self.env['student.student'].search([], limit=1)

# Get all records
all_students = self.env['student.student'].search([])
```

### Update
```python
# Update single record
student.write({
    'name': 'Updated Name',
    'email': 'updated@example.com'
})

# Update multiple records
students = self.env['student.student'].search([('is_active', '=', False)])
students.write({'is_active': True})
```

### Delete
```python
# Delete single record
student.unlink()

# Delete multiple records
students = self.env['student.student'].search([('is_active', '=', False)])
students.unlink()
```

## Search Operators

```python
# Equality
[('name', '=', 'John')]
[('age', '=', 25)]

# Inequality
[('status', '!=', 'draft')]
[('age', '!=', 25)]

# Greater/Less than
[('age', '>', 18)]
[('age', '<', 65)]
[('age', '>=', 18)]
[('age', '<=', 65)]

# Contains/Like
[('name', 'like', 'john')]
[('name', 'ilike', 'JOHN')]  # Case insensitive

# In list
[('status', 'in', ['draft', 'submitted'])]

# Not in list
[('status', 'not in', ['rejected', 'cancelled'])]

# Is null
[('email', '=', False)]

# Is not null
[('email', '!=', False)]
```

## Search with Multiple Conditions

```python
# AND condition (comma-separated)
students = self.env['student.student'].search([
    ('name', 'ilike', 'john'),
    ('is_active', '=', True),
    ('age', '>', 18)
])

# OR condition (using |)
students = self.env['student.student'].search([
    '|',
    ('status', '=', 'draft'),
    ('status', '=', 'submitted')
])

# Complex conditions
students = self.env['student.student'].search([
    '|',
    ('name', 'ilike', 'john'),
    ('email', 'ilike', 'john'),
    ('is_active', '=', True)
])
```

## Computed Fields

```python
class Student(models.Model):
    _name = 'student.student'
    
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"
```

## Methods

### Standard Methods

```python
class Student(models.Model):
    _name = 'student.student'
    
    # Custom method
    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year
    
    # Override write method
    def write(self, vals):
        return super().write(vals)
    
    # Override create method
    def create(self, vals_list):
        return super().create(vals_list)
```

## Common Model Attributes

```python
class Student(models.Model):
    _name = 'student.student'              # Database table name
    _description = 'Student'               # Model description
    _rec_name = 'name'                     # Field to display in relations
    _order = 'id DESC'                     # Default ordering
    _sql_constraints = [                   # Database constraints
        ('email_unique', 'UNIQUE(email)', 'Email must be unique!')
    ]
    _inherit = 'base.model'                # Inherit from another model
```

## Important Methods

```python
# Get total count
count = self.env['student.student'].search_count([])

# Get with offset and limit
students = self.env['student.student'].search(
    [],
    offset=10,
    limit=5
)

# Get with specific fields (better performance)
students = self.env['student.student'].search_read(
    [],
    fields=['name', 'email']
)

# Sort results
students = self.env['student.student'].search([], order='name')
```

## Context & Environment

```python
# Access current user
current_user = self.env.user

# Get company
company = self.env.company

# Set context
records = self.env['student.student'].with_context(custom_key='value').search([])

# Get from context
value = self._context.get('custom_key')
```

## Tips & Best Practices

1. ✅ Always use ORM methods instead of raw SQL
2. ✅ Use `search_read()` for better performance when you need specific fields
3. ✅ Add `required=True` for mandatory fields
4. ✅ Use `index=True` for frequently searched fields
5. ✅ Store computed fields if they're accessed frequently
6. ✅ Use constraints for data validation
7. ✅ Document your models with `_description`

---

Next: [Models, Views & Actions](07-models-views-actions.md)
