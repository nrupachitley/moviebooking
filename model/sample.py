login_id = "nrupa@amc.com"
email_add = login_id.split("@")
print(email_add)
email = email_add[1].split(".")
print(email)
print(email[0])
if email[0] == "amc" or email[0] == "bc" or email[0] == "century":
    print(True)