# Interview Questions

## Basic Odoo Concepts

### Q1: What is Odoo?
**Answer**: Odoo is an open-source suite of business management applications. It includes CRM, Sales, Inventory, Accounting, HR, Projects, and more. It's built with Python and uses PostgreSQL as the database.

### Q2: What are the main components of Odoo?
**Answer**: 
- **Web Client**: Browser-based UI
- **Server**: Backend written in Python
- **ORM**: Object-Relational Mapping for database access
- **Database**: PostgreSQL for data storage
- **Modules**: Packaged functionality that can be installed/uninstalled

### Q3: What is a Module in Odoo?
**Answer**: A module (also called an addon) is a package containing models, views, controllers, and other components that add specific functionality to Odoo. Examples: CRM, Sales, Inventory modules.

---

## Models and ORM

### Q4: What is ORM and why is it used?
**Answer**: ORM (Object-Relational Mapping) allows database interaction using Python objects instead of SQL. Benefits:
- Abstracts database complexity
- Prevents SQL injection
- Provides consistent interface across different databases
- Makes code more maintainable

### Q5: What are the different field types in Odoo?
**Answer**: 
- **Text**: Char, Text
- **Numeric**: Integer, Float
- **Date/Time**: Date, Datetime
- **Boolean**: Boolean
- **Selection**: Selection
- **Relational**: Many2one, One2many, Many2many
- **Computed**: Computed fields with dependencies

### Q6: Explain Many2one, One2many, and Many2many relationships.
**Answer**:
- **Many2one**: Multiple records point to one record (e.g., Student → Department)
- **One2many**: Inverse of Many2one; one record has multiple related records
- **Many2many**: Records have multiple related records and vice versa (e.g., Students ↔ Courses)

### Q7: How do you create a model in Odoo?
**Answer**:
```python
from odoo import models, fields

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student'
    
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
```

### Q8: What is the difference between `store=True` and `compute`?
**Answer**:
- **Computed fields** (`compute`): Calculated on-the-fly, not stored
- **Stored computed fields** (`store=True`): Calculated and stored in database
- Use `store=True` if frequently accessed for better performance

### Q9: How do you search for records in Odoo?
**Answer**:
```python
# Search with domain
students = self.env['student.student'].search([
    ('name', 'ilike', 'john'),
    ('age', '>', 18)
])

# Get single record
student = self.env['student.student'].browse(1)

# Search with limit and offset
results = self.env['student.student'].search([], limit=10, offset=0)
```

---

## Views and UI

### Q10: What are the different view types in Odoo?
**Answer**:
- **Form**: Detailed view for single record
- **List/Tree**: Tabular view of multiple records
- **Search**: Filtering and search interface
- **Kanban**: Card-based view
- **Calendar**: Calendar display
- **Chart**: Graph/chart visualization
- **Gallery**: Image gallery view

### Q11: What is the purpose of a Search View?
**Answer**: Search view provides filtering capabilities including:
- Quick search fields
- Predefined filters
- Advanced search options
- Grouping functionality

### Q12: How do you define a Form View?
**Answer**:
```xml
<form string="Student">
    <header>
        <button name="action_approve" type="object" string="Approve"/>
        <field name="status" widget="statusbar"/>
    </header>
    <sheet>
        <group>
            <field name="name"/>
            <field name="email"/>
        </group>
    </sheet>
</form>
```

### Q13: What are view attributes and their purpose?
**Answer**: View attributes control behavior and appearance:
- `required="1"`: Field is mandatory
- `readonly="1"`: Field cannot be edited
- `invisible="1"`: Field is hidden
- `attrs="{'readonly': [('status', '=', 'done')]}"`: Conditional rendering

---

## Security and Access Control

### Q14: Explain Odoo's security layers.
**Answer**:
1. **Authentication**: User login validation
2. **Access Rights (ACL)**: Model-level permissions (read, write, create, delete)
3. **Record Rules**: Row-level access based on domain conditions
4. **Field Access**: Column-level permissions per field

### Q15: How do you define access rights in Odoo?
**Answer**: In `security/ir.model.access.csv`:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_student_manager,Student Manager,model_student_student,group_student_manager,1,1,1,1
access_student_user,Student User,model_student_student,group_student_user,1,0,0,0
```

### Q16: What are Record Rules and how do they work?
**Answer**: Record Rules (ir.rule) provide row-level security:
- Control which records users can access
- Based on domain conditions
- Applied per group
- Example:
```xml
<record id="rule_student_my_records" model="ir.rule">
    <field name="domain_force">[('create_uid', '=', user.id)]</field>
</record>
```

### Q17: How do you use `sudo()` in Odoo?
**Answer**: 
- `sudo()` bypasses access checks (admin mode)
- Use only when necessary for backend operations
- Example:
```python
# Execute with admin privileges
self.env['student.student'].sudo().write({'field': 'value'})
```

---

## Module Structure and Configuration

### Q18: What is the structure of an Odoo module?
**Answer**:
```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
├── views/
├── security/
├── data/
├── reports/
├── static/
└── tests/
```

### Q19: What should be in `__manifest__.py`?
**Answer**:
```python
{
    'name': 'Module Name',
    'version': '1.0',
    'category': 'Category',
    'depends': ['base', 'other_module'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/views.xml',
    ],
    'installable': True,
}
```

### Q20: What is the purpose of `__init__.py`?
**Answer**: 
- Makes Python directory a package
- Imports models and controllers to make them available
- Example:
```python
from . import models
from . import controllers
```

---

## Advanced Topics

### Q21: What is inheritance in Odoo models?
**Answer**:
- **Classical Inheritance**: Child model inherits all parent fields
- **Delegation Inheritance**: Relationship using Many2one
- **Mixins**: Share methods across models
- Example:
```python
class StudentExtended(models.Model):
    _inherit = 'student.student'
    additional_field = fields.Char()
```

### Q22: What are computed fields and how do you create them?
**Answer**:
```python
@api.depends('first_name', 'last_name')
def _compute_full_name(self):
    for record in self:
        record.full_name = f"{record.first_name} {record.last_name}"

full_name = fields.Char(compute='_compute_full_name', store=True)
```

### Q23: What is the `@api` decorator?
**Answer**: Decorators modify method behavior:
- `@api.model`: Method on model class, not records
- `@api.multi`: Method processes multiple records (legacy)
- `@api.depends`: Specifies computed field dependencies
- `@api.constrains`: Validates data
- `@api.onchange`: Triggered when field value changes

### Q24: How do you create custom methods and call them from views?
**Answer**:
```python
def action_approve(self):
    self.write({'status': 'approved'})
    return True

# In view:
<button name="action_approve" type="object" string="Approve"/>
```

### Q25: What are constraints and how are they used?
**Answer**:
```python
@api.constrains('email')
def _check_email_format(self):
    for record in self:
        if record.email and '@' not in record.email:
            raise ValidationError('Invalid email!')

_sql_constraints = [
    ('email_unique', 'UNIQUE(email)', 'Email must be unique!')
]
```

---

## Common Scenarios

### Q26: How do you handle onchange in forms?
**Answer**:
```python
@api.onchange('department_id')
def _onchange_department(self):
    if self.department_id:
        self.department_name = self.department_id.name
        # Return warning
        return {'warning': {'title': 'Warning', 'message': 'Changed department'}}
```

### Q27: How do you create and manage relationships between models?
**Answer**:
```python
# Many2one - Student belongs to Department
department_id = fields.Many2one('hr.department', string='Department')

# One2many - Department has many Students
student_ids = fields.One2many('student.student', 'department_id', string='Students')

# Many2many - Students take many Courses, Courses have many Students
course_ids = fields.Many2many('course.course', string='Courses')
```

### Q28: How do you test Odoo modules?
**Answer**:
```python
from odoo.tests.common import TransactionCase

class StudentTestCase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.student = self.env['student.student'].create({
            'name': 'Test'
        })
    
    def test_create_student(self):
        self.assertEqual(self.student.name, 'Test')
```

---

## Behavioral Questions

### Q29: Describe a complex module you've built.
**Answer**: Structure response:
- Module purpose and scope
- Models created and relationships
- Views implemented
- Security model
- Challenges faced and solutions
- Results and learning

### Q30: How do you approach debugging issues in Odoo?
**Answer**:
- Check Odoo logs
- Enable debug mode
- Use Python debugger
- Test in PostgreSQL directly
- Check XML for syntax errors
- Verify access rights
- Check browser console for JavaScript errors
- Isolate the problem systematically

---

## Tips for Interview

1. **Be specific**: Use code examples
2. **Know fundamentals**: Master ORM, Models, Views, Security
3. **Practice**: Write actual code, test it
4. **Understand flow**: Know how requests are processed
5. **Real-world examples**: Prepare examples from your experience
6. **Ask clarifying questions**: Don't assume requirements
7. **Stay updated**: Odoo versions differ, mention which version you know
8. **Showcase learning**: Mention resources and communities you follow

---

Good luck with your interviews! 🚀
