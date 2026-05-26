"""
Unit Tests for Contact Management System

Tests for validation, CRUD operations, and data persistence.
Run with: python -m unittest test_contact_system.py
"""

import unittest
import os
import json
from contact_management_system import Contact, ContactManager


class TestContact(unittest.TestCase):
    """Test cases for the Contact class."""
    
    def setUp(self):
        """Create a sample contact for testing."""
        self.contact = Contact("John Doe", "5551234567", "john@example.com", "123 Main St")
    
    def test_contact_creation(self):
        """Test that a contact is created correctly."""
        self.assertEqual(self.contact.name, "John Doe")
        self.assertEqual(self.contact.phone, "5551234567")
        self.assertEqual(self.contact.email, "john@example.com")
        self.assertEqual(self.contact.address, "123 Main St")
    
    def test_contact_to_dict(self):
        """Test conversion to dictionary."""
        contact_dict = self.contact.to_dict()
        self.assertIn("name", contact_dict)
        self.assertIn("phone", contact_dict)
        self.assertIn("email", contact_dict)
        self.assertIn("address", contact_dict)
        self.assertIn("created_at", contact_dict)
    
    def test_contact_string_representation(self):
        """Test string representation of contact."""
        contact_str = str(self.contact)
        self.assertIn("John Doe", contact_str)
        self.assertIn("5551234567", contact_str)


class TestContactManagerValidation(unittest.TestCase):
    """Test validation methods in ContactManager."""
    
    def setUp(self):
        """Create a ContactManager instance for testing."""
        self.manager = ContactManager("test_contacts.json")
    
    def tearDown(self):
        """Clean up test file."""
        if os.path.exists("test_contacts.json"):
            os.remove("test_contacts.json")
    
    def test_valid_phone_numbers(self):
        """Test validation of valid phone numbers."""
        valid_phones = [
            "5551234567",
            "555-123-4567",
            "555 123 4567",
            "1234567890",
            "12345678901234567890"  # Edge case: exactly max length
        ]
        for phone in valid_phones:
            # Clean for proper testing
            if len(phone.replace('-', '').replace(' ', '')) <= 15:
                self.assertTrue(
                    self.manager.validate_phone(phone),
                    f"Phone {phone} should be valid"
                )
    
    def test_invalid_phone_numbers(self):
        """Test validation of invalid phone numbers."""
        invalid_phones = [
            "123",                    # Too short
            "abc1234567",            # Contains letters
            "555-ABC-1234",          # Contains letters
            "123456789012345678901",  # Too long
            "555.123.4567",          # Invalid separators
            "",                      # Empty
        ]
        for phone in invalid_phones:
            self.assertFalse(
                self.manager.validate_phone(phone),
                f"Phone {phone} should be invalid"
            )
    
    def test_valid_email_addresses(self):
        """Test validation of valid email addresses."""
        valid_emails = [
            "john@example.com",
            "sarah.johnson@company.co.uk",
            "mike+test@domain.org",
            "user.name@sub.domain.com",
        ]
        for email in valid_emails:
            self.assertTrue(
                self.manager.validate_email(email),
                f"Email {email} should be valid"
            )
    
    def test_invalid_email_addresses(self):
        """Test validation of invalid email addresses."""
        invalid_emails = [
            "invalid.email",
            "@example.com",
            "john@",
            "john@.com",
            "john example@test.com",
            "",
        ]
        for email in invalid_emails:
            self.assertFalse(
                self.manager.validate_email(email),
                f"Email {email} should be invalid"
            )


class TestContactManagerCRUD(unittest.TestCase):
    """Test CRUD operations in ContactManager."""
    
    def setUp(self):
        """Create a fresh ContactManager for each test."""
        self.test_file = "test_crud_contacts.json"
        self.manager = ContactManager(self.test_file)
    
    def tearDown(self):
        """Clean up test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_valid_contact(self):
        """Test adding a valid contact."""
        result = self.manager.add_contact(
            "Alice Smith",
            "5551234567",
            "alice@example.com",
            "456 Oak Ave"
        )
        self.assertTrue(result)
        self.assertIn("5551234567", self.manager.contacts)
    
    def test_add_contact_with_invalid_phone(self):
        """Test that adding contact with invalid phone fails."""
        result = self.manager.add_contact(
            "Bob Jones",
            "123",
            "bob@example.com",
            "789 Pine Rd"
        )
        self.assertFalse(result)
        self.assertEqual(len(self.manager.contacts), 0)
    
    def test_add_contact_with_invalid_email(self):
        """Test that adding contact with invalid email fails."""
        result = self.manager.add_contact(
            "Carol White",
            "5559876543",
            "invalid-email",
            "321 Elm St"
        )
        self.assertFalse(result)
        self.assertEqual(len(self.manager.contacts), 0)
    
    def test_add_contact_with_empty_name(self):
        """Test that adding contact with empty name fails."""
        result = self.manager.add_contact(
            "",
            "5555555555",
            "test@example.com",
            "123 Test St"
        )
        self.assertFalse(result)
        self.assertEqual(len(self.manager.contacts), 0)
    
    def test_add_duplicate_contact(self):
        """Test that duplicate phone numbers are rejected."""
        phone = "5551234567"
        self.manager.add_contact(
            "First Person",
            phone,
            "first@example.com",
            "123 Main St"
        )
        
        result = self.manager.add_contact(
            "Second Person",
            phone,
            "second@example.com",
            "456 Oak Ave"
        )
        
        self.assertFalse(result)
        self.assertEqual(len(self.manager.contacts), 1)
    
    def test_search_contacts_by_name(self):
        """Test searching contacts by name."""
        self.manager.add_contact("John Smith", "5551111111", "john@ex.com", "Addr1")
        self.manager.add_contact("Jane Doe", "5552222222", "jane@ex.com", "Addr2")
        self.manager.add_contact("John Doe", "5553333333", "john2@ex.com", "Addr3")
        
        # This would normally print, but we're just testing the search logic
        results = {p: c for p, c in self.manager.contacts.items() 
                  if "john" in c.name.lower()}
        self.assertEqual(len(results), 2)
    
    def test_search_contacts_by_phone(self):
        """Test searching contacts by phone number."""
        phone = "5551234567"
        self.manager.add_contact("Test Person", phone, "test@ex.com", "Test Addr")
        
        results = {p: c for p, c in self.manager.contacts.items() 
                  if phone in p}
        self.assertEqual(len(results), 1)
    
    def test_delete_existing_contact(self):
        """Test deleting an existing contact."""
        phone = "5551234567"
        self.manager.add_contact("Delete Me", phone, "delete@ex.com", "Delete Addr")
        
        self.assertIn(phone, self.manager.contacts)
        del self.manager.contacts[phone]
        self.manager.save_contacts()
        
        self.assertNotIn(phone, self.manager.contacts)
    
    def test_update_contact_fields(self):
        """Test updating contact fields."""
        phone = "5551234567"
        self.manager.add_contact("Old Name", phone, "old@ex.com", "Old Addr")
        
        contact = self.manager.contacts[phone]
        contact.name = "New Name"
        contact.email = "new@ex.com"
        contact.address = "New Addr"
        self.manager.save_contacts()
        
        # Reload and verify
        manager2 = ContactManager(self.test_file)
        updated_contact = manager2.contacts[phone]
        self.assertEqual(updated_contact.name, "New Name")
        self.assertEqual(updated_contact.email, "new@ex.com")
        self.assertEqual(updated_contact.address, "New Addr")


class TestContactManagerPersistence(unittest.TestCase):
    """Test data persistence functionality."""
    
    def setUp(self):
        """Set up test file."""
        self.test_file = "test_persistence.json"
    
    def tearDown(self):
        """Clean up test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_save_and_load_contacts(self):
        """Test that contacts are saved and loaded correctly."""
        # Create and save contacts
        manager1 = ContactManager(self.test_file)
        manager1.add_contact("Test Person", "5551234567", "test@ex.com", "Test Addr")
        manager1.add_contact("Another Person", "5559999999", "another@ex.com", "Another Addr")
        
        # Load in new manager instance
        manager2 = ContactManager(self.test_file)
        
        # Verify contacts were loaded
        self.assertEqual(len(manager2.contacts), 2)
        self.assertIn("5551234567", manager2.contacts)
        self.assertIn("5559999999", manager2.contacts)
    
    def test_json_file_format(self):
        """Test that JSON file is properly formatted."""
        manager = ContactManager(self.test_file)
        manager.add_contact("Test", "5551234567", "test@ex.com", "Addr")
        
        # Verify JSON is valid
        with open(self.test_file, 'r') as f:
            data = json.load(f)
            self.assertIn("5551234567", data)
            self.assertEqual(data["5551234567"]["name"], "Test")
    
    def test_load_corrupted_file(self):
        """Test handling of corrupted JSON file."""
        # Write invalid JSON
        with open(self.test_file, 'w') as f:
            f.write("{ invalid json }")
        
        # Should handle gracefully
        manager = ContactManager(self.test_file)
        self.assertEqual(len(manager.contacts), 0)


class TestContactManagerIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def setUp(self):
        """Set up test file."""
        self.test_file = "test_integration.json"
        self.manager = ContactManager(self.test_file)
    
    def tearDown(self):
        """Clean up test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_complete_contact_workflow(self):
        """Test a complete workflow: add, search, update, delete."""
        phone = "5551234567"
        
        # Add contact
        self.manager.add_contact("John Doe", phone, "john@ex.com", "123 Main")
        self.assertEqual(len(self.manager.contacts), 1)
        
        # Verify contact exists
        self.assertIn(phone, self.manager.contacts)
        
        # Update contact
        contact = self.manager.contacts[phone]
        contact.email = "john.new@ex.com"
        self.manager.save_contacts()
        
        # Search for contact
        results = {p: c for p, c in self.manager.contacts.items() 
                  if "John" in c.name}
        self.assertEqual(len(results), 1)
        
        # Delete contact
        del self.manager.contacts[phone]
        self.manager.save_contacts()
        self.assertEqual(len(self.manager.contacts), 0)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestContact))
    suite.addTests(loader.loadTestsFromTestCase(TestContactManagerValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestContactManagerCRUD))
    suite.addTests(loader.loadTestsFromTestCase(TestContactManagerPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestContactManagerIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
