# Contact Management System

A simple and user-friendly Python application for managing contact details efficiently.

## Features

✅ **Add New Contacts** - Store contact information with name, phone number, email, and address  
✅ **View All Contacts** - Display all saved contacts in an organized format  
✅ **Search Contacts** - Find contacts by name or phone number  
✅ **Update Contacts** - Modify existing contact details  
✅ **Delete Contacts** - Remove contacts with confirmation  
✅ **Data Persistence** - Automatically save and load contacts from file  
✅ **Input Validation** - Validates phone numbers and email formats  
✅ **Error Handling** - Graceful handling of invalid inputs and errors  

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Installation

1. Ensure you have Python 3.6+ installed on your system
2. Download or clone the `contact_management_system.py` file to your desired location

## Usage

### Running the Application

Open a terminal/command prompt and run:

```bash
python contact_management_system.py
```

### Menu Options

**1. Add New Contact**
- Enter contact name, phone number, email, and address
- Phone number must be 10-15 digits
- Email format is validated
- All fields are required

**2. View All Contacts**
- Displays all saved contacts in a formatted list
- Shows contact details including creation timestamp

**3. Search Contact**
- Search by name (partial matches supported)
- Search by phone number (exact match)
- Displays matching contacts

**4. Update Contact**
- Enter the phone number of the contact to update
- Leave fields blank to keep current values
- Modify name, email, or address

**5. Delete Contact**
- Enter the phone number of the contact to delete
- Requires confirmation before deletion
- Permanently removes the contact

**6. Exit**
- Closes the application
- All contacts are automatically saved

## File Storage

Contacts are automatically saved to a `contacts.json` file in the same directory as the script.

**contacts.json** structure:
```json
{
  "9876543210": {
    "name": "John Doe",
    "phone": "9876543210",
    "email": "john@example.com",
    "address": "123 Main St, City",
    "created_at": "2026-05-26 10:30:45"
  }
}
```

## Validation Rules

### Phone Number
- Must contain 10-15 digits
- Spaces and hyphens are allowed but removed for validation
- Examples: `9876543210`, `987-654-3210`, `987 654 3210`

### Email
- Must follow standard email format: `user@domain.com`
- Domain must have at least one dot and 2+ character extension

### Name and Address
- Cannot be empty
- Whitespace is trimmed automatically

## Example Workflow

```
1. Run the application
2. Select Option 1 to add a new contact
3. Enter: Name = "Alice Smith", Phone = "5551234567", 
         Email = "alice@example.com", Address = "456 Oak Ave"
4. Select Option 2 to view all contacts
5. Select Option 3 to search for contacts
6. Select Option 4 to update contact information
7. Select Option 5 to delete a contact when needed
8. Select Option 6 to exit
```

## Error Handling

The application handles various error scenarios:

- ✗ **Invalid phone numbers** - Shows format requirements
- ✗ **Invalid email addresses** - Alerts user and prevents saving
- ✗ **Duplicate phone numbers** - Prevents duplicate contacts
- ✗ **File I/O errors** - Provides error messages and continues operation
- ✗ **Empty inputs** - Validates required fields
- ✗ **Invalid menu choices** - Prompts user to select valid option

## Tips for Best Use

1. **Phone Number as Identifier** - Phone numbers are unique and used to identify contacts
2. **Search Flexibility** - You can search by partial name (e.g., "John" finds "John Doe")
3. **Data Persistence** - All changes are automatically saved to the JSON file
4. **Update Selectively** - Only update fields you want to change
5. **Backup** - Regularly back up your `contacts.json` file

## Troubleshooting

**Q: Where are my contacts saved?**
A: Contacts are saved in a `contacts.json` file in the same directory as the script.

**Q: Can I have multiple contacts with the same phone number?**
A: No, each phone number must be unique to prevent data conflicts.

**Q: What if I accidentally delete a contact?**
A: If you haven't closed the application, you can manually edit the `contacts.json` file to restore it.

**Q: Can I edit the contacts.json file directly?**
A: Yes, but ensure you maintain the correct JSON format to avoid corrupting the file.

## Future Enhancements

Possible improvements could include:
- Export contacts to CSV/Excel format
- Import contacts from other sources
- Categorize contacts (friends, work, family)
- Backup and restore functionality
- Contact groups and distribution lists
- Advanced search filters

---

**Version:** 1.0  
**Last Updated:** May 26, 2026  
**License:** Open Source
