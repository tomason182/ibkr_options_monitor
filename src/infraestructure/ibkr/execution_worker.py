from socket import timeout
import threading
from queue import Empty


class ExecutionWorker:
    def __init__(self, client, repository):
        self.client = client
        self.repo = repository
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        print("ExecutionWorker started")

    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        self.thread = None
        print("ExecutionWroker stopped")

    def run(self):
        while self.running:
            try:
                exec_data = self.client.execution_queue.get(timeout=1)

                # Guardado directo con INSERT OR IGNORE
                self.repo.save(exec_data)
                print("Saved execution", exec_data["exec_id"])

            except Empty:
                continue

            except Exception as e:
                print(f"Error processing executions: {str(e)}")
