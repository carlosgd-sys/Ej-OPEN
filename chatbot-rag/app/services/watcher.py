import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app.db.vectorstore import index_file_hybrid
from app.config import DOCS_PATH

SUPPORTED_EXTENSIONS = (".pdf", ".txt", ".csv")


class IncrementalDocsHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(SUPPORTED_EXTENSIONS):
            time.sleep(0.5)
            index_file_hybrid(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(SUPPORTED_EXTENSIONS):
            time.sleep(0.5)
            index_file_hybrid(event.src_path)


def start_watcher():
    observer = Observer()
    observer.schedule(
        IncrementalDocsHandler(),
        DOCS_PATH,
        recursive=False
    )
    observer.start()

    print(f"Watcher híbrido activo en {DOCS_PATH}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
