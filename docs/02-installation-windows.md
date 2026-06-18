# Installation on Windows

## Step 1: Install Python

1. Download Python 3.10+ from https://www.python.org/downloads/
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation: Open PowerShell and run:
   ```bash
   python --version
   pip --version
   ```

## Step 2: Install PostgreSQL

1. Download from https://www.postgresql.org/download/windows/
2. Run the installer
3. Choose installation directory (default is fine)
4. Set a password for the `postgres` user (remember this!)
5. Keep port as 5432 (default)
6. Complete installation

### Verify PostgreSQL
```bash
psql --version
psql -U postgres -h localhost
```

## Step 3: Install Git

1. Download from https://git-scm.com/download/win
2. Run the installer
3. Use default settings
4. Verify: `git --version`

## Step 4: Create Python Virtual Environment

Open PowerShell and navigate to your project folder:

```bash
# Navigate to your desired directory
cd C:\Users\YourUsername\Desktop

# Create virtual environment
python -m venv odoo_env

# Activate virtual environment
.\odoo_env\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 5: Clone and Setup Odoo Learning Journey

```bash
# Clone the repository
git clone https://github.com/Tanishkhan9/odoo-learning-journey.git
cd odoo-learning-journey

# Install dependencies
pip install -r requirements.txt
```

## Step 6: Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# In the psql prompt, create a new database:
CREATE DATABASE odoo_learning;
CREATE USER odoo_user WITH PASSWORD 'your_password';
ALTER ROLE odoo_user SET client_encoding TO 'utf8';
ALTER ROLE odoo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE odoo_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE odoo_learning TO odoo_user;
\q
```

## Step 7: Configure Odoo

Create a configuration file `odoo.conf`:

```ini
[options]
addons_path = ./modules
db_host = localhost
db_port = 5432
db_user = odoo_user
db_password = your_password
db_name = odoo_learning
admin_passwd = admin
```

## Step 8: Start Odoo Server

With your virtual environment activated:

```bash
python -m odoo --config odoo.conf
```

Access Odoo at: http://localhost:8069

## Troubleshooting

### Issue: psycopg2 installation fails
**Solution**:
```bash
pip install psycopg2-binary
```

### Issue: Permission denied on Activate.ps1
**Solution**: Run PowerShell as Administrator and execute:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: PostgreSQL connection refused
**Solution**: Ensure PostgreSQL service is running:
```bash
# Check services or restart PostgreSQL via Services app
```

## Next Steps

- [Odoo Introduction](04-odoo-introduction.md)
- [Learning Roadmap](11-learning-roadmap.md)
