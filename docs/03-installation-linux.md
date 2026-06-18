# Installation on Linux

## Step 1: Update System Packages

```bash
sudo apt update
sudo apt upgrade -y
```

## Step 2: Install Python and Dependencies

```bash
sudo apt install python3 python3-pip python3-dev python3-venv git -y
```

### Verify Python Installation
```bash
python3 --version
pip3 --version
```

## Step 3: Install PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

## Step 4: Create PostgreSQL Database and User

```bash
# Connect to PostgreSQL as default user
sudo -u postgres psql

# Inside psql prompt, run:
CREATE DATABASE odoo_learning;
CREATE USER odoo_user WITH PASSWORD 'your_password';
ALTER ROLE odoo_user SET client_encoding TO 'utf8';
ALTER ROLE odoo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE odoo_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE odoo_learning TO odoo_user;
\q
```

## Step 5: Install Required System Libraries

```bash
sudo apt install libpq-dev python3-dev -y

# For certain Odoo features
sudo apt install npm node-less -y
```

## Step 6: Create Python Virtual Environment

```bash
# Navigate to your project directory
cd ~/Desktop

# Create virtual environment
python3 -m venv odoo_env

# Activate virtual environment
source odoo_env/bin/activate
```

## Step 7: Clone and Setup Odoo Learning Journey

```bash
git clone https://github.com/Tanishkhan9/odoo-learning-journey.git
cd odoo-learning-journey

# Install Python dependencies
pip install -r requirements.txt
```

## Step 8: Configure Odoo

Create a configuration file `odoo.conf`:

```bash
cat > odoo.conf << EOF
[options]
addons_path = ./modules
db_host = localhost
db_port = 5432
db_user = odoo_user
db_password = your_password
db_name = odoo_learning
admin_passwd = admin
logfile = ./odoo.log
EOF
```

## Step 9: Start Odoo Server

With your virtual environment activated:

```bash
python -m odoo --config odoo.conf
```

Access Odoo at: http://localhost:8069

## Troubleshooting

### Issue: Permission denied on PostgreSQL
**Solution**: Ensure user has proper permissions:
```bash
sudo usermod -a -G postgres your_username
```

### Issue: psycopg2 installation fails
**Solution**:
```bash
pip install psycopg2-binary
```

### Issue: Port 8069 already in use
**Solution**: Use a different port:
```bash
python -m odoo --config odoo.conf --http-port 8070
```

### Issue: ModuleNotFoundError
**Solution**: Ensure virtual environment is activated:
```bash
source odoo_env/bin/activate
```

## Next Steps

- [Odoo Introduction](04-odoo-introduction.md)
- [Learning Roadmap](11-learning-roadmap.md)
