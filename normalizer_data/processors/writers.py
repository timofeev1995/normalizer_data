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

    def _update_bar(self, bar, collected, text_num, numeric_changes, shortener_changes):
        bar.set_postfix_str(
            f'Collected: {collected}, texts processed: {text_num}, numeric_changes: {numeric_changes}, shortener_changes: {shortener_changes}'
        )

    def run(self) -> None:

        max_text_num = 0
        number_of_collected_samples = 0
        numeric_changes = 0
        shortener_changes = 0

        with open(self.out_path, 'w') as output_file:
            infobar = tqdm(desc='Writing of collected samples')
            while True:
                sample_to_write = self.input_queue.get()
                if (sample_to_write == END_OF_RESOURCES_SENTINEL) or (number_of_collected_samples > self.max_samples):
                    break
                else:
                    text_num, sample_to_write, num_changes, changes = sample_to_write
                    output_file.write(sample_to_write + '\n<sample_sep>\n')

                    number_of_collected_samples += 1
                    numeric_changes += num_changes
                    shortener_changes += changes
                    max_text_num = max(max_text_num, text_num)
                    self._update_bar(
                        infobar,
                        number_of_collected_samples,
                        max_text_num,
                        numeric_changes,
                        shortener_changes
                    )
