from data_loader import DataLoader
from chains import extract_jobs, write_mail

urls = [
    "https://www.mindinventory.com/careers.php",
]

loader = DataLoader(urls=urls)
text_data = loader.load_data()
print(repr(text_data))


jobs = extract_jobs(text_data)
emails = []
for i, job in enumerate(jobs):
    mail = write_mail(job)
    print(mail)
    emails.append(mail)

print(emails)
