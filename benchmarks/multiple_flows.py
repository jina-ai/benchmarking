import os

from jina import Document, Flow
from memory_profiler import profile as memory_profiler

output_dir = os.path.join(os.getcwd().replace('/benchmarks', ''), 'outputs')
fp = open(
    os.path.join(
        output_dir,
        '{}_memory_profile.txt'.format(os.path.basename(__file__)).replace('.py', ''),
    ),
    'w+',
)


def __doc_generator():
    # Document generator
    for i in range(1000):
        yield Document(
            text=f'This is the document number: {i}',
        )


@memory_profiler(stream=fp)
def benchmark():
    fs = [
        Flow().add(),
        Flow().add().add(),
        Flow().add().add().add(),
        Flow().add().add().add(needs='gateway'),
    ]

    for f in fs:
        with f:
            f.post(on='/', inputs=__doc_generator, request_size=10)


if __name__ == '__main__':
    benchmark()
    fp.close()
