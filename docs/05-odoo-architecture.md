# Odoo Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│          Browser / Web Client                    │
│  (HTML, CSS, JavaScript, QWeb Templates)        │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
    HTTP/REST                  WebSocket
        │                         │
┌───────▼──────────────────────────▼──────────────┐
│         Odoo Server (Python)                     │
│                                                   │
│  ┌──────────────────────────────────────────┐  │
│  │  Application Layer (Models, Views)       │  │
│  │  • Models (ORM objects)                  │  │
│  │  • Views (Form, List, Calendar, etc.)   │  │
│  │  • Controllers (Routes)                 │  │
│  └──────────────────────────────────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐  │
│  │  Business Logic Layer                    │  │
│  │  • Workflows                             │  │
│  │  • Validations                           │  │
│  │  • Computations                          │  │
│  └──────────────────────────────────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐  │
│  │  ORM Layer                               │  │
│  │  • Database abstraction                  │  │
│  │  • Query building                        │  │
│  │  • Field types                           │  │
│  └──────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────┘
                     │
                  SQL Queries
                     │
┌────────────────────▼────────────────────────────┐
│       PostgreSQL Database                        │
│  • Tables (Models)                               │
│  • Relations                                     │
│  • Indexes                                       │
└──────────────────────────────────────────────────┘
```

## Components Explained

### 1. Web Client (Frontend)
- User interface built with HTML, CSS, and JavaScript
- QWeb: Odoo's templating language (similar to Jinja2)
- Handles:
  - Form displays
  - Data validation
  - User interactions
  - Real-time updates

### 2. Odoo Server (Backend)
Written entirely in Python, handles:
- Request processing
- Business logic execution
- Data management
- Authorization and security

### 3. ORM (Object-Relational Mapping)
- Maps Python classes to database tables
- Provides a Pythonic interface to the database
- No need to write raw SQL
- Example:
  ```python
  # Instead of: SELECT * FROM res_partner WHERE name='John'
  partners = self.env['res.partner'].search([('name', '=', 'John')])
  ```

### 4. Database Layer
- PostgreSQL stores all data
- Relational structure with foreign keys
- ACID transactions

## Module Structure

Each Odoo module (addon) typically contains:

```
my_module/
├── __init__.py              # Python initialization
├── __manifest__.py          # Module metadata
├── models/
│   ├── __init__.py
│   └── my_model.py          # Business logic
├── views/
│   ├── my_model_views.xml   # UI Definitions
│   └── menu.xml             # Menu structure
├── security/
│   └── ir.model.access.csv  # Access rights
├── data/
│   └── data.xml             # Demo/default data
├── reports/
│   └── report_template.xml  # Report layouts
├── static/
│   ├── description/
│   │   └── index.html       # Module icon/description
│   └── src/
│       └── css/js files
└── tests/
    └── test_models.py       # Unit tests
```

## Request-Response Flow

```
1. User clicks button in browser
   │
2. JavaScript sends HTTP request to Odoo server
   │
3. Odoo controller receives request
   │
4. Controller calls model methods
   │
5. Model executes business logic
   │
6. ORM translates to SQL and queries database
   │
7. PostgreSQL returns data
   │
8. Model processes data
   │
9. Controller formats response (JSON/HTML)
   │
10. Browser receives response
    │
11. UI updates/renders
```

## Key Concepts

### Models
Python classes representing business objects:
```python
class Student(models.Model):
    _name = 'student.student'
    name = fields.Char('Name')
    email = fields.Char('Email')
```

### Views
XML definitions of user interface:
```xml
<form>
    <field name="name"/>
    <field name="email"/>
</form>
```

### Actions
Links between models and views:
```xml
<action name="Open Students" model="student.student" type="ir.actions.act_window"/>
```

### Modules/Addons
Packaged functionality that can be installed/uninstalled

### Inheritance
- **Classical Inheritance**: Extend existing models
- **Delegation Inheritance**: Link to parent model
- **Mixins**: Reusable functionality

## Data Flow

```
User Input → Browser → HTTP → Odoo Server → Python → ORM → SQL → Database
                                                     ↑           ↑
                                                 Processing   Storage

Database Response → SQL Result → ORM Objects → Python Processing → JSON → HTTP → Browser → Render
```

## Security Layers

1. **Authentication**: User login/session
2. **Authorization**: Access rules (ACL)
3. **Row-level Security**: Record rules
4. **Field-level Security**: Field access control

## Scalability Architecture

### Single Server (Development)
```
Browser → Odoo Server → PostgreSQL
```

### Multi-Server (Production)
```
Load Balancer
    ↙    ↓    ↘
Odoo1  Odoo2  Odoo3
    ↘    ↓    ↙
PostgreSQL (with replication)
```

## Performance Considerations

1. **Caching**: Browser caching, server-side caching
2. **Database Indexing**: Speed up queries
3. **Lazy Loading**: Load data when needed
4. **Batch Operations**: Reduce database calls

---

Next: Learn about [ORM Fundamentals](06-orm-cheatsheet.md)
