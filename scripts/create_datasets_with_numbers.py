import argparse
from multiprocessing import get_context
from multiprocessing.queues import Queue
from pathlib import Path

from normalizer_data.processors.readers import TextsReaderProcess
from normalizer_data.processors.samples_producers import NumbersNormalizationProducer
from normalizer_data.processors.sentence_tokenizers import SentenceTokenizerProcess
from normalizer_data.processors.writers import TextsWriterProcess

MAX_TEXT_QUEUE_SIZE = 2000
MAX_SENTENCES_QUEUE_SIZE = 10000


def parse_args():
    parser = argparse.ArgumentParser(description='Run Tacotron experiment')
    parser.add_argument(
        '--texts_path', type=Path, required=True,
        help='Path to directory with texts to build dataset_from.'
    )
    parser.add_argument(
        '--output_path', type=Path, required=True,
        help='Path to store dataset.'
    )
    parser.add_argument(
        '--processes_tokenizing', type=int, required=False, default=2,
        help='Numbers of processes to work with.'
    )
    parser.add_argument(
        '--processes_producing', type=int, required=False, default=8,
        help='Numbers of processes to work with.'
    )
    parser.add_argument(
        '--max_samples', type=int, required=False, default=1e10,
        help='Maximum numbers of collected samples.'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = parse_args()

    texts_queue = Queue(maxsize=MAX_TEXT_QUEUE_SIZE, ctx=get_context())
    sentences_queue = Queue(maxsize=MAX_SENTENCES_QUEUE_SIZE, ctx=get_context())
    pairs_queue = Queue(maxsize=MAX_SENTENCES_QUEUE_SIZE, ctx=get_context())

    reader = TextsReaderProcess(directory_path=args.texts_path, out_text_queue=texts_queue)
    sentence_tokenizers = [
        SentenceTokenizerProcess(input_queue=texts_queue, out_queue=sentences_queue)
        for _ in range(args.processes_tokenizing)
    ]
    samples_producers = [
        NumbersNormalizationProducer(input_queue=sentences_queue, out_queue=pairs_queue)
        for _ in range(args.processes_producing)
    ]
    writer = TextsWriterProcess(out_path=args.output_path, input_queue=pairs_queue, max_samples=args.max_samples)

    reader.start()
    [p.start() for p in sentence_tokenizers]
    [p.start() for p in samples_producers]

    writer.start()
    writer.join()
