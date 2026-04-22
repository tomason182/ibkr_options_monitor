import threading


class ExecutionWorker:
    def __init__(self, client, repository):
        self.client = client
        self.repo = repository
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            exec_data = self.client.execution_queue.get()

            if not self.repo.exists(exec_data["execId"]):
                self.repo.save(exec_data)
                print("Saved execution", exec_data["execID"])
