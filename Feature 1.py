class Person:
    def __init__(self, name, birth_year=None, death_year=None):
        self.name = name
        self.birth_year = birth_year
        self.death_year = death_year
        self.parents = []  # List of parent objects
        self.children = []  # List of child objects
        self.siblings = []  # List of sibling objects
        self.spouse = None  # Reference to the spouse object

    def add_parent(self, parent):
        """Add a parent to the person's record."""
        if parent not in self.parents:
            self.parents.append(parent)
            parent.add_child(self)

    def add_child(self, child):
        """Add a child to the person's record."""
        if child not in self.children:
            self.children.append(child)
            child.add_parent(self)

    def add_sibling(self, sibling):
        """Add a sibling to the person's record."""
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            sibling.siblings.append(self)

    def set_spouse(self, spouse):
        """Set the spouse for the person."""
        self.spouse = spouse
        spouse.spouse = self


# Display functions
def display_parents(person):
    if person.parents:
        return f"Parents of {person.name}: " + ", ".join(parent.name for parent in person.parents)
    return f"{person.name} has no recorded parents."


def  (person):
    grandchildren = [grandchild.name for child in person.children for grandchild in child.children]
    if grandchildren:
        return f"Grandchildren of {person.name}: " + ", ".join(grandchildren)
    return f"{person.name} has no recorded grandchildren."


def display_immediate_family(person):
    immediate_family = []
    if person.parents:
        immediate_family.append("Parents: " + ", ".join(parent.name for parent in person.parents))
    if person.siblings:
        immediate_family.append("Siblings: " + ", ".join(sibling.name for sibling in person.siblings))
    if person.spouse:
        immediate_family.append(f"Spouse: {person.spouse.name}")
    if person.children:
        immediate_family.append("Children: " + ", ".join(child.name for child in person.children))
    return f"Immediate family of {person.name}:\n" + "\n".join(immediate_family) if immediate_family else f"{person.name} has no immediate family."


def display_extended_family(person):
    extended_family = set()
    if person.parents:
        extended_family.update(person.parents)
    if person.children:
        extended_family.update(person.children)
    if person.siblings:
        extended_family.update(person.siblings)
    for parent in person.parents:
        for sibling in parent.children:
            if sibling != person:
                extended_family.add(sibling)
        for grandparent in parent.parents:
            for uncle_aunt in grandparent.children:
                if uncle_aunt != parent:
                    extended_family.add(uncle_aunt)
    alive_family = [member.name for member in extended_family if member.death_year is None]
    return f"Extended family of {person.name} (alive):\n" + ", ".join(alive_family) if alive_family else f"{person.name} has no recorded extended family."


# Example setup for the family tree
otto = Person("Otto Emmersohn", birth_year=1980)
cornelia = Person("Cornelia Emmersohn", birth_year=1985)
karanbir = Person("Karanbir Thakuri" , birth_year=1935 ,death_year=2005)
laxmi = Person("Laxmi Thakuri", birth_year=1938 ,death_year=2010)
angad = Person("Angad Thakuri", birth_year=1960)
yashvi = Person("Yashvi Thakuri", birth_year=1965)

mahesh = Person("Mahesh Shah", birth_year=1990)
aanya = Person("Aanya Shah", birth_year=1991)

aadesh = Person("Aadesh Thakuri", birth_year=1990)
megha = Person("Megha Thakuri",birth_year=1994)
simran = Person("Simran Thakuri",birth_year=2008)
ashish = Person("Ashish Thakuri",birth_year=2010)
roshni = Person("Roshni Thakuri",birth_year=2012)

alision = Person("Alision Emmersohn",birth_year=1999)
william = Person("William Emmersohn",birth_year=2000)
presley = Person("Presley Emmersohn",birth_year=2000)
rowan = Person("Rowan Emmersohn",birth_year=2019)
harper = Person("Harper Emmersohn",birth_year=2024)


# Define relationships
otto.set_spouse(cornelia)
karanbir.set_spouse(laxmi)
angad.set_spouse(yashvi)
mahesh.set_spouse(aanya)
aadesh.set_spouse(megha)
william.set_spouse(presley)


karanbir.add_child(angad)
laxmi.add_child(angad)
angad.add_child(cornelia)
yashvi.add_child(cornelia)
angad.add_child(aanya)
yashvi.add_child(aanya)
angad.add_child(aadesh)
yashvi.add_child(aadesh)

aadesh.add_child(ashish)
megha.add_child(ashish)
aadesh.add_child(roshni)
megha.add_child(roshni)
aadesh.add_child(simran)
megha.add_child(simran)

cornelia.add_child(william)
otto.add_child(william)
cornelia.add_child(alision)
otto.add_child(alision)
william.add_child(rowan)
presley.add_child(rowan)
william.add_child(harper)
presley.add_child(harper)

# Dictionary to map names to Person objects
family_members = {
    person.name: person
    for person in [
        karanbir, laxmi, angad, yashvi, cornelia, otto, mahesh,
        aanya, aadesh, megha, simran, ashish, roshni, alision,
        william, presley, rowan, harper
    ]
}


# Main interactive program
def main():
    print("Welcome to the Family Tree Handling System!")

    while True:
        print("\nOptions:")
        print("1. Display Parents")
        print("2. Display Grandchildren")
        print("3. Display Immediate Family")
        print("4. Display Extended Family")
        print("7. Show All Family Members")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            name = input("Enter the name of the person: ").strip().lower()  # Convert input to lowercase
            person = None
            # Search for the person, ignoring case
            for p in family_members.values():
                if p.name.lower() == name:  # Convert the stored name to lowercase
                    person = p
                    break

            if person:
                print(display_parents(person))
            else:
                print("Person not found.")

        elif choice == "2":
            name = input("Enter the name of the person: ").strip()
            person = family_members.get(name)
            if person:
                print(display_grandchildren(person))
            else:
                print("Person not found.")

        elif choice == "3":
            name = input("Enter the name of the person: ").strip()
            person = family_members.get(name)
            if person:
                print(display_immediate_family(person))
            else:
                print("Person not found.")

        elif choice == "4":
            name = input("Enter the name of the person: ").strip()
            person = family_members.get(name)
            if person:
                print(display_extended_family(person))
            else:
                print("Person not found.")

        elif choice == "7":
            # Display all available family members
            print("\nAvailable family members:")
            for name in family_members.keys():
                print(name)

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
