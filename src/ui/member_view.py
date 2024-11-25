"""
Member management view for St Mary's Fitness Management System.
Provides user interface for managing members.
"""

from services.member_service import MemberService


class MemberView:
    """View for managing members"""

    def __init__(self, member_service: MemberService):
        self.member_service = member_service

    def display_menu(self):
        """Display the member management menu"""
        print("\n=== Member Management ===")
        print("1. View All Members")
        print("2. Add New Member")
        print("3. Update Member Information")
        print("4. Deactivate Member")
        print("5. Activate Member")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")
        self.handle_choice(choice)

    def handle_choice(self, choice: str):
        """Handle user's menu choice"""
        if choice == "1":
            self.view_all_members()
        elif choice == "2":
            self.add_new_member()
        elif choice == "3":
            self.update_member_info()
        elif choice == "4":
            self.deactivate_member()
        elif choice == "5":
            self.activate_member()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please try again.")
            self.display_menu()

    def view_all_members(self):
        """Display all members"""
        members = self.member_service.get_all_members()
        if not members:
            print("No members found.")
            return
        print("\n=== Member List ===")
        for member in members:
            print(f"{member.id}: {member.full_name} ({'Active' if member.is_active else 'Inactive'})")

    def add_new_member(self):
        """Add a new member"""
        print("\n=== Add New Member ===")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        membership_type = input("Membership Type (regular/premium/trial): ").lower()
        address = input("Address: ")

        # Simplified: More validations or dynamic inputs for address and health info can be added.
        health_info = {
            "height": float(input("Height (cm): ")),
            "weight": float(input("Weight (kg): ")),
            "medical_conditions": input("Medical Conditions (comma-separated): ").split(","),
            "emergency_contact_name": input("Emergency Contact Name: "),
            "emergency_contact_phone": input("Emergency Contact Phone: ")
        }

        try:
            new_member = self.member_service.add_member(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                membership_type=membership_type,
                address=address,
                health_info=health_info
            )
            print(f"New member added successfully! ID: {new_member.id}")
        except ValueError as e:
            print(f"Error: {e}")

    def update_member_info(self):
        """Update member information"""
        member_id = input("\nEnter Member ID: ")
        print("Leave fields blank to retain current values.")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        address = input("Address: ")

        try:
            updated_member = self.member_service.update_member(
                member_id=member_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address
            )
            print(f"Member updated successfully! Name: {updated_member.full_name}")
        except ValueError as e:
            print(f"Error: {e}")

    def deactivate_member(self):
        """Deactivate a member"""
        member_id = input("\nEnter Member ID to deactivate: ")
        try:
            self.member_service.deactivate_member(member_id)
            print(f"Member ID {member_id} deactivated.")
        except ValueError as e:
            print(f"Error: {e}")

    def activate_member(self):
        """Activate a member"""
        member_id = input("\nEnter Member ID to activate: ")
        try:
            self.member_service.activate_member(member_id)
            print(f"Member ID {member_id} activated.")
        except ValueError as e:
            print(f"Error: {e}")
