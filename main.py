import psycopg2

# Database connection parameters
DATABASE_NAME = "lifeline"
USER = "wraith"
PASSWORD = "kiprop"
HOST = "localhost"
PORT = "5432"

# Define the Concert class
class Concert:
    def __init__(self, concert_id):
        self.concert_id = concert_id

    def _get_connection(self):
        """Establish a connection to the PostgreSQL database."""
        return psycopg2.connect(
            dbname=DATABASE_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )

    def band(self):
        """Return the Band instance for this concert."""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                SELECT bands.id, bands.name, bands.hometown
                FROM concerts
                JOIN bands ON concerts.band_id = bands.id
                WHERE concerts.id = %s;
                """
                cursor.execute(query, (self.concert_id,))
                band = cursor.fetchone()
                return band

    def venue(self):
        """Return the Venue instance for this concert."""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                SELECT venues.id, venues.title, venues.city
                FROM concerts
                JOIN venues ON concerts.venue_id = venues.id
                WHERE concerts.id = %s;
                """
                cursor.execute(query, (self.concert_id,))
                venue = cursor.fetchone()
                return venue

    def hometown_show(self):
        """Return true if the concert is in the band's hometown."""
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                SELECT bands.hometown = venues.city
                FROM concerts
                JOIN bands ON concerts.band_id = bands.id
                JOIN venues ON concerts.venue_id = venues.id
                WHERE concerts.id = %s;
                """
                cursor.execute(query, (self.concert_id,))
                result = cursor.fetchone()
                return result[0] if result else False

    def introduction(self):
        """Return a string with the band's introduction for this concert."""
        band = self.band()
        venue = self.venue()
        if band and venue:
            return f"Hello {venue[2]}!!!!! We are {band[1]} and we're from {band[2]}"
        return "Introduction not available."

def create_tables():
    """Create tables in the PostgreSQL database."""
    with psycopg2.connect(
        dbname=DATABASE_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    ) as connection:
        with connection.cursor() as cursor:
            # Create bands table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bands (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                hometown VARCHAR(100)
            );
            """)
            # Create venues table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS venues (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100),
                city VARCHAR(100)
            );
            """)
            # Create concerts table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS concerts (
                id SERIAL PRIMARY KEY,
                band_id INTEGER REFERENCES bands(id),
                venue_id INTEGER REFERENCES venues(id),
                date VARCHAR(50)
            );
            """)
            # Commit the changes
            connection.commit()

def main():
    """Main function to test the Concert class and table creation."""
    create_tables()

    # Test the Concert class
    concert_id = 1  # Replace with an actual concert_id from your database
    concert = Concert(concert_id)

    print("Band:", concert.band())
    print("Venue:", concert.venue())
    print("Hometown Show:", concert.hometown_show())
    print("Introduction:", concert.introduction())

if __name__ == "__main__":
    main()
