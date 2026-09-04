import os
import shutil
import re
import csv

source_folder = os.path.join(os.path.dirname(__file__), "data")
organized_folder = os.path.join(os.path.dirname(__file__), "organized")

if not os.path.exists(organized_folder):
    os.makedirs(organized_folder)

for file_name in os.listdir(source_folder):
    file_path = os.path.join(source_folder, file_name)

    file_extension = os.path.splitext(file_name)[1].lower()

    print(file_name, "->", file_extension)

    extension_folder = os.path.join(organized_folder, file_extension[1:])

    if not os.path.exists(extension_folder):
        os.makedirs(extension_folder)

    shutil.move(file_path, extension_folder)
    
def extract_data(file_path):
        with open(file_path, "r") as file:
            text = file.read()

        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

        emails = re.findall(email_pattern, text)
        
        transaction_pattern = r'TXN-\d+'

        transaction_ids = re.findall(transaction_pattern, text)

        return emails, transaction_ids        
        


csv_file = os.path.join(organized_folder, "master.csv")

with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["File Name", "Email", "Transaction ID"])

    for folder_name in os.listdir(organized_folder):
        folder_path = os.path.join(organized_folder, folder_name)

        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                if file_name.endswith((".txt", ".log")):
                    emails, transaction_ids = extract_data(file_path)

                    print(file_name, emails, transaction_ids)

                    for email in emails:
                        for transaction_id in transaction_ids:
                            writer.writerow([file_name, email, transaction_id])