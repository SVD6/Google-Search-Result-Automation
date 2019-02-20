from extract_emails import ExtractEmails


em = ExtractEmails('https://www.madridcitytours.com/', True, 20, True, 'chrome')
emails = em.emails
print (emails)
print (len(em.for_scan))