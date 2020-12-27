from multiprocessing import Queue, Process
from pathlib import Path
from typing import Union

from normalizer_data.processors.sentinels import END_OF_RESOURCES_SENTINEL


class TextsReaderProcess(Process):
    """
    Recursively finds all .txt files and stores their data into queue.
    """
    def __init__(self, directory_path: Union[str, Path], out_text_queue: Queue):
        super().__init__(daemon=True)
        self.output_queue = out_text_queue
        self.all_texts = list(Path(directory_path).glob('**/*.txt'))

    def run(self) -> None:
        for i, text in self.all_texts:
            with open(str(text)) as input_file:
                text_data = input_file.read().strip()
                self.output_queue.put((i, text_data))
        self.output_queue.put(END_OF_RESOURCES_SENTINEL)
