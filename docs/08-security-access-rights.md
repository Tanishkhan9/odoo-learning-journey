# Security & Access Rights

## Odoo Security Model

Odoo has multiple layers of security:

1. **Authentication**: User login verification
2. **Access Rights (ACL)**: Model-level permissions
3. **Record Rules (RLS)**: Row-level permissions
4. **Field Access**: Column-level permissions

## Access Rights (ir.model.access)

### CSV Format

Access rights are defined in `security/ir.model.access.csv`:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_student_manager,Student Manager,model_student_student,group_student_manager,1,1,1,1
access_student_user,Student User,model_student_student,group_student_user,1,0,0,0
```

### Meaning of Permissions

| Permission | Meaning | Value |
|-----------|---------|-------|
| `perm_read` | Can view records | 1/0 |
| `perm_write` | Can edit records | 1/0 |
| `perm_create` | Can create records | 1/0 |
| `perm_unlink` | Can delete records | 1/0 |

## Defining Groups

### In __manifest__.py

```python
{
    'name': 'Student Management',
    'version': '1.0',
    'category': 'Education',
    'sequence': 1,
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/student_groups.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/student_views.xml',
    ],
}
```

### In security/student_groups.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Define Groups -->
        <record id="group_student_user" model="res.groups">
            <field name="name">Student User</field>
            <field name="category_id" ref="base.module_category_services"/>
            <field name="comment">Can view student records</field>
        </record>
        
        <record id="group_student_manager" model="res.groups">
            <field name="name">Student Manager</field>
            <field name="category_id" ref="base.module_category_services"/>
            <field name="comment">Can manage student records</field>
            <!-- Inherit from user group -->
            <field name="implied_ids" eval="[(4, ref('group_student_user'))]"/>
        </record>
        
        <!-- Add users to groups -->
        <record id="base.user_admin" model="res.users">
            <field name="groups_id" eval="[(4, ref('group_student_manager'))]"/>
        </record>
        
    </data>
</odoo>
```

## Record Rules (Row-Level Security)

Control which records users can access based on conditions.

### Record Rule Definition

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Rule 1: Managers see all records -->
        <record id="rule_student_manager_all" model="ir.rule">
            <field name="name">Student Manager - All</field>
            <field name="model_id" ref="model_student_student"/>
            <field name="groups" eval="[(4, ref('group_student_manager'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="True"/>
            <field name="domain_force">[(1, '=', 1)]</field> <!-- All records -->
        </record>
        
        <!-- Rule 2: Users see only active students -->
        <record id="rule_student_user_active" model="ir.rule">
            <field name="name">Student User - Active Only</field>
            <field name="model_id" ref="model_student_student"/>
            <field name="groups" eval="[(4, ref('group_student_user'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
            <field name="domain_force">[('status', '=', 'active')]</field>
        </record>
        
    </data>
</odoo>
```

## Field-Level Access

Control field visibility per group.

### In Model Definition

```python
from odoo import models, fields

class Student(models.Model):
    _name = 'student.student'
    
    name = fields.Char('Name')
    
    # Only managers can see salary
    salary = fields.Float(
        'Salary',
        groups='student_management.group_student_manager'
    )
    
    # Only admins can edit
    sensitive_data = fields.Char(
        'Sensitive Data',
        readonly=True,
        groups='base.group_system'
    )
```

## Security in Python Code

### Check Permissions

```python
def create(self, vals):
    # Check if user has create permission
    if not self.env.user.has_group('student_management.group_student_manager'):
        raise AccessDenied('Only managers can create students!')
    return super().create(vals)
```

### Check Group Membership

```python
def action_approve(self):
    user = self.env.user
    
    if user.has_group('student_management.group_student_manager'):
        # Allow managers
        return self.write({'status': 'approved'})
    else:
        raise AccessDenied('Only managers can approve!')
```

### Sudo for Special Operations

```python
def process_with_admin_rights(self):
    # Execute as superuser (admin)
    admin_context = self.env['student.student'].sudo()
    admin_context.write({'processed': True})

def process_without_groups(self):
    # Execute bypassing group checks
    self.sudo().write({'internal_field': True})
```

## Best Practices

### 1. Principle of Least Privilege
```python
# ❌ Bad: Everyone is a manager
perm_read=1, perm_write=1, perm_create=1, perm_unlink=1

# ✅ Good: Specific roles with limited permissions
# Managers: All permissions
# Users: Read only
# Guests: No access
```

### 2. Clear Group Naming
```xml
<!-- ✅ Good naming -->
<record id="group_student_manager" model="res.groups">
    <field name="name">Student Manager</field>
</record>

<!-- ❌ Bad naming -->
<record id="group_admin" model="res.groups">
    <field name="name">Admin</field>
</record>
```

### 3. Document Security Model
```python
class Student(models.Model):
    """
    Security Model:
    - Managers: Full access
    - Users: Read-only access to active students
    - Guests: No access
    """
    _name = 'student.student'
```

### 4. Use Record Rules with Domains
```xml
<!-- Allow users to see records they created -->
<record id="rule_student_own_records" model="ir.rule">
    <field name="domain_force">[('create_uid', '=', user.id)]</field>
</record>
```

## Common Record Rule Patterns

### Access by User
```python
# Records created by current user
[('create_uid', '=', user.id)]

# Records assigned to current user
[('assigned_to', '=', user.id)]
```

### Access by Department
```python
# Records in user's department
[('department_id', '=', user.employee_id.department_id.id)]
```

### Access by Status
```python
# Only published records
[('status', '=', 'published')]

# Active records only
[('active', '=', True)]
```

### Complex Rules
```python
# User's own records OR assigned to user's group
['|',
    ('create_uid', '=', user.id),
    ('group_id', 'in', user.groups_id.ids)
]
```

## Testing Security

```python
def test_student_manager_full_access(self):
    manager = self.env['res.users'].create({
        'name': 'Manager',
        'login': 'manager@test.com',
        'groups_id': [(4, self.env.ref('student_management.group_student_manager').id)]
    })
    
    student = self.env['student.student'].with_user(manager).create({
        'name': 'Test Student'
    })
    
    self.assertTrue(student)

def test_student_user_read_only(self):
    user = self.env['res.users'].create({
        'name': 'User',
        'login': 'user@test.com',
        'groups_id': [(4, self.env.ref('student_management.group_student_user').id)]
    })
    
    student = self.env['student.student'].create({'name': 'Test'})
    
    # Can read
    self.assertTrue(self.env['student.student'].with_user(user).search([('id', '=', student.id)]))
    
    # Cannot write
    with self.assertRaises(AccessError):
        student.with_user(user).write({'name': 'Updated'})
```

## Security Checklist

- ✅ Define groups for different roles
- ✅ Set appropriate access rights per model
- ✅ Use record rules for row-level security
- ✅ Apply field-level access for sensitive data
- ✅ Test security rules thoroughly
- ✅ Document security model in code
- ✅ Use sudo() only when necessary
- ✅ Validate permissions in critical methods

---

Next: [Common Errors and Fixes](09-common-errors-and-fixes.md)
