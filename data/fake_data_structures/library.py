"""
Here the schema of the table from client has to be pasted
---

**TABLE NAME** Website Aggregates

**Schema**
    column_name : data_type
    
"""

from src.utils import generate_int_in_range, \
    hash_fun, \
    get_structure_for_faker, \
    generate_using, \
    generate_closure, \
    generate_date_between, \
    generate_rand_from_choices, \
    get_table_blueprint

from src.mock_data_generator import create_mock_data, \
    insert_records, \
    create_table,\
    check_exists

from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

book_names = list(set([
    "The Labyrinth of Lost Dreams",
    "Moonlit Melodies",
    "Shadows and Intrigue",
    "Digital Revolution: Navigating the Tech Landscape",
    "Economics Unraveled: Understanding the Global Marketplace",
    "Quantum Quandaries",
    "How to be a Logician",
    "This Statement is False",
    "Unveiling the Cosmos: A Journey through Space Exploration",
    "Serenade of the Silver Moon",
    "Angel",
    "Mindful Living: Cultivating Peace in a Busy World",
    "Sanctum Unveiled",
    "Aetherial Tides: Saga of the Starforged",
    "The Labyrinth of Lost Dreams",
    "Monkeys On a Typewriter",
    "The Bear and The Goose",
    "The Alchemist",
    "Pride and Prejudice",
    "To Kill a Mockingbird",
    "1984",
    "The Great Gatsby",
    "Animal Farm",
    "Brave New World",
    "Lord of the Flies",
    "The Catcher in the Rye",
    "Fahrenheit 451",
    "One Hundred Years of Solitude",
    "The Hitchhiker's Guide to the Galaxy",
    "The Lord of the Rings",
    "Harry Potter and the Philosopher's Stone",
    "The Da Vinci Code",
    "The Girl with the Dragon Tattoo",
    "The Hunger Games",
    "The Chronicles of Narnia",
    "Gone with the Wind",
    "The Kite Runner",
    "Life of Pi",
    "The Road",
    "The Book Thief",
    "The Fault in Our Stars",
    "Dune",
    "The Stand",
    "American Gods",
    "Jurassic Park",
    "The Shining",
    "The Handmaid's Tale",
    "A Song of Ice and Fire",
    "The Name of the Wind",
    "The Silence of the Lambs",
    "The Color Purple",
    "The Secret History",
    "The Martian",
    "The Goldfinch",
    "Crazy Rich Asians",
    "Ready Player One",
    "The Testaments",
    "Educated",
    "Becoming",
    "Where the Crawdads Sing",
    "The Night Circus",
    "The Tattooist of Auschwitz",
    "The Water Dancer",
    "Normal People",
    "Little Fires Everywhere",
    "Circe",
    "The Seven Husbands of Evelyn Hugo",
    "Red, White & Royal Blue",
    "The Vanishing Half",
    "The Silent Patient",
    "Such a Fun Age",
    "The Dutch House",
    "The Giver of Stars",
    "Daisy Jones & The Six",
    "City of Girls",
    "A Gentleman in Moscow",
    "The Starless Sea",
    "The Glass Hotel",
    "Anxious People",
    "The Invisible Life of Addie LaRue",
    "Transcendent Kingdom",
    "Mexican Gothic",
    "The Midnight Library",
    "The Push",
    "Klara and the Sun",
    "The Last Thing He Told Me",
    "The Final Girl Support Group",
    "The Maidens",
    "The Paper Palace",
    "The Wife Upstairs",
    "The Lincoln Highway",
    "Apples Never Fall",
    "Cloud Cuckoo Land",
    "Harlem Shuffle",
    "The Love Hypothesis",
    "Velvet Was the Night",
    "Project Hail Mary",
    "The Last Graduate",
    "The Atlas Six",
    "The Once and Future Witches",
    "The Burning Girls",
    "The Personal Librarian",
    "The Therapist",
    "The Bone Shard Daughter",
    "The Death of Jane Lawrence",
    "The Turnout",
    "The Plot",
    "The Unheard",
    "The Echo Wife",
    "The Ones We're Meant to Find",
    "The Maid",
    "The Forest of Vanishing Stars",
    "The Siren",
    "The Burning God",
    "The Ruthless Lady's Guide to Wizardry",
    "The Vanished Queen",
    "The Inheritance of Orquídea Divina",
    "The Girl and the Goddess",
    "The Chosen and the Beautiful",
    "The Witch King",
    "The Jasmine Throne",
]))

member_names = list(set([
    "Emma Smith",
    "Olivia Johnson",
    "Ava Williams",
    "Isabella Jones",
    "Sophia Brown",
    "Charlotte Davis",
    "Mia Miller",
    "Amelia Wilson",
    "Harper Moore",
    "Evelyn Taylor",
    "Liam Anderson",
    "Noah Thomas",
    "Oliver Jackson",
    "Elijah White",
    "William Harris",
    "James Martin",
    "Benjamin Thompson",
    "Lucas Garcia",
    "Henry Martinez",
    "Alexander Robinson",
    "Aiden Clark",
    "Ethan Rodriguez",
    "Daniel Lewis",
    "Matthew Lee",
    "Jackson Walker",
    "David Hall",
    "Joseph Allen",
    "Samuel Young",
    "Carter Hernandez",
    "Sebastian King",
    "Abigail Wright",
    "Emily Lopez",
    "Elizabeth Hill",
    "Mila Scott",
    "Ella Green",
    "Avery Adams",
    "Sofia Baker",
    "Camila Gonzalez",
    "Aria Nelson",
    "Scarlett Carter",
    "Michael Mitchell",
    "Lucy Perez",
    "Evelyn Roberts",
    "Lincoln Turner",
    "Grace Phillips",
    "Victoria Campbell",
    "Penelope Parker",
    "Riley Evans",
    "Zoey Edwards",
    "Lillian Collins",
    "Anthony Stewart",
    "Dylan Sanchez",
    "Christopher Morris",
    "Luke Rogers",
    "Adam Reed",
    "Nathan Cook",
    "Isaac Morgan",
    "Andrew Bell",
    "Joshua Murphy",
    "Gabriel Bailey",
    "Chloe Rivera",
    "Layla Cooper",
    "Nora Richardson",
    "Hazel Cox",
    "Zoe Howard",
    "Luna Ward",
    "Stella Torres",
    "Aurora Peterson",
    "Leah Gray",
    "Violet Ramirez",
    "Ellie James",
    "Claire Watson",
    "Bella Brooks",
    "Natalie Kelly",
    "Skylar Sanders",
    "Allison Price",
    "Lucy Bennett",
    "Anna Wood",
    "Samantha Barnes",
    "Caroline Ross",
    "Xavier Henderson",
    "Levi Coleman",
    "Logan Jenkins",
    "Mateo Perry",
    "Jack Powell",
    "Theodore Long",
    "Ezra Patterson",
    "Jordan Hughes",
    "Owen Flores",
    "Caleb Washington"
]))


start_date = datetime.now().date() - timedelta(days=30)


def main():
    data_structures = {
        'library_books': {
            'book_id': ('VARCHAR(64) PRIMARY KEY', generate_using(hash_fun, 'title')),
            'title': ('VARCHAR(255)', None),
            'author': ('VARCHAR(100)', fake.name),
            'count': ('INT', generate_int_in_range(1, 5))
        },
        'library_members': {
            'member_id': ('VARCHAR(64) PRIMARY KEY', generate_using(hash_fun, 'name')),
            'name': ('VARCHAR(100)', None),
            'email': ('VARCHAR(255)', fake.email)
        },
        'books_lent':  {
            'lent_id': ('VARCHAR(64) PRIMARY KEY', generate_using(hash_fun, 'book_id', 'member_id')),
            'book_id': ('VARCHAR(64) REFERENCES library_books(book_id)', generate_closure(hash_fun, generate_rand_from_choices(book_names))),
            'member_id': ('VARCHAR(64) REFERENCES library_members(member_id)', generate_closure(hash_fun, generate_rand_from_choices(member_names))),
            'lend_date': ('DATE', generate_date_between(start_date)),
        }
    }

    output = []
    for table_name, structure in data_structures.items():
        output.append({
            'table_name': table_name,
            'column_blueprint': get_table_blueprint(structure),
            'fake_data_structure': get_structure_for_faker(structure)
        })

    return output

# Only for testing


if __name__ == '__main__':
    records = main()
    data = []
    object = records[0]
    structure = object['fake_data_structure']
    table_name = object['table_name']
    for name in book_names:
        mock_data = create_mock_data(structure)[0]
        mock_data['title'] = name
        mock_data['book_id'] = hash_fun(name)
        data.append(mock_data)
    if not check_exists(table_name):
        create_table(table_name,object['column_blueprint'])
    insert_records(table_name, data)

    data = []
    object = records[1]
    structure = object['fake_data_structure']
    table_name = object['table_name']
    for name in member_names:
        mock_data = create_mock_data(structure)[0]
        mock_data['name'] = name
        mock_data['member_id'] = hash_fun(name)
        data.append(mock_data)
    if not check_exists(table_name):
        create_table(table_name,object['column_blueprint'])
    insert_records(table_name, data)

    data = []
    object = records[2]
    structure = object['fake_data_structure']
    table_name = object['table_name']
    if not check_exists(table_name):
        create_table(table_name,object['column_blueprint'])
    insert_records(table_name, create_mock_data(structure, 100))