def EmailTransformation(email):
    name = ' '.join([part.capitalize() for part in email.split('@')[0].split('.')])
    return name