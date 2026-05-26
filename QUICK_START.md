# Quick Start Guide

## Installation & Setup

1. **Download the File**
   - Save `contact_management_system.py` to your desired location

2. **Run the Application**
   - Open Command Prompt/PowerShell/Terminal
   - Navigate to the folder containing the script
   - Run: `python contact_management_system.py`

## Getting Started in 5 Minutes

### Step 1: Add Your First Contact
```
Select Option 1: Add New Contact
Enter Name: John Smith
Enter Phone Number: 555-123-4567
Enter Email: john.smith@example.com
Enter Address: 123 Main Street, Springfield
```
✓ Contact added!

### Step 2: Add More Contacts
```
Select Option 1 again and add:
- Name: Sarah Johnson, Phone: 555-987-6543, Email: sarah.j@example.com
- Name: Mike Wilson, Phone: 555-456-7890, Email: mike.w@example.com
```

### Step 3: View All Your Contacts
```
Select Option 2: View All Contacts
```
See all three contacts displayed with full details

### Step 4: Search for a Contact
```
Select Option 3: Search Contact
Search Query: john
```
Find "John Smith" by name or search by phone: "555-123-4567"

### Step 5: Update a Contact
```
Select Option 4: Update Contact
Enter Phone: 555-123-4567
Leave blank to keep values or enter new ones:
New Name: John D. Smith (leave blank to skip)
New Email: john.d.smith@example.com
```
Contact updated!

### Step 6: Delete a Contact
```
Select Option 5: Delete Contact
Enter Phone: 555-456-7890
Confirm deletion: yes
```
Contact removed!

### Step 7: Exit the Application
```
Select Option 6: Exit
```
All changes automatically saved to contacts.json

## Valid Input Formats

### Phone Numbers
- **Format:** 10-15 digits
- **Valid Examples:**
  - `5551234567`
  - `555-123-4567`
  - `555 123 4567`
  - `+1-555-123-4567`

### Email Addresses
- **Format:** Standard email format
- **Valid Examples:**
  - `john@example.com`
  - `sarah.johnson@company.co.uk`
  - `mike+work@domain.com`

### Names & Addresses
- **Must not be empty**
- **Can contain:** Letters, numbers, spaces, common punctuation
- **Examples:**
  - Name: `John O'Neill`
  - Address: `123 Oak St, Apt 4B, New York, NY 10001`

## Common Questions

**Q: What if I enter an invalid phone number?**
A: The system will show an error and ask you to re-enter with 10-15 digits.

**Q: Can I have the same contact saved twice?**
A: No, phone numbers are unique. The system prevents duplicate entries.

**Q: Where is my data stored?**
A: In a file called `contacts.json` in the same folder as the script.

**Q: What happens if I close without saving?**
A: Don't worry! Changes are automatically saved whenever you add, update, or delete.

**Q: Can I run this on Mac/Linux?**
A: Yes! Python works on all platforms. The process is identical.

## Keyboard Shortcuts

- **Ctrl+C**: Exit the application anytime
- **Arrow Keys**: Navigate through menu (if using enhanced terminal)

## Sample Contacts to Try

Copy and paste these when adding contacts:

1. **Alice Cooper**
   - Phone: 555-111-2222
   - Email: alice.cooper@music.com
   - Address: 456 Rock Avenue, Los Angeles, CA

2. **Bob Dylan**
   - Phone: 555-333-4444
   - Email: bob@songs.net
   - Address: 789 Nobel Street, Minneapolis, MN

3. **Charlie Parker**
   - Phone: 555-555-6666
   - Email: charlie.p@jazz.org
   - Address: 321 Jazz Lane, Kansas City, MO

## Tips for Success

✓ Use consistent formatting for similar contacts (all with area codes, etc.)
✓ Include full addresses with city and state for better organization
✓ Search by partial names - no need for exact spelling
✓ Back up contacts.json periodically
✓ Try searching by different parts of names or phone numbers

## Need Help?

- Check the detailed [README.md](README.md) for complete documentation
- Review the source code comments for technical details
- Test with sample contacts before adding real data

---

**Ready to use?** Just run `python contact_management_system.py` and start managing your contacts!
