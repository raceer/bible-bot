import pythonbible, random

class BibleSearch:
    def __init__(self):
        self.books = [book for book in pythonbible.Book]

    def get_random_verse(self):

        book = random.choice(self.books)
        book_chapters = pythonbible.get_number_of_chapters(book)
        chapter = random.randint(1, book_chapters)
        verses = pythonbible.get_number_of_verses(book, chapter)
        verse = random.randint(1, verses)

        reference = pythonbible.NormalizedReference(book, chapter, verse, chapter, verse)
        verse_id = pythonbible.convert_reference_to_verse_ids(reference)[0]
        text = pythonbible.get_verse_text(verse_id) + " - " + f"{book.title} {chapter}:{verse}"
        return text

if __name__ == "__main__":
    bible = BibleSearch()
    random_verse = bible.get_random_verse()
    print(random_verse)
