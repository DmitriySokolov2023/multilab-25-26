from pathlib import Path

project_dir = Path(__file__).parent
inbox = project_dir / "inbox"
def create_demo_files(inbox: Path) -> None:
    inbox.mkdir(exist_ok=True)

    # создадим несколько “файлов”
    (inbox / "photo1.jpg").write_text("fake image", encoding="utf-8")
    (inbox / "photo2.png").write_text("fake image", encoding="utf-8")
    (inbox / "song.mp3").write_text("fake music", encoding="utf-8")
    (inbox / "notes.txt").write_text("hello", encoding="utf-8")
    (inbox / "table.csv").write_text("a,b,c\n1,2,3\n", encoding="utf-8")
    (inbox / "book.pdf").write_text("fake pdf", encoding="utf-8")
    (inbox / "archive.zip").write_text("fake zip", encoding="utf-8")
    (inbox / "script.py").write_text("print('hi')", encoding="utf-8")
    (inbox / "no_extension").write_text("?", encoding="utf-8")


create_demo_files(inbox)