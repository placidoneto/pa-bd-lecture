class Config:
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/meuappdb" (Caso queira usar PostgreSQL)
    SQLALCHEMY_DATABASE_URI = "sqlite:///meuappdb.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
