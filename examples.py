"""
Advanced Usage Examples - Contact Management System

This file demonstrates how to use the ContactManager class programmatically
for more advanced use cases beyond the interactive menu.
"""

from contact_management_system import ContactManager, Contact


def example_1_batch_add_contacts():
    """Example: Add multiple contacts programmatically."""
    print("\n" + "="*60)
    print("Example 1: Batch Add Multiple Contacts")
    print("="*60)
    
    manager = ContactManager("contacts_example.json")
    
    # Sample contacts to add
    contacts_data = [
        ("Alice Johnson", "5551234567", "alice.johnson@company.com", "123 Main St, Boston, MA"),
        ("Bob Smith", "5559876543", "bob.smith@company.com", "456 Oak Ave, New York, NY"),
        ("Carol White", "5555555555", "carol.white@company.com", "789 Pine Rd, Chicago, IL"),
        ("David Brown", "5554444444", "david.brown@company.com", "321 Elm St, Houston, TX"),
    ]
    
    print("\nAdding contacts...")
    for name, phone, email, address in contacts_data:
        manager.add_contact(name, phone, email, address)
    
    print("\n✓ All contacts added successfully!")


def example_2_search_and_display():
    """Example: Search and display specific contacts."""
    print("\n" + "="*60)
    print("Example 2: Search and Display Contacts")
    print("="*60)
    
    manager = ContactManager("contacts_example.json")
    
    print("\n--- Searching for 'Smith' ---")
    manager.search_contacts("Smith")
    
    print("\n--- Searching for '555' (partial phone) ---")
    manager.search_contacts("555")


def example_3_bulk_operations():
    """Example: Perform bulk operations on contacts."""
    print("\n" + "="*60)
    print("Example 3: Bulk Operations")
    print("="*60)
    
    manager = ContactManager("contacts_example.json")
    
    # Count contacts by email domain
    email_domains = {}
    for phone, contact in manager.contacts.items():
        domain = contact.email.split('@')[1]
        email_domains[domain] = email_domains.get(domain, 0) + 1
    
    print("\n--- Email Domains Distribution ---")
    for domain, count in email_domains.items():
        print(f"{domain}: {count} contact(s)")
    
    # List contacts by creation date
    print("\n--- Contacts by Creation Date ---")
    sorted_contacts = sorted(manager.contacts.items(), 
                            key=lambda x: x[1].created_at)
    for idx, (phone, contact) in enumerate(sorted_contacts, 1):
        print(f"{idx}. {contact.name} - {contact.created_at}")


def example_4_export_operations():
    """Example: Export contacts to different formats."""
    print("\n" + "="*60)
    print("Example 4: Export Contacts")
    print("="*60)
    
    manager = ContactManager("contacts_example.json")
    
    # Export to CSV format
    csv_content = "Name,Phone,Email,Address\n"
    for phone, contact in manager.contacts.items():
        csv_content += f'"{contact.name}","{contact.phone}","{contact.email}","{contact.address}"\n'
    
    with open("contacts_export.csv", "w") as f:
        f.write(csv_content)
    
    print("\n✓ Contacts exported to 'contacts_export.csv'")
    print("\nFirst few lines of CSV:")
    print(csv_content.split('\n')[0])  # Header
    for line in csv_content.split('\n')[1:3]:  # First 2 contacts
        if line:
            print(line)


def example_5_validation_examples():
    """Example: Demonstrate validation functionality."""
    print("\n" + "="*60)
    print("Example 5: Validation Examples")
    print("="*60)
    
    manager = ContactManager()
    
    # Test phone number validation
    test_phones = [
        "5551234567",      # Valid
        "555-123-4567",    # Valid with hyphens
        "555 123 4567",    # Valid with spaces
        "123",             # Invalid - too short
        "555-ABC-1234",    # Invalid - contains letters
        "5551234567890123" # Invalid - too long
    ]
    
    print("\n--- Phone Number Validation ---")
    for phone in test_phones:
        result = "✓ Valid" if manager.validate_phone(phone) else "✗ Invalid"
        print(f"{phone:<20} {result}")
    
    # Test email validation
    test_emails = [
        "john@example.com",        # Valid
        "sarah.johnson@work.co.uk", # Valid
        "invalid.email",           # Invalid - no @
        "@example.com",            # Invalid - no local part
        "john@.com",               # Invalid - no domain
    ]
    
    print("\n--- Email Validation ---")
    for email in test_emails:
        result = "✓ Valid" if manager.validate_email(email) else "✗ Invalid"
        print(f"{email:<30} {result}")


def example_6_contact_statistics():
    """Example: Display contact statistics."""
    print("\n" + "="*60)
    print("Example 6: Contact Statistics")
    print("="*60)
    
    manager = ContactManager("contacts_example.json")
    
    if not manager.contacts:
        print("\nNo contacts found.")
        return
    
    total_contacts = len(manager.contacts)
    
    # Get phone number providers (implied from format)
    phone_formats = {"international": 0, "local": 0}
    for phone in manager.contacts.keys():
        if phone.startswith("+"):
            phone_formats["international"] += 1
        else:
            phone_formats["local"] += 1
    
    # Count email providers
    email_providers = {}
    for contact in manager.contacts.values():
        provider = contact.email.split('@')[1].split('.')[0]
        email_providers[provider] = email_providers.get(provider, 0) + 1
    
    print(f"\n--- Statistics ---")
    print(f"Total Contacts: {total_contacts}")
    print(f"Phone Formats: {phone_formats}")
    print(f"\nTop Email Providers:")
    for provider, count in sorted(email_providers.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {provider}: {count} contact(s)")


def example_7_contact_filtering():
    """Example: Filter contacts by various criteria."""
    print("\n" + "="*60)
    print("Example 7: Filter Contacts by Criteria")
    print("="*60)
    
    manager = ContactManager("contacts_example.json")
    
    if not manager.contacts:
        print("\nNo contacts found.")
        return
    
    # Filter by name length
    print("\n--- Contacts with names longer than 10 characters ---")
    long_names = {p: c for p, c in manager.contacts.items() if len(c.name) > 10}
    for phone, contact in long_names.items():
        print(f"  {contact.name} ({len(contact.name)} chars)")
    
    # Filter by email provider
    print("\n--- Contacts with Gmail addresses ---")
    gmail_contacts = {p: c for p, c in manager.contacts.items() 
                     if c.email.endswith('@gmail.com')}
    for phone, contact in gmail_contacts.items():
        print(f"  {contact.name}: {contact.email}")
    
    # Filter by address content
    print("\n--- Contacts in California (CA) ---")
    ca_contacts = {p: c for p, c in manager.contacts.items() 
                  if 'CA' in c.address.upper()}
    for phone, contact in ca_contacts.items():
        print(f"  {contact.name}: {contact.address}")


def example_8_backup_and_restore():
    """Example: Create and restore backups."""
    print("\n" + "="*60)
    print("Example 8: Backup and Restore")
    print("="*60)
    
    import shutil
    import os
    from datetime import datetime
    
    manager = ContactManager("contacts_example.json")
    
    if not os.path.exists("contacts_example.json"):
        print("\nNo contacts file to backup.")
        return
    
    # Create backup with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"contacts_backup_{timestamp}.json"
    
    shutil.copy("contacts_example.json", backup_name)
    print(f"\n✓ Backup created: {backup_name}")
    
    # List recent backups
    import glob
    backups = sorted(glob.glob("contacts_backup_*.json"), reverse=True)[:3]
    print(f"\nRecent backups:")
    for backup in backups:
        size = os.path.getsize(backup) / 1024  # Convert to KB
        print(f"  {backup} ({size:.2f} KB)")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print(" "*15 + "CONTACT MANAGEMENT SYSTEM - ADVANCED EXAMPLES")
    print("="*70)
    
    examples = [
        ("Batch Add Contacts", example_1_batch_add_contacts),
        ("Search and Display", example_2_search_and_display),
        ("Bulk Operations", example_3_bulk_operations),
        ("Export Contacts", example_4_export_operations),
        ("Validation Examples", example_5_validation_examples),
        ("Contact Statistics", example_6_contact_statistics),
        ("Filter Contacts", example_7_contact_filtering),
        ("Backup and Restore", example_8_backup_and_restore),
    ]
    
    print("\nAvailable Examples:")
    for idx, (name, _) in enumerate(examples, 1):
        print(f"  {idx}. {name}")
    
    print("\n" + "-"*70)
    print("Note: Examples 1-8 create their own sample data.")
    print("Modify example functions to work with your actual contacts.json")
    print("-"*70)
    
    # Run examples sequentially or select specific ones
    try:
        choice = input("\nRun all examples? (yes/no): ").lower()
        if choice == 'yes':
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n✗ Error in {name}: {e}")
                input("\nPress Enter to continue to next example...")
        else:
            print("\nEnter example numbers to run (comma-separated, e.g., 1,3,5):")
            selections = input("Your selection: ").split(',')
            for sel in selections:
                try:
                    idx = int(sel.strip()) - 1
                    if 0 <= idx < len(examples):
                        examples[idx][1]()
                        input("\nPress Enter to continue...")
                except (ValueError, IndexError):
                    print(f"Invalid selection: {sel}")
    
    except KeyboardInterrupt:
        print("\n\n✗ Examples interrupted.")
    
    print("\n" + "="*70)
    print("Examples completed! Refer to the source code for more details.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
