# Contact Management System - Setup & Configuration Guide

## System Requirements

### Minimum Requirements
- **OS:** Windows, macOS, or Linux
- **Python:** 3.6 or higher
- **RAM:** 50 MB minimum
- **Disk Space:** 1 MB minimum
- **Terminal/Command Prompt:** Any standard terminal

### Recommended Requirements
- **Python:** 3.8 or higher
- **RAM:** 512 MB or more
- **Disk Space:** 10+ MB (for future expansion)

## Installation Methods

### Method 1: Direct Download (Easiest)

1. Download `contact_management_system.py`
2. Save to your desired location
3. Open terminal/command prompt in that folder
4. Run: `python contact_management_system.py`

### Method 2: Clone from Repository

```bash
# If using Git
git clone https://github.com/yourusername/contact-management.git
cd contact-management
python contact_management_system.py
```

### Method 3: Create Virtual Environment (Recommended for Development)

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Run application
python contact_management_system.py
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Run application
python contact_management_system.py
```

## Configuration

### Data Storage Location

By default, contacts are saved to `contacts.json` in the same directory as the script.

**To change storage location:**

```python
# In contact_management_system.py, line ~1175:
manager = ContactManager("contacts.json")  # Change filename

# Example: Store in specific folder
manager = ContactManager("./data/contacts.json")
```

### File Location Examples

**Windows:**
```
C:\Users\YourName\Documents\contacts.json
C:\projects\contact_manager\contacts.json
```

**macOS/Linux:**
```
/Users/username/Documents/contacts.json
~/contact_management/contacts.json
```

### Validation Settings

#### Phone Number Validation

**Current Settings:**
- Minimum length: 10 digits
- Maximum length: 15 digits
- Allows spaces and hyphens

**To modify:**

```python
@staticmethod
def validate_phone(phone):
    """Customize validation here"""
    cleaned = phone.replace(" ", "").replace("-", "")
    
    # For US-only: min 10, max 10
    if re.match(r'^\d{10}$', cleaned):
        return True
    
    # For international: min 7, max 15
    # if re.match(r'^\d{7,15}$', cleaned):
    #     return True
    
    return False
```

#### Email Validation

**Current Settings:**
- Standard email format: `user@domain.extension`
- Domain requires at least 1 dot
- Extension minimum 2 characters

**To modify:**

```python
@staticmethod
def validate_email(email):
    """Customize email validation"""
    # Strict validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Loose validation (accepts more formats)
    # pattern = r'.+@.+\..+'
    
    return re.match(pattern, email) is not None
```

## Display Customization

### Menu Styling

**Current:**
```
------
Main Menu:
------
1. Add New Contact
```

**To customize colors (for supported terminals):**

```python
def display_menu():
    """Display main menu options with color."""
    class Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}Main Menu:{Colors.ENDC}")
    # ... rest of menu
```

### Width and Formatting

**To change separator width:**

```python
# Change from 60 to 80 characters
SEPARATOR_WIDTH = 80
print("=" * SEPARATOR_WIDTH)
```

### Message Customization

**Success messages:**
```python
print(f"✓ Contact '{name}' added successfully!")
# Can change ✓ to: [OK], ✔, SUCCESS, +, etc.
```

**Error messages:**
```python
print("✗ Error: Name cannot be empty.")
# Can change ✗ to: [ERROR], ✘, FAIL, -, etc.
```

## Performance Tuning

### For Small Lists (< 100 contacts)
- Default settings are optimal
- No changes needed

### For Medium Lists (100-1000 contacts)

**Enable lazy loading:**
```python
class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = {}
        self.dirty = True  # Track if needs reload
        # Don't auto-load; load on demand
    
    def ensure_loaded(self):
        """Load contacts only when needed"""
        if self.dirty:
            self.load_contacts()
            self.dirty = False
```

### For Large Lists (> 1000 contacts)

**Consider database switch:**
```python
import sqlite3

class DatabaseContactManager(ContactManager):
    def __init__(self, db_file="contacts.db"):
        self.conn = sqlite3.connect(db_file)
        self.create_table()
    
    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                phone TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()
```

## Advanced Features

### Add Import from CSV

```python
def import_from_csv(self, csv_file):
    """Import contacts from CSV file"""
    import csv
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            self.add_contact(
                row['name'],
                row['phone'],
                row['email'],
                row['address']
            )
```

### Add Export to Multiple Formats

```python
def export_csv(self, filename):
    """Export as CSV"""
    import csv
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'phone', 'email', 'address'])
        writer.writeheader()
        for contact in self.contacts.values():
            writer.writerow(contact.to_dict())

def export_vcard(self, filename):
    """Export as vCard format"""
    with open(filename, 'w') as f:
        for contact in self.contacts.values():
            f.write("BEGIN:VCARD\n")
            f.write("VERSION:3.0\n")
            f.write(f"FN:{contact.name}\n")
            f.write(f"TEL:{contact.phone}\n")
            f.write(f"EMAIL:{contact.email}\n")
            f.write(f"ADR:;;{contact.address}\n")
            f.write("END:VCARD\n\n")
```

### Add Contact Categories

```python
class Contact:
    def __init__(self, name, phone, email, address, category="General"):
        # ... existing fields
        self.category = category  # Add category
```

### Add Search History

```python
class ContactManager:
    def __init__(self, filename="contacts.json"):
        # ... existing code
        self.search_history = []
    
    def search_contacts(self, query):
        """Search and log"""
        self.search_history.append({
            'query': query,
            'timestamp': datetime.now()
        })
        # ... rest of search logic
```

## Environment Variables

### Optional: Use .env File

**Create `.env` file:**
```
CONTACTS_FILE=./data/contacts.json
BACKUP_ENABLED=true
BACKUP_FOLDER=./backups
DEBUG_MODE=false
```

**Load in Python:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
CONTACTS_FILE = os.getenv('CONTACTS_FILE', 'contacts.json')
BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'false') == 'true'
```

## Logging Configuration

### Enable Debug Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('contact_manager.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

### Log Levels
- **DEBUG** - Detailed information for debugging
- **INFO** - General informational messages
- **WARNING** - Warning messages for potential issues
- **ERROR** - Error messages for failures

## Backup & Recovery

### Manual Backup

**Windows:**
```batch
copy contacts.json contacts_backup_%date%.json
```

**macOS/Linux:**
```bash
cp contacts.json contacts_backup_$(date +%Y%m%d_%H%M%S).json
```

### Automated Backup

```python
import shutil
from datetime import datetime

def create_backup(self):
    """Create timestamped backup"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"contacts_backup_{timestamp}.json"
    shutil.copy(self.filename, backup_file)
    print(f"✓ Backup created: {backup_file}")

# Call periodically
if len(self.contacts) % 10 == 0:  # After every 10 operations
    self.create_backup()
```

### Restore from Backup

```python
def restore_from_backup(self, backup_file):
    """Restore contacts from backup"""
    if not os.path.exists(backup_file):
        print("✗ Backup file not found")
        return
    
    shutil.copy(backup_file, self.filename)
    self.load_contacts()
    print(f"✓ Restored from {backup_file}")
```

## Troubleshooting Installation

### Issue: "python: command not found"

**Solution:**
- Windows: Use `python3` or install Python from python.org
- macOS: Use `python3` (need to install via brew or python.org)
- Linux: Use `python3` or install via package manager

### Issue: "Module not found" errors

**Solution:**
- This app uses only standard library - no external packages needed
- Ensure Python 3.6+ is installed

### Issue: Permission denied when saving

**Solution:**
- Check folder write permissions
- Save to a different location
- Run terminal as administrator (Windows)

### Issue: File path not working

**Solution:**
```python
# Use absolute path
manager = ContactManager("/absolute/path/to/contacts.json")

# Or use home directory
import os
home = os.path.expanduser("~")
manager = ContactManager(os.path.join(home, "Documents", "contacts.json"))
```

## Performance Testing

### Benchmark Add Operation

```python
import time

manager = ContactManager()
start = time.time()

for i in range(1000):
    manager.add_contact(
        f"Contact {i}",
        f"555{i:07d}",
        f"contact{i}@example.com",
        f"{i} Test St"
    )

elapsed = time.time() - start
print(f"Added 1000 contacts in {elapsed:.2f} seconds")
print(f"Average: {elapsed/1000*1000:.2f} ms per contact")
```

### Benchmark Search Operation

```python
import time

manager = ContactManager("contacts.json")
start = time.time()

for i in range(100):
    manager.search_contacts("Contact")

elapsed = time.time() - start
print(f"100 searches in {elapsed:.2f} seconds")
```

## Security Best Practices

1. **Backup Regularly**
   ```bash
   # Weekly backup
   cp contacts.json contacts_backup_weekly.json
   ```

2. **Restrict File Access**
   ```bash
   # Linux/macOS: Readable only by owner
   chmod 600 contacts.json
   ```

3. **Don't Share Contact Files**
   - Keep contacts.json private
   - Don't commit to public repositories
   - Use .gitignore if using Git

4. **Encrypt Sensitive Data** (Optional)
   ```python
   from cryptography.fernet import Fernet
   
   key = Fernet.generate_key()
   cipher_suite = Fernet(key)
   encrypted_data = cipher_suite.encrypt(contacts_json.encode())
   ```

## Uninstall

**To remove the application:**

1. Delete `contact_management_system.py`
2. Delete `contacts.json` (if you saved a backup)
3. Delete any backup files (optional)

**To remove virtual environment:**

```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

---

**Setup Guide Version:** 1.0  
**Last Updated:** May 26, 2026
