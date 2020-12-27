from multiprocessing import Queue, Process
from pathlib import Path
from typing import Union, Optional

from tqdm import tqdm

from normalizer_data.processors.sentinels import END_OF_RESOURCES_SENTINEL


class TextsWriterProcess(Process):
    """
    Recursively finds all .txt files and stores their data into queue.
    """
    def __init__(self, out_path: Union[str, Path], input_queue: Queue, max_samples: int = 1e6):
        super().__init__(daemon=True)
        self.input_queue = input_queue
        self.out_path = out_path
        self.max_samples = max_samples

    def run(self) -> None:
        number_of_collected_samples = 0
        max_text_num = 0
        with open(self.out_path, 'w') as output_file:
            infobar = tqdm(desc='Writing of collected samples')
            while True:
                sample_to_write = self.input_queue.get()
                if (sample_to_write == END_OF_RESOURCES_SENTINEL) or (number_of_collected_samples > self.max_samples):
                    break
                else:
                    text_num, sample_to_write = sample_to_write
                    output_file.write(sample_to_write + '\n<sample_sep>\n')
                    number_of_collected_samples += 1
                    max_text_num = max(max_text_num, text_num)
                    infobar.set_postfix_str(f'Collected: {number_of_collected_samples}, texts processed: {max_text_num}')
