# Common Errors and Fixes

## Module Installation Errors

### Error: "ImportError: No module named 'odoo'"

**Cause**: Odoo is not installed in your Python environment.

**Solution**:
```bash
pip install -r requirements.txt
# or specifically
pip install odoo==16.0.1.0
```

### Error: "psycopg2 not installed"

**Cause**: PostgreSQL adapter for Python is missing.

**Solution**:
```bash
pip install psycopg2-binary
```

---

## Database Errors

### Error: "could not connect to server: Connection refused"

**Cause**: PostgreSQL server is not running.

**Solution (Windows)**:
- Start PostgreSQL service from Services app
- Or: `net start postgresql-x64-12`

**Solution (Linux)**:
```bash
sudo service postgresql start
# or
sudo systemctl start postgresql
```

### Error: "FATAL: database does not exist"

**Cause**: Database specified in config doesn't exist.

**Solution**:
```bash
# Create database as postgres user
sudo -u postgres psql
CREATE DATABASE odoo_learning;
```

### Error: "role 'odoo_user' does not exist"

**Cause**: Database user is not created.

**Solution**:
```bash
sudo -u postgres psql
CREATE USER odoo_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE odoo_learning TO odoo_user;
```

---

## Module Structure Errors

### Error: "ValueError: External ID not found: 'model_student_student'"

**Cause**: Referenced model doesn't exist or has wrong name.

**Solution**: Check in `ir.model.access.csv`:
- Model name must match exactly: `model_student_student`
- Underscore replaces dots in model name
- If model is `student.student`, ID is `model_student_student`

### Error: "No menu item found with id 'menu_student_root'"

**Cause**: Referenced menu ID doesn't exist.

**Solution**: Define menu first in `menu.xml`:
```xml
<menuitem id="menu_student_root" name="Student Management"/>
```

### Error: "Key Error: 'student_groups.xml' does not exist"

**Cause**: File referenced in `__manifest__.py` is missing.

**Solution**: Ensure file path is correct:
```python
'data': [
    'security/student_groups.xml',  # File must exist
    'security/ir.model.access.csv',
    'views/menu.xml',
]
```

---

## Model Definition Errors

### Error: "AttributeError: 'student.student' object has no attribute 'name'"

**Cause**: Field is not defined in model or computed but not stored.

**Solution**: Define the field:
```python
name = fields.Char(string='Name', required=True)
```

Or if it's computed, add `store=True`:
```python
full_name = fields.Char(
    string='Full Name',
    compute='_compute_full_name',
    store=True  # Add this to persist computed value
)
```

### Error: "TypeError: _compute_method() missing required positional argument"

**Cause**: Compute method has wrong signature.

**Solution**: Compute methods should accept `self`:
```python
# ❌ Wrong
def _compute_age():
    pass

# ✅ Correct
def _compute_age(self):
    for record in self:
        record.age = calculate_age()
```

### Error: "IntegrityError: duplicate key violates unique constraint"

**Cause**: Trying to insert duplicate value in unique field.

**Solution**: Check for existing records:
```python
existing = self.env['student.student'].search([('email', '=', 'test@example.com')])
if not existing:
    self.env['student.student'].create({'email': 'test@example.com'})
```

---

## View and Action Errors

### Error: "QWebException: 'field_name' is not defined"

**Cause**: Referenced field doesn't exist in model.

**Solution**: Verify field name matches exactly:
```xml
<!-- ✅ Correct -->
<field name="email"/>

<!-- ❌ Wrong (field doesn't exist) -->
<field name="email_address"/>
```

### Error: "ValueError: Invalid view XML"

**Cause**: Malformed XML syntax.

**Solution**: Check XML structure:
```xml
<!-- ❌ Wrong: Missing closing tag -->
<form string="Student">
    <field name="name"/>
</form>

<!-- ✅ Correct -->
<form string="Student">
    <field name="name"/>
</form>
```

### Error: "No action found"

**Cause**: Action defined but not linked to menu.

**Solution**: Reference action in menu:
```xml
<menuitem id="menu_student" 
    name="Students" 
    action="action_student_list"/>
```

---

## Inheritance Errors

### Error: "ValueError: Model inheritance"

**Cause**: Circular dependency or wrong inheritance setup.

**Solution**: Check inheritance chain:
```python
# ❌ Wrong: Circular inheritance
class Model1(models.Model):
    _inherit = 'model.2'

class Model2(models.Model):
    _inherit = 'model.1'

# ✅ Correct: Linear chain
class Model2Extended(models.Model):
    _inherit = 'model.2'
```

---

## Permission and Security Errors

### Error: "AccessError: Access denied"

**Cause**: User doesn't have permission for operation.

**Solution**: 
1. Check access rights in `ir.model.access.csv`
2. Verify user is in correct group
3. Check record rules

```xml
<!-- Example: Give user read permission -->
<record id="access_student_user" model="ir.model.access">
    <field name="name">Student User</field>
    <field name="model_id" ref="model_student_student"/>
    <field name="group_id" ref="group_student_user"/>
    <field name="perm_read">1</field>
</record>
```

### Error: "ValidateError: The following restrictions apply"

**Cause**: Record rule prevents access.

**Solution**: Update record rule domain or add user to appropriate group.

---

## API and Method Errors

### Error: "TypeError: unbound method method_name() takes 1 positional argument but 2 were given"

**Cause**: Missing `@api` decorator or wrong method signature.

**Solution**:
```python
# ❌ Wrong
def action_approve(self):
    pass

# ✅ Correct with decorator
@api.multi  # if multiple records
def action_approve(self):
    for record in self:
        record.write({'status': 'approved'})

# OR modern approach (no decorator needed)
def action_approve(self):
    self.write({'status': 'approved'})
```

### Error: "RecursionError: maximum recursion depth exceeded"

**Cause**: Method calling itself indefinitely, usually in onchange.

**Solution**: Add condition to prevent recursion:
```python
@api.onchange('name')
def _onchange_name(self):
    if self.name and 'auto' not in self._context:
        # Prevent recursive call
        self = self.with_context(auto=True)
        # ... process
```

---

## Performance Issues

### Symptom: "Module loading is very slow"

**Cause**: Database queries in module initialization.

**Solution**: Move queries to methods:
```python
# ❌ Avoid: Query during import
students = env['student.student'].search([])

# ✅ Good: Query in method
def get_students(self):
    return self.env['student.student'].search([])
```

### Symptom: "Form loads slowly with many records"

**Cause**: Loading all records in One2many field.

**Solution**: Use domain and limit:
```xml
<field name="course_ids" domain="[('active', '=', True)]" options="{'limit': 50}"/>
```

---

## Debugging Tips

### 1. Enable Debug Mode
```bash
python -m odoo --debug --config odoo.conf
```

### 2. Check Logs
```bash
tail -f odoo.log
```

### 3. Python Debugging
```python
import logging
logger = logging.getLogger(__name__)

def my_method(self):
    logger.info('Debug message: %s', self.name)
```

### 4. Use print() in Console
```python
def my_method(self):
    print(f"Debug: {self.name}")  # Will appear in terminal
```

### 5. PostgreSQL Query Logs
```bash
# In psql:
SET log_statement = 'all';
```

---

## Quick Reference Checklist

Before deploying, verify:

- ✅ Module structure is correct
- ✅ All files referenced in `__manifest__.py` exist
- ✅ Database connection works
- ✅ Access rights are defined
- ✅ XML views are well-formed
- ✅ Fields in views match model definition
- ✅ No circular dependencies
- ✅ Required fields have default values
- ✅ Module can be installed without errors
- ✅ Tests pass successfully

---

Next: [Interview Questions](10-interview-questions.md)
