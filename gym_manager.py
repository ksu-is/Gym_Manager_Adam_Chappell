class Gym:
    def __init__(self):
        self.classes = []  # List to store classes
        self.memberships = {}  # Dictionary to store membership statuses
        self.users = {}  # Dictionary to store user data by username

    def add_class(self, class_name, class_time):
        """Add a new class to the gym schedule."""
        self.classes.append({"class_name": class_name, "class_time": class_time})
        print(f"Class '{class_name}' added to the schedule.")

    def view_classes(self):
        """Display the list of upcoming classes."""
        if not self.classes:
            print("No upcoming classes available.")
        else:
            print("Upcoming Classes:")
            for idx, gym_class in enumerate(self.classes, 1):
                print(f"{idx}. {gym_class['class_name']} at {gym_class['class_time']}")

    def sign_up_for_class(self, user, class_index):
        """Sign up a user for a class."""
        if user.type != 'customer':
            print("Only customers can sign up for classes.")
            return

        if class_index < 1 or class_index > len(self.classes):
            print("Invalid class index.")
            return
        
        class_to_sign_up = self.classes[class_index - 1]
        user.classes.append(class_to_sign_up)
        print(f"{user.username} successfully signed up for {class_to_sign_up['class_name']}.")

    def cancel_membership(self, user):
        """Cancel a customer's membership."""
        if user.type != 'customer':
            print("Only customers can cancel memberships.")
            return

        if self.memberships.get(user.username, False):
            self.memberships[user.username] = False
            print(f"Membership for {user.username} has been canceled.")
        else:
            print(f"{user.username} does not have an active membership.")

    def create_membership(self, user):
        """Create a membership for a customer."""
        if user.type != 'customer':
            print("Only customers can create memberships.")
            return

        if self.memberships.get(user.username, False):
            print(f"{user.username} already has an active membership.")
        else:
            self.memberships[user.username] = True
            print(f"Membership for {user.username} has been created.")

    def add_user(self, username, user_type):
        """Add a new user (customer, staff, or manager)."""
        if username in self.users:
            print(f"User {username} already exists.")
        else:
            if user_type not in ['customer', 'staff', 'manager']:
                print("Invalid user type.")
                return
            self.users[username] = User(username, user_type)
            print(f"{user_type.capitalize()} '{username}' added successfully.")


class User:
    def __init__(self, username, user_type):
        self.username = username
        self.type = user_type
        self.classes = []  # List to store classes the user has signed up for

    def view_info(self):
        """View the user's information."""
        print(f"Username: {self.username}")
        print(f"User Type: {self.type}")
        if self.type == 'customer':
            print(f"Signed up for {len(self.classes)} classes.")
        else:
            print(f"User {self.username} is a {self.type}.")


class Staff(User):
    def __init__(self, username):
        super().__init__(username, 'staff')
      def add_class(self, gym, class_name, class_time):
        """Staff can add a class to the schedule."""
        gym.add_class(class_name, class_time, self)

    def view_classes(self, gym):
        """Staff can view all upcoming classes."""
        gym.view_classes()

    def manage_roster(self, gym, class_index, action, customer_username=None):
        """Manage the class roster (add/remove customers)."""
        if action not in ['add', 'remove']:
            print("Invalid action. Use 'add' or 'remove'.")
            return

        if class_index < 1 or class_index > len(gym.classes):
            print("Invalid class index.")
            return
        
        class_to_manage = gym.classes[class_index - 1]

        if action == 'add':
            if customer_username:
                class_to_manage["roster"].append(customer_username)
                print(f"{customer_username} added to {class_to_manage['class_name']} roster.")
            else:
                print("Please provide a valid customer username.")
        
        elif action == 'remove':
            if customer_username and customer_username in class_to_manage["roster"]:
                class_to_manage["roster"].remove(customer_username)
                print(f"{customer_username} removed from {class_to_manage['class_name']} roster.")
            else:
                print(f"{customer_username} not found in the class roster.")


class Manager(User):
    def __init__(self, username):
        super().__init__(username, 'manager')

    def add_class(self, gym, class_name, class_time):
        """Manager can add a class to the schedule."""
        gym.add_class(class_name, class_time)

    def view_classes(self, gym):
        """Manager can view all upcoming classes."""
        gym.view_classes()


class Customer(User):
    def __init__(self, username):
        super().__init__(username, 'customer')

    def sign_up_for_class(self, gym, class_index):
        """Customer can sign up for a class."""
        gym.sign_up_for_class(self, class_index)

    def cancel_membership(self, gym):
        """Customer can cancel their membership."""
        gym.cancel_membership(self)

    def create_membership(self, gym):
        """Customer can create a membership."""
        gym.create_membership(self)


