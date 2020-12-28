from multiprocessing import Queue, Process

from normalizer_data.numericals.extractor import NumberExtractor
from normalizer_data.processors.sentinels import END_OF_RESOURCES_SENTINEL
from normalizer_data.sample_builder import build_sample
from normalizer_data.shorteners.shorteners_model import get_shorteners_model


class NumbersNormalizationProducer(Process):
    """
    Computes pairs 'normalized'/'denormalized' text and puts them into output queue.
    """
    def __init__(self, input_queue: Queue, out_queue: Queue):
        super().__init__(daemon=True)
        self.input_queue = input_queue
        self.output_queue = out_queue
        self.shortener_model = get_shorteners_model()
        self._extractor = None

    @property
    def extractor(self):
        if self._extractor is not None:
            return self._extractor
        else:
            self._extractor = NumberExtractor()
            return self._extractor

    def run(self) -> None:
        while True:
            sentence = self.input_queue.get()
            if sentence == END_OF_RESOURCES_SENTINEL:
                self.output_queue.put(END_OF_RESOURCES_SENTINEL)
                break
            else:
                text_num, sentence = sentence
                result = build_sample(sentence, self.extractor, self.shortener_model)
                if result is not None:
                    replaced, num_changes, changes = result
                    string_to_write = sentence + '<sep>' + replaced
                    self.output_queue.put((text_num, string_to_write, num_changes, changes))
