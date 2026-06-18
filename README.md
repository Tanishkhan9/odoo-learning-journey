# Odoo Learning Journey

A comprehensive guide and practical implementation for learning Odoo development from scratch.

## 📚 Project Overview

This project contains:
- Complete documentation covering Odoo fundamentals
- Practical examples and best practices
- A functional `student_management` module
- Interview preparation resources
- Step-by-step installation guides

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Tanishkhan9/odoo-learning-journey.git
   cd odoo-learning-journey
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Database**
   - Create a PostgreSQL database
   - Configure Odoo with your database credentials

4. **Install the Module**
   - Place the `student_management` module in your Odoo addons path
   - Update app list and install the module

## 📖 Documentation

### Getting Started
- [01 - Setup Prerequisites](docs/01-setup-prerequisites.md)
- [02 - Installation on Windows](docs/02-installation-windows.md)
- [03 - Installation on Linux](docs/03-installation-linux.md)

### Core Concepts
- [04 - Odoo Introduction](docs/04-odoo-introduction.md)
- [05 - Odoo Architecture](docs/05-odoo-architecture.md)
- [06 - ORM Cheatsheet](docs/06-orm-cheatsheet.md)
- [07 - Models, Views & Actions](docs/07-models-views-actions.md)
- [08 - Security & Access Rights](docs/08-security-access-rights.md)

### Resources
- [09 - Common Errors and Fixes](docs/09-common-errors-and-fixes.md)
- [10 - Interview Questions](docs/10-interview-questions.md)
- [11 - Learning Roadmap](docs/11-learning-roadmap.md)

## 📁 Project Structure

```
odoo-learning-journey/
├── docs/                          # Documentation files
├── modules/
│   └── student_management/        # Example Odoo module
│       ├── models/                # Business logic
│       ├── views/                 # UI definitions
│       ├── security/              # Access controls
│       ├── data/                  # Sample data
│       ├── static/                # Static assets
│       └── __manifest__.py        # Module metadata
└── tests/                         # Unit tests
```

## 🎯 Learning Roadmap

1. **Week 1-2**: Setup & Installation
2. **Week 3-4**: Odoo Architecture & ORM Concepts
3. **Week 5-6**: Models, Views & Actions
4. **Week 7-8**: Security & Advanced Topics
5. **Week 9-10**: Building Practical Projects

## 🧪 Testing

Run tests using:
```bash
python -m pytest tests/
```

## 🔧 Requirements

See `requirements.txt` for all dependencies.

## 📝 License

This project is for educational purposes.

## 👤 Author

Tanishk Khan

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

---

Happy learning! 🎉