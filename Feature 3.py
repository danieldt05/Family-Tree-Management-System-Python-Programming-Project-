from datetime import datetime, date
from collections import defaultdict


# Feature 1 - Person Class (Partner A)
class Person:
    def __init__(self, name, birth_date=None, death_date=None, spouse=None):
        self.name = name
        self.birth_date = birth_date  # Should be a datetime.date object
        self.death_date = death_date
        self.spouse = spouse  # Spouse of the individual
        self.parents = []  # List of parent Person objects
        self.siblings = []  # List of sibling Person objects
        self.children = []  # List of child Person objects

    def add_sibling(self, sibling):
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            sibling.siblings.append(self)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parents.append(self)

    def get_siblings(self):
        return self.siblings

    def get_cousins(self):
        cousins = []
        for parent in self.parents:
            for sibling in parent.get_siblings():
                cousins.extend(sibling.children)
        return cousins

    def age_at_death(self):
        if self.death_date:
            return self.death_date.year - self.birth_date.year - (
                        (self.death_date.month, self.death_date.day) < (self.birth_date.month, self.birth_date.day))
        return None  # If no death date, return None

    def get_grandchildren(self):
        grandchildren = []
        for child in self.children:
            grandchildren.extend(child.children)
        return grandchildren

    def get_immediate_family(self):
        immediate_family = {
            'parents': [parent.name for parent in self.parents],
            'siblings': [sibling.name for sibling in self.siblings],
            'spouse': self.spouse.name if self.spouse else None,
            'children': [child.name for child in self.children]
        }
        return immediate_family

    def get_extended_family(self):
        extended_family = set(self.get_immediate_family()['parents'])
        for parent in self.parents:
            extended_family.update(parent.get_siblings())
        extended_family.update(self.get_cousins())
        extended_family.discard(self.name)
        return list(extended_family)


# Feature 2 - FamilyTree Class (Partner B)
class FamilyTree:
    def __init__(self):
        self.people = {}

    def add_person(self, name, birth_date=None, death_date=None, spouse=None):
        if name not in self.people:
            person = Person(name, birth_date, death_date, spouse)
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
        birthday_dict = defaultdict(list)
        for name, birth_date in birthdays.items():
            key = (birth_date.month, birth_date.day)
            birthday_dict[key].append(name)
        sorted_birthdays = sorted(birthday_dict.items(), key=lambda x: (x[0][0], x[0][1]))
        return [(datetime(1, month, day).strftime("%B %d"), names) for (month, day), names in sorted_birthdays]

    def average_age_at_death(self):
        total_age = 0
        count = 0
        for person in self.people.values():
            age = person.age_at_death()
            if age:
                total_age += age
                count += 1
        return total_age / count if count else None

    def number_of_children(self):
        children_count = {}
        for person in self.people.values():
            children_count[person.name] = len(person.children)
        return children_count

    def average_number_of_children(self):
        total_children = sum(len(person.children) for person in self.people.values())
        total_people = len(self.people)
        return total_children / total_people if total_people else None


# Create the family tree (integrating both partners' branches)

family_tree = FamilyTree()

# Example family members from both branches

# Partner A's branch
otto = family_tree.add_person("Otto Emmersohn", birth_date=datetime(1980, 3, 15).date())
emmerlia = family_tree.add_person("Cornelia Emmersohn", birth_date=datetime(1985, 6, 20).date())

anna = family_tree.add_person("Anna Emmersohn", birth_date=datetime(2010, 5, 15).date())
otto.add_child(anna)
emmerlia.add_child(anna)

# Partner B's branch
karanbir = family_tree.add_person("Karanbir Thakuri", birth_date=datetime(1935, 10, 10).date(),
                                  death_date=datetime(2005, 5, 25).date())
laxmi = family_tree.add_person("Laxmi Thakuri", birth_date=datetime(1938, 2, 5).date(),
                               death_date=datetime(2010, 9, 10).date())

# Adding siblings and children
karanbir.add_sibling(laxmi)
laxmi.add_child(otto)  # Laxmi is Otto's grandparent


# Main interactive program for all features
def main():
    while True:
        print("\n--- Family Tree Menu ---")
        print("1. Parents and Grandparents")
        print("2. Immediate Family")
        print("3. Extended Family")
        print("4. Average Age at Death")
        print("5. Number of Children for Each Individual")
        print("6. Average Number of Children per Person")
        print("7. Siblings")
        print("8. Cousins")
        print("9. Family Birthdays")
        print("10. Sorted Birthday Calendar")
        print("11. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter the name of the person: ")
            person = family_tree.find_person(name)
            if person:
                parents = person.parents
                grandchildren = person.get_grandchildren()
                print(f"Parents of {name}: {[p.name for p in parents]}")
                print(f"Grandchildren of {name}: {[g.name for g in grandchildren]}")
            else:
                print(f"No person found with name {name}.")

        elif choice == "2":
            name = input("Enter the name of the person: ")
            person = family_tree.find_person(name)
            if person:
                immediate_family = person.get_immediate_family()
                print(f"Immediate family of {name}: {immediate_family}")
            else:
                print(f"No person found with name {name}.")

        elif choice == "3":
            name = input("Enter the name of the person: ")
            person = family_tree.find_person(name)
            if person:
                extended_family = person.get_extended_family()
                print(f"Extended family of {name}: {extended_family}")
            else:
                print(f"No person found with name {name}.")

        elif choice == "4":
            average_age = family_tree.average_age_at_death()
            if average_age is not None:
                print(f"The average age at death is {average_age:.2f} years.")
            else:
                print("No death dates found.")

        elif choice == "5":
            children_count = family_tree.number_of_children()
            for person, count in children_count.items():
                print(f"{person} has {count} children.")

        elif choice == "6":
            avg_children = family_tree.average_number_of_children()
            if avg_children is not None:
                print(f"The average number of children per person is {avg_children:.2f}.")
            else:
                print("No people found.")

        elif choice == "7":
            name = input("Enter the name of the person: ")
            siblings = family_tree.get_siblings(name)
            print(f"Siblings of {name}: {siblings}")

        elif choice == "8":
            name = input("Enter the name of the person: ")
            cousins = family_tree.get_cousins(name)
            print(f"Cousins of {name}: {cousins}")

        elif choice == "9":
            birthdays = family_tree.get_birthdays()
            print("Family Birthdays:")
            for name, birth_date in birthdays.items():
                print(f"{name}: {birth_date.strftime('%B %d')}")

        elif choice == "10":
            birthday_calendar = family_tree.get_sorted_birthdays()
            print("Birthday Calendar:")
            for date, names in birthday_calendar:
                print(f"{date}: {', '.join(names)}")

        elif choice == "11":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
