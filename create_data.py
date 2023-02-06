import csv
from faker import Faker

fake = Faker()

def create_prof(fake: Faker) -> dict:
    return {
            "Name": fake.name(),
            "Country": fake.country(),
            "Address": fake.address().replace("\n", ". "),
            "Expertise": fake.date(),
            "Position": fake.job(),
            "Phone_number": fake.phone_number(),
            "Email": fake.free_email()
            }

def insert_prof(records:dict, prof:dict):
    for k,v in prof.items():
        if not records.get(k):
            records[k] = []
        records[k].append(v)

def main() -> dict:
    records = {}
    for _ in range(1000):
        insert_prof(records, create_prof(fake))

    print(records)

    with open("records.csv", "w") as recs:
        fieldnames = list(records.keys())
        writer = csv.writer(recs, delimiter="|")
        writer.writerow(fieldnames)

        writer.writerows(zip(*records.values()))
    return records

if __name__ == "__main__":
    main()
