import json
import os
from datetime import datetime
import re

class Contact:
    """Represents a single contact with name, phone, email, and address."""
    
    def __init__(self, name, phone, email, address, created_at=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """Convert contact to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at
        }
    
    def __str__(self):
        """String representation of contact for display."""
        return f"""
    Name: {self.name}
    Phone: {self.phone}
    Email: {self.email}
    Address: {self.address}
    Created: {self.created_at}"""


class ContactManager:
    """Manages all contact operations including CRUD and persistence."""
    
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = {}  # Dictionary with phone number as key
        self.load_contacts()
    
    def load_contacts(self):
        """Load contacts from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.contacts = {phone: Contact(**contact) 
                                   for phone, contact in data.items()}
                print(f"\n✓ Loaded {len(self.contacts)} contacts from file.")
            except (json.JSONDecodeError, IOError) as e:
                print(f"\n⚠ Error loading contacts: {e}. Starting with empty contact list.")
                self.contacts = {}
        else:
            self.contacts = {}
    
    def save_contacts(self):
        """Save contacts to JSON file."""
        try:
            data = {phone: contact.to_dict() 
                   for phone, contact in self.contacts.items()}
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"\n✗ Error saving contacts: {e}")
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format."""
        # Remove spaces and hyphens for validation
        cleaned = phone.replace(" ", "").replace("-", "")
        # Check if it contains only digits and is 10-15 characters
        if re.match(r'^\d{10,15}$', cleaned):
            return True
        return False
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def add_contact(self, name, phone, email, address):
        """Add a new contact with validation."""
        # Validate inputs
        if not name or not name.strip():
            print("\n✗ Error: Name cannot be empty.")
            return False
        
        if not self.validate_phone(phone):
            print("\n✗ Error: Invalid phone number. Please use 10-15 digits.")
            return False
        
        if not self.validate_email(email):
            print("\n✗ Error: Invalid email format.")
            return False
        
        if not address or not address.strip():
            print("\n✗ Error: Address cannot be empty.")
            return False
        
        # Check if phone already exists
        if phone in self.contacts:
            print(f"\n✗ Error: Contact with phone {phone} already exists.")
            return False
        
        # Create and store contact
        contact = Contact(name.strip(), phone, email.strip(), address.strip())
        self.contacts[phone] = contact
        self.save_contacts()
        print(f"\n✓ Contact '{name}' added successfully!")
        return True
    
    def view_all_contacts(self):
        """Display all contacts in a formatted manner."""
        if not self.contacts:
            print("\n✗ No contacts found. Your contact list is empty.")
            return
        
        print(f"\n{'='*60}")
        print(f"Total Contacts: {len(self.contacts)}")
        print(f"{'='*60}")
        
        for idx, (phone, contact) in enumerate(self.contacts.items(), 1):
            print(f"\n[Contact {idx}]")
            print(contact)
        
        print(f"\n{'='*60}")
    
    def search_contacts(self, query):
        """Search contacts by name or phone number."""
        query_lower = query.lower()
        results = {}
        
        for phone, contact in self.contacts.items():
            if (query_lower in contact.name.lower() or 
                query in phone):
                results[phone] = contact
        
        if not results:
            print(f"\n✗ No contacts found matching '{query}'.")
            return
        
        print(f"\n{'='*60}")
        print(f"Search Results for '{query}' ({len(results)} found)")
        print(f"{'='*60}")
        
        for idx, (phone, contact) in enumerate(results.items(), 1):
            print(f"\n[Result {idx}]")
            print(contact)
        
        print(f"\n{'='*60}")
    
    def update_contact(self, phone):
        """Update an existing contact's details."""
        if phone not in self.contacts:
            print(f"\n✗ Contact with phone {phone} not found.")
            return
        
        contact = self.contacts[phone]
        print(f"\n{'='*60}")
        print(f"Updating Contact: {contact.name}")
        print(f"{'='*60}")
        print("Leave field blank to keep current value.")
        
        # Get new details
        new_name = input("\nNew Name (current: {}): ".format(contact.name)).strip()
        new_email = input("New Email (current: {}): ".format(contact.email)).strip()
        new_address = input("New Address (current: {}): ".format(contact.address)).strip()
        
        # Update only if new values provided
        if new_name:
            contact.name = new_name
        
        if new_email:
            if not self.validate_email(new_email):
                print("\n✗ Error: Invalid email format. Email not updated.")
            else:
                contact.email = new_email
        
        if new_address:
            contact.address = new_address
        
        self.save_contacts()
        print(f"\n✓ Contact updated successfully!")
    
    def delete_contact(self, phone):
        """Delete a contact."""
        if phone not in self.contacts:
            print(f"\n✗ Contact with phone {phone} not found.")
            return
        
        contact_name = self.contacts[phone].name
        confirm = input(f"\nAre you sure you want to delete '{contact_name}'? (yes/no): ").lower()
        
        if confirm == 'yes':
            del self.contacts[phone]
            self.save_contacts()
            print(f"\n✓ Contact '{contact_name}' deleted successfully!")
        else:
            print("\n✗ Deletion cancelled.")


def display_banner():
    """Display application banner."""
    print("\n" + "="*60)
    print(" "*10 + "CONTACT MANAGEMENT SYSTEM")
    print("="*60)


def display_menu():
    """Display main menu options."""
    print("\n" + "-"*60)
    print("Main Menu:")
    print("-"*60)
    print("1. Add New Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")
    print("-"*60)


def add_contact_interactive(manager):
    """Interactive function to add a new contact."""
    print("\n" + "="*60)
    print("Add New Contact")
    print("="*60)
    
    try:
        name = input("\nEnter Name: ").strip()
        if not name:
            print("✗ Name cannot be empty.")
            return
        
        phone = input("Enter Phone Number (10-15 digits): ").strip()
        email = input("Enter Email: ").strip()
        address = input("Enter Address: ").strip()
        
        manager.add_contact(name, phone, email, address)
    
    except Exception as e:
        print(f"\n✗ Error: {e}")


def search_contact_interactive(manager):
    """Interactive function to search for a contact."""
    print("\n" + "="*60)
    print("Search Contact")
    print("="*60)
    
    try:
        query = input("\nEnter Name or Phone Number to search: ").strip()
        if not query:
            print("✗ Search query cannot be empty.")
            return
        
        manager.search_contacts(query)
    
    except Exception as e:
        print(f"\n✗ Error: {e}")


def update_contact_interactive(manager):
    """Interactive function to update a contact."""
    print("\n" + "="*60)
    print("Update Contact")
    print("="*60)
    
    try:
        phone = input("\nEnter Phone Number of Contact to Update: ").strip()
        if not phone:
            print("✗ Phone number cannot be empty.")
            return
        
        manager.update_contact(phone)
    
    except Exception as e:
        print(f"\n✗ Error: {e}")


def delete_contact_interactive(manager):
    """Interactive function to delete a contact."""
    print("\n" + "="*60)
    print("Delete Contact")
    print("="*60)
    
    try:
        phone = input("\nEnter Phone Number of Contact to Delete: ").strip()
        if not phone:
            print("✗ Phone number cannot be empty.")
            return
        
        manager.delete_contact(phone)
    
    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Main application loop."""
    manager = ContactManager()
    display_banner()
    
    while True:
        try:
            display_menu()
            choice = input("Select an option (1-6): ").strip()
            
            if choice == '1':
                add_contact_interactive(manager)
            
            elif choice == '2':
                manager.view_all_contacts()
            
            elif choice == '3':
                search_contact_interactive(manager)
            
            elif choice == '4':
                update_contact_interactive(manager)
            
            elif choice == '5':
                delete_contact_interactive(manager)
            
            elif choice == '6':
                print("\n" + "="*60)
                print("Thank you for using Contact Management System!")
                print("Goodbye!")
                print("="*60 + "\n")
                break
            
            else:
                print("\n✗ Invalid choice. Please select a valid option (1-6).")
        
        except KeyboardInterrupt:
            print("\n\n✗ Application interrupted by user.")
            print("="*60)
            break
        
        except Exception as e:
            print(f"\n✗ An unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
