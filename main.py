import re
import csv
from data import DATA_FILE, PHONE_PATTERN, SUB_PHONE


def input_data():
    with open(DATA_FILE, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def parse_contact_list(contacts_list):
    new_contacts_list = list()
    for contact in contacts_list:
        new_contact = list()  #Inițializăm o nouă listă (new_contact) pentru a stoca informațiile curățate ale unui contact
        full_name_str = ",".join(contact[:3])  #Concatenează primele trei elemente ale contactului pentru a obține un șir de nume complet (full_name_str)
        result = re.findall(r'(\w+)', full_name_str)  #Folosește expresii regulate (re.findall()) pentru a găsi toate cuvintele în full_name_str
        while len(result) < 3:
            result.append('')  #Asigură că există cel puțin trei elemente în lista rezultată și completează cu șiruri goale dacă nu există suficiente
        new_contact += result  #result - [lastname, firstname, surname]
        new_contact.append(contact[3])  #organisation
        new_contact.append(contact[4])  #position
        phone_pattern = re.compile(PHONE_PATTERN)  #Compilează un obiect de tipul expresiei regulate pentru modelul de număr de telefon
        changed_phone = phone_pattern.sub(SUB_PHONE, contact[5]) #reformatam numărul de telefon folosind expresia regulată definită anterior
        new_contact.append(changed_phone) #phone
        new_contact.append(contact[6]) #email
        new_contacts_list.append(new_contact)
    return new_contacts_list


def delete_duplicates_contact(new_contacts_list):
    phone_book = dict()
    for contact in new_contacts_list:
        if contact[0] in phone_book:
            contact_value = phone_book[contact[0]] #contact_value devine contactul existent din dicț
            for i in range(len(contact_value)): #actualizam datele din contact_value cu datele din dublura(iteratia actuala)
                if contact[i]:
                    contact_value[i] = contact[i]
        else:
            phone_book[contact[0]] = contact #umplem dictul, key=contact[0]: value=fullcontact
    return list(phone_book.values())


def write_data(new_contacts_list):
    with open("new_reformat_phonebook.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(new_contacts_list)

if __name__ == "__main__":
    new_contacts_list = input_data()
    new_parsed_list = parse_contact_list(new_contacts_list)
    contact_book_values = delete_duplicates_contact(new_parsed_list)
    write_data(contact_book_values)