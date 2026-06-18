# Models, Views & Actions

## Introduction

The MVA (Models-Views-Actions) pattern is the core architecture of Odoo development:

- **Models**: Define business logic and data structure
- **Views**: Define user interface representation
- **Actions**: Link models and views together

## Models

### Creating a Model

```python
# student.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Management'
    _rec_name = 'name'
    
    # Fields
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    registration_number = fields.Char(string='Registration #', unique=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    status = fields.Selection([
        ('new', 'New'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated')
    ], string='Status', default='new')
    
    # Relational fields
    department_id = fields.Many2one('hr.department', string='Department')
    course_ids = fields.Many2many('course.course', string='Courses')
    
    # Other fields
    notes = fields.Text(string='Notes')
    created_date = fields.Datetime(string='Created', default=lambda self: fields.Datetime.now())
    
    # Constraints
    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'Email must be unique!'),
    ]
    
    # Compute methods
    @api.depends('birth_date')
    def _compute_age(self):
        from datetime import date
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year
    
    # Validation
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError('Invalid email format!')
    
    # Custom methods
    def action_activate(self):
        self.write({'status': 'active'})
        return True
    
    def get_enrollment_count(self):
        return len(self.course_ids)
```

## Views

### Form View

```xml
<!-- student_views.xml -->
<form string="Student">
    <sheet>
        <group>
            <group>
                <field name="name" required="1"/>
                <field name="email" widget="email"/>
                <field name="registration_number"/>
            </group>
            <group>
                <field name="birth_date"/>
                <field name="age"/>
                <field name="status" widget="radio"/>
            </group>
        </group>
        
        <notebook>
            <page string="General">
                <field name="department_id"/>
                <field name="notes"/>
            </page>
            <page string="Courses">
                <field name="course_ids" widget="many2many_tags"/>
            </page>
        </notebook>
    </sheet>
    
    <footer>
        <button name="action_activate" type="object" string="Activate" class="btn btn-primary"/>
        <button string="Cancel" special="cancel" class="btn btn-secondary"/>
    </footer>
</form>
```

### List View

```xml
<tree string="Students">
    <field name="name"/>
    <field name="email"/>
    <field name="registration_number"/>
    <field name="birth_date"/>
    <field name="age"/>
    <field name="status"/>
    <field name="department_id"/>
</tree>
```

### Search View

```xml
<search string="Search Students">
    <field name="name"/>
    <field name="email"/>
    <field name="registration_number"/>
    
    <filter string="Active" name="active_students" domain="[('status', '=', 'active')]"/>
    <filter string="New" name="new_students" domain="[('status', '=', 'new')]"/>
    <filter string="Graduated" name="graduated" domain="[('status', '=', 'graduated')]"/>
    
    <separator/>
    <filter string="My Department" name="my_department" domain="[('department_id', '=', uid)]"/>
    
    <group expand="1" string="Group By">
        <filter string="Status" name="group_by_status" context="{'group_by': 'status'}"/>
        <filter string="Department" name="group_by_department" context="{'group_by': 'department_id'}"/>
    </group>
</search>
```

### Kanban View

```xml
<kanban>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_card">
                <div class="oe_kanban_content">
                    <h4><field name="name"/></h4>
                    <p><strong>Email:</strong> <field name="email"/></p>
                    <p><strong>Status:</strong> <field name="status"/></p>
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

## Actions

### Window Action

```xml
<action id="action_student_list" name="Students" type="ir.actions.act_window">
    <field name="res_model">student.student</field>
    <field name="view_mode">tree,form</field>
    <field name="view_type">form</field>
    <field name="help">Create and manage students</field>
</action>
```

### Server Action

```xml
<action id="action_mass_activate" name="Mass Activate" type="ir.actions.server">
    <field name="model_id" ref="model_student_student"/>
    <field name="binding_model_id" ref="model_student_student"/>
    <field name="state">code</field>
    <field name="code">
action = records.action_activate()
    </field>
</action>
```

### URL Action

```xml
<action id="action_open_students" name="Open Students" type="ir.actions.act_url">
    <field name="url">http://example.com/students</field>
</action>
```

## Menu Definition

```xml
<!-- menu.xml -->
<menuitem id="menu_student_root" name="Student Management" web_icon="student_management,static/description/icon.png"/>

<menuitem id="menu_student_list" 
    name="Students" 
    parent="menu_student_root"
    action="action_student_list"
    sequence="1"/>

<menuitem id="menu_reports" 
    name="Reports" 
    parent="menu_student_root"
    sequence="2"/>

<menuitem id="menu_config" 
    name="Configuration" 
    parent="menu_student_root"
    sequence="10"/>
```

## View Widgets

### Common Widgets

```xml
<!-- Text widget -->
<field name="name" widget="text"/>

<!-- Email widget -->
<field name="email" widget="email"/>

<!-- URL widget -->
<field name="website" widget="url"/>

<!-- Many2many tags -->
<field name="tags" widget="many2many_tags"/>

<!-- Binary image -->
<field name="image" widget="image"/>

<!-- Progress bar -->
<field name="progress" widget="progressbar"/>

<!-- Radio buttons -->
<field name="status" widget="radio"/>

<!-- Selection dropdown -->
<field name="status" widget="selection"/>
```

## Form Widgets

```xml
<form>
    <!-- Header section -->
    <header>
        <button name="action_activate" type="object" string="Activate" class="btn btn-primary"/>
        <button name="action_deactivate" type="object" string="Deactivate"/>
        <field name="status" widget="statusbar" options="{'clickable': True}"/>
    </header>
    
    <!-- Sheet for content -->
    <sheet>
        <!-- Groups -->
        <group>
            <group col="2">
                <field name="name"/>
                <field name="email"/>
            </group>
            <group col="2">
                <field name="birth_date"/>
                <field name="age"/>
            </group>
        </group>
        
        <!-- Tabs -->
        <notebook>
            <page string="General">
                <field name="notes"/>
            </page>
            <page string="Courses">
                <field name="course_ids"/>
            </page>
        </notebook>
    </sheet>
    
    <!-- Footer -->
    <footer>
        <button string="Save" type="object" class="btn btn-primary"/>
        <button string="Cancel" special="cancel" class="btn btn-secondary"/>
    </footer>
</form>
```

## Tips & Best Practices

1. **Naming Conventions**
   - Model: `snake_case` (student_student)
   - View: descriptive with `_views` suffix
   - Action: `action_` prefix

2. **View Inheritance**
   - Use inheritance to extend existing views
   - Avoids overwriting original code

3. **Domain Syntax**
   - Use domain filters in actions
   - Format: `[('field', 'operator', 'value')]`

4. **Button Types**
   - `type="object"`: Call Python method
   - `type="action"`: Execute action
   - `type="server"`: Run server action

5. **Performance**
   - Use appropriate view types
   - Optimize list view with search filters
   - Use computed fields wisely

---

Next: [Security & Access Rights](08-security-access-rights.md)
