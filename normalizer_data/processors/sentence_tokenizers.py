from multiprocessing import Queue, Process

from razdel import sentenize

from normalizer_data.processors.sentinels import END_OF_RESOURCES_SENTINEL


class SentenceTokenizerProcess(Process):
    """
    Takes texts from input queue and puts sentences into output queue.
    """
    def __init__(self, input_queue: Queue, out_queue: Queue):
        super().__init__(daemon=True)
        self.input_queue = input_queue
        self.output_queue = out_queue

    def run(self) -> None:
        while True:
            text = self.input_queue.get()
            if text == END_OF_RESOURCES_SENTINEL:
                self.output_queue.put(END_OF_RESOURCES_SENTINEL)
                break
            else:
                sentences = [s.text for s in sentenize(text)]
                for s in sentences:
                    self.output_queue.put(s)
