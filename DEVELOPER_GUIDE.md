# Contact Management System - Developer Guide

## Architecture Overview

The Contact Management System is built with a clean, object-oriented design that separates concerns and enables easy extension and maintenance.

### Core Components

#### 1. **Contact Class**
Represents an individual contact with personal information.

**Attributes:**
- `name` - Contact's full name
- `phone` - Phone number (unique identifier)
- `email` - Email address
- `address` - Physical address
- `created_at` - Timestamp of creation

**Key Methods:**
- `to_dict()` - Converts contact to dictionary for JSON serialization
- `__str__()` - Returns formatted string representation

#### 2. **ContactManager Class**
Manages all contact operations including CRUD, validation, and persistence.

**Key Methods:**

| Method | Purpose |
|--------|---------|
| `load_contacts()` | Load contacts from JSON file |
| `save_contacts()` | Save contacts to JSON file |
| `validate_phone()` | Validate phone number format |
| `validate_email()` | Validate email format |
| `add_contact()` | Add new contact with validation |
| `view_all_contacts()` | Display all contacts formatted |
| `search_contacts()` | Search by name or phone |
| `update_contact()` | Update contact details |
| `delete_contact()` | Delete contact with confirmation |

#### 3. **User Interface Functions**
Interactive command-line functions for user interaction.

**Functions:**
- `display_banner()` - Shows application title
- `display_menu()` - Shows menu options
- `add_contact_interactive()` - Interactive contact addition
- `search_contact_interactive()` - Interactive search
- `update_contact_interactive()` - Interactive update
- `delete_contact_interactive()` - Interactive deletion
- `main()` - Main application loop

## Data Structure

### In-Memory Structure
```python
contacts = {
    "5551234567": Contact(...),
    "5559876543": Contact(...),
}
```
Uses phone numbers as unique keys for O(1) lookup.

### File Structure (contacts.json)
```json
{
  "5551234567": {
    "name": "John Doe",
    "phone": "5551234567",
    "email": "john@example.com",
    "address": "123 Main St, City, State",
    "created_at": "2026-05-26 10:30:45"
  }
}
```

## Design Patterns Used

### 1. **Separation of Concerns**
- `Contact` class: Data representation
- `ContactManager` class: Business logic and persistence
- UI functions: User interaction

### 2. **Encapsulation**
- Contact data encapsulated in Contact class
- Manager handles all contact operations
- Validation logic centralized

### 3. **Single Responsibility**
- Each method has a single, clear purpose
- Validation separated from storage
- UI separated from business logic

## Validation Strategy

### Phone Number Validation
```
Rule: 10-15 numeric digits
Supports: Spaces, hyphens (removed before validation)
Regex: ^\d{10,15}$
```

### Email Validation
```
Rule: Standard email format with TLD
Pattern: user@domain.extension
Regex: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

### Field Validation
```
Name: Required, non-empty (whitespace trimmed)
Address: Required, non-empty (whitespace trimmed)
```

## Extending the System

### Adding a New Feature

**Example: Add phone number formatting**

```python
class ContactManager:
    @staticmethod
    def format_phone(phone):
        """Format phone to (XXX) XXX-XXXX"""
        cleaned = phone.replace("-", "").replace(" ", "")
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    
    def get_formatted_contact(self, phone):
        contact = self.contacts[phone]
        contact.phone = self.format_phone(contact.phone)
        return contact
```

### Adding a New Storage Format

**Example: Add CSV export**

```python
def export_to_csv(self, filename):
    """Export contacts to CSV file"""
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'phone', 'email', 'address'])
        writer.writeheader()
        for contact in self.contacts.values():
            writer.writerow(contact.to_dict())
```

### Adding a New Search Method

**Example: Search by email domain**

```python
def search_by_email_domain(self, domain):
    """Find all contacts with specific email domain"""
    results = {}
    for phone, contact in self.contacts.items():
        if contact.email.endswith(f"@{domain}"):
            results[phone] = contact
    return results
```

## Error Handling Strategy

### Validation Errors
- Input validation before processing
- Clear error messages to user
- Operation rejected without side effects

### File I/O Errors
- Try-except blocks for file operations
- Graceful degradation (starts with empty list if file corrupted)
- User notification of errors

### User Input Errors
- Required fields validation
- Format validation (phone, email)
- Confirmation for destructive operations (delete)

## Performance Considerations

### Current Performance
- **Add Contact:** O(1) - Direct dictionary insertion
- **Search:** O(n) - Linear scan through contacts
- **Update:** O(1) - Direct dictionary lookup
- **Delete:** O(1) - Direct dictionary removal
- **Load:** O(n) - JSON parsing

### Optimization Opportunities

For large contact lists (>10,000):

1. **Implement Indexing**
```python
self.name_index = defaultdict(list)  # Map names to phone numbers
self.email_index = defaultdict(list)  # Map emails to phone numbers
```

2. **Use Database**
```python
# Replace JSON with SQLite
import sqlite3
conn = sqlite3.connect('contacts.db')
```

3. **Implement Caching**
```python
self.search_cache = {}  # Cache recent search results
```

## Testing Strategy

The system includes comprehensive unit tests covering:

1. **Contact Class Tests** - Creation, serialization, representation
2. **Validation Tests** - Phone, email, field validation
3. **CRUD Tests** - Add, read, update, delete operations
4. **Persistence Tests** - File save/load operations
5. **Integration Tests** - Complete workflows

### Running Tests
```bash
python test_contact_system.py
```

### Test Coverage
- Validation: 100% of validation methods
- CRUD: 100% of CRUD operations
- Edge cases: Empty inputs, duplicates, invalid formats

## Code Style Guidelines

### Naming Conventions
```python
# Classes: PascalCase
class ContactManager:
    pass

# Functions: snake_case
def add_contact_interactive():
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_FILENAME = "contacts.json"

# Private attributes: _leading_underscore
self._internal_cache = {}
```

### Documentation
```python
def add_contact(self, name, phone, email, address):
    """Add a new contact with validation.
    
    Args:
        name (str): Contact's full name
        phone (str): Phone number (10-15 digits)
        email (str): Email address
        address (str): Physical address
    
    Returns:
        bool: True if added successfully, False otherwise
    """
```

### Comments
- Use comments for "why", not "what"
- Keep docstrings concise and clear
- Update comments when code changes

## Security Considerations

### Current Implementation
- No authentication/authorization (local single-user)
- Data stored in plain text JSON
- No encryption

### For Multi-User Systems
```python
# Add user authentication
class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

# Add role-based access control
class Contact:
    def __init__(self, ..., owner, access_level):
        self.owner = owner
        self.access_level = access_level  # 'private', 'shared', 'public'
```

### For Sensitive Data
```python
# Add encryption
from cryptography.fernet import Fernet

class EncryptedContactManager(ContactManager):
    def __init__(self, filename, encryption_key):
        super().__init__(filename)
        self.cipher_suite = Fernet(encryption_key)
```

## Troubleshooting Development Issues

### Contact not saving?
```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def save_contacts(self):
    logger.debug(f"Saving {len(self.contacts)} contacts")
    # ... save logic
```

### Validation too strict?
- Modify validation methods
- Update regex patterns
- Add format parameter to phone validation

### Performance degradation?
- Monitor file size
- Check for memory leaks
- Implement caching for searches

## Future Enhancement Ideas

1. **Contact Categories** - Group contacts by type (work, personal, etc.)
2. **Photo Support** - Store contact photos
3. **Notes Field** - Add free-form notes
4. **Favorites** - Mark frequently used contacts
5. **Birthday Tracking** - Set reminders for birthdays
6. **Contact Merging** - Combine duplicate contacts
7. **Export/Import** - CSV, vCard, Outlook formats
8. **Cloud Sync** - Sync with cloud services
9. **Mobile App** - Cross-platform support
10. **Social Integration** - Link to social profiles

## File Organization Structure

```
contact_management_system/
├── contact_management_system.py  # Main application
├── test_contact_system.py        # Unit tests
├── examples.py                   # Usage examples
├── contacts.json                 # Data file (auto-created)
├── README.md                     # Full documentation
├── QUICK_START.md               # Quick start guide
└── DEVELOPER_GUIDE.md           # This file
```

## Contributing Guidelines

1. **Code Style** - Follow PEP 8
2. **Testing** - Write tests for new features
3. **Documentation** - Update docstrings and comments
4. **Backward Compatibility** - Maintain existing APIs
5. **Error Handling** - Handle edge cases gracefully

## Additional Resources

- **Python JSON Module:** https://docs.python.org/3/library/json.html
- **Regular Expressions:** https://docs.python.org/3/library/re.html
- **Unit Testing:** https://docs.python.org/3/library/unittest.html
- **File I/O:** https://docs.python.org/3/tutorial/inputoutput.html

---

**Last Updated:** May 26, 2026  
**Version:** 1.0  
**Author:** Development Team
