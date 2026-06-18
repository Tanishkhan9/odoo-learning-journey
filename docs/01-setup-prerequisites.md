# Setup Prerequisites

## System Requirements

Before installing Odoo, ensure your system meets the following requirements:

### Minimum Requirements

- **OS**: Windows 10/11, Ubuntu 20.04 LTS, or macOS 10.15+
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 10 GB free space minimum
- **Processor**: 2-core processor minimum

### Software Requirements

#### Python
- **Version**: Python 3.8 or higher
- **Download**: https://www.python.org/downloads/
- **Verification**: `python --version`

#### PostgreSQL
- **Version**: PostgreSQL 12 or higher
- **Download**: https://www.postgresql.org/download/
- **Verification**: `psql --version`

#### Git
- **Version**: Git 2.25 or higher
- **Download**: https://git-scm.com/download/
- **Verification**: `git --version`

### Development Tools

- **Text Editor/IDE**: 
  - Visual Studio Code (recommended)
  - PyCharm
  - Sublime Text

- **Version Control**: Git (already listed above)

## Environment Setup

### Windows Users
1. Install Python from python.org
2. During installation, check "Add Python to PATH"
3. Install PostgreSQL and note the password
4. Install Git from git-scm.com

### Linux Users (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-dev
sudo apt install postgresql postgresql-contrib
sudo apt install git
```

### macOS Users
```bash
# Using Homebrew
brew install python@3.10
brew install postgresql
brew install git
```

## Verification Checklist

Run these commands in your terminal:

```bash
python --version          # Should be 3.8+
pip --version            # Should be present
psql --version           # Should be 12+
git --version            # Should be present
```

If all commands return versions, you're ready to proceed with installation!

## Next Steps

- [Installation on Windows](02-installation-windows.md)
- [Installation on Linux](03-installation-linux.md)
