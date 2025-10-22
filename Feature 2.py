from datetime import datetime
from collections import defaultdict


# Class representing an individual in the family tree
class Person:
    def __init__(self, name, birth_date=None):
        self.name = name
        self.birth_date = birth_date  # Should be a datetime.date object
        self.parents = []  # List of parent Person objects
        self.siblings = []  # List of sibling Person objects
        self.children = []  # List of child Person objects

    def add_sibling(self, sibling):
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            sibling.siblings.append(self)  # Ensure the relationship is mutual

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parents.append(self)  # Add self as a parent to the child

    def get_siblings(self):
        return self.siblings

    def get_cousins(self):
        # Cousins are children of siblings of parents
        cousins = []
        for parent in self.parents:
            for sibling in parent.get_siblings():
                cousins.extend(sibling.children)
        return cousins


# Class representing the entire family tree
class FamilyTree:
    def __init__(self):
        self.people = {}  # Dictionary to store Person objects by name

    def add_person(self, name, birth_date=None):
        if name not in self.people:
            person = Person(name, birth_date)
            self.people[name] = person
        return self.people[name]

    def find_person(self, name):
        return self.people.get(name, None)

    def get_siblings(self, name):
        person = self.find_person(name)
        if person:
            return [sibling.name for sibling in person.get_siblings()]
        return []

    def get_cousins(self, name):
        person = self.find_person(name)
        if person:
            return [cousin.name for cousin in person.get_cousins()]
        return []

    def get_birthdays(self):
        return {name: person.birth_date for name, person in self.people.items() if person.birth_date}

    def get_sorted_birthdays(self):
        birthdays = self.get_birthdays()
        # Group by day and month, ignoring year
        birthday_dict = defaultdict(list)
        for name, birth_date in birthdays.items():
            key = (birth_date.month, birth_date.day)
            birthday_dict[key].append(name)
        # Sort by month and day
        sorted_birthdays = sorted(birthday_dict.items(), key=lambda x: (x[0][0], x[0][1]))
        return [(datetime(1, month, day).strftime("%B %d"), names) for (month, day), names in sorted_birthdays]


# Interactive menu
def main():
    family_tree = FamilyTree()

    # Prepopulate some people and relationships
    # A couple: Otto Emmersohn and Emmerlia Emmersohn
    otto = family_tree.add_person("Otto Emmersohn", datetime(1965, 3, 12).date())
    emmerlia = family_tree.add_person("Cornelia Emmersohn", datetime(1967, 6, 25).date())

    # Their children
    anna = family_tree.add_person("Anna Emmersohn", datetime(1990, 5, 15).date())
    erik = family_tree.add_person("Erik Emmersohn", datetime(1993, 8, 20).date())
    otto.add_child(anna)
    otto.add_child(erik)
    emmerlia.add_child(anna)
    emmerlia.add_child(erik)

    # Otto's siblings
    klaus = family_tree.add_person("Klaus Emmersohn", datetime(1970, 4, 8).date())
    otto.add_sibling(klaus)


    greta = family_tree.add_person("Greta Novak", datetime(1975, 7, 14).date())
    max = family_tree.add_person("Max Novak", datetime(2000, 12, 25).date())
    maria = family_tree.add_person("Maria Novak", datetime(2003, 11, 3).date())
    klaus.add_child(max)
    klaus.add_child(maria)

    # Additional family members for cousins
    franz = family_tree.add_person("Franz Bauer", datetime(1985, 2, 2).date())
    hans = family_tree.add_person("Hans Bauer", datetime(1987, 9, 30).date())
    klaus.add_sibling(franz)
    franz.add_child(hans)

    while True:
        print("\n--- Family Tree Menu ---")
        print("1. View Siblings of a Person")
        print("2. View Cousins of a Person")
        print("3. View All Birthdays")
        print("4. View Sorted Birthdays")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter the name of the person: ")
            siblings = family_tree.get_siblings(name)
            if siblings:
                print(f"Siblings of {name}: {', '.join(siblings)}")
            else:
                print(f"No siblings found for {name}.")

        elif choice == "2":
            name = input("Enter the name of the person: ")
            cousins = family_tree.get_cousins(name)
            if cousins:
                print(f"Cousins of {name}: {', '.join(cousins)}")
            else:
                print(f"No cousins found for {name}.")

        elif choice == "3":
            birthdays = family_tree.get_birthdays()
            if birthdays:
                for name, date in birthdays.items():
                    print(f"{name}: {date.strftime('%B %d, %Y')}")
            else:
                print("No birthdays found.")

        elif choice == "4":
            sorted_birthdays = family_tree.get_sorted_birthdays()
            if sorted_birthdays:
                for date, names in sorted_birthdays:
                    print(f"{date}: {', '.join(names)}")
            else:
                print("No birthdays found.")

        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


# Run the program
if __name__ == "__main__":
    main()
