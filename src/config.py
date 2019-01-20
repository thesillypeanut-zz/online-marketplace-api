class Config:
    # these belong in a safer place (perhaps as exports in your bash_profile)
    SECRET_KEY = 'thisissooosecret_itshouldntevenbehere'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
