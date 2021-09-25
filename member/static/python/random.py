def password_init( req ):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*"
    password = ""
    
    for i in range(8):
        index = random.randrange(len(alphabet))
        password = password + alphabet[index]
    if any(a.isdigit() for a in password) == True:
        return password

    elif any(a.isdigit() for a in password) == False:
        return password_init()
    
    print(password_init())
