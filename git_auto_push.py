import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

CAMINHO_PASTA = os.path.dirname(os.path.realpath(__file__))

class GitPushHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if not event.is_directory:
            print(f"🔄 Alteração detectada: {event.src_path}")
            try:
                subprocess.run(["git", "add", "."], cwd=CAMINHO_PASTA)
                subprocess.run(["git", "commit", "-m", "Atualização automática via Watchdog"], cwd=CAMINHO_PASTA)
                subprocess.run(["git", "push", "origin", "main"], cwd=CAMINHO_PASTA)
                print("✅ Push automático realizado.")
            except Exception as e:
                print(f"❌ Erro: {e}")

if __name__ == "__main__":
    event_handler = GitPushHandler()
    observer = Observer()
    observer.schedule(event_handler, path=CAMINHO_PASTA, recursive=True)
    observer.start()
    print("👀 Monitorando alterações na pasta...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
