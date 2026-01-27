from db import engine, Base
import models


def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database ready.")

if __name__ == "__main__":
    main()
