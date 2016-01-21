import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def watch_file(file_name, action, *args, **kwargs):
    "Return a watchdog observer, it will call the action callback"

    def on_modified(event):
        "File-changed event"
        if event.src_path == file_name:
            action(*args, **kwargs)

    handler = FileSystemEventHandler()
    handler.on_modified = on_modified
    observer = Observer()

    base_path = os.path.split(file_name)[0]
    observer.schedule(handler, path=base_path)
    observer.start()

    return observer
