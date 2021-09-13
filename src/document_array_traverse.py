import pytest
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages

NUM_REPETITIONS = 5


def _get_docs(num_docs):
    return [Document(text=f'This is the document number: {i}') for i in range(num_docs)]


def _build_da(num_docs, num_matches, num_chunks):
    da = DocumentArray(_get_docs(num_docs))
    for doc in da:
        if num_matches > 0:
            doc.matches.extend(_get_docs(num_matches))
        if num_chunks > 0:
            doc.chunks.extend(_get_docs(num_matches))

    return da


@pytest.mark.parametrize(
    'num_docs,num_matches,num_chunks',
    [
        (10, 10, 10, ['r', 'c', 'm']),
        (100, 100, 100, ['r', 'c', 'm']),
        (1000, 1000, 1000, ['r', 'c', 'm']),
        (1000, 10, 10, ['r']),
        (1000, 10, 1000, ['c']),
        (1000, 1000, 10, ['m']),
    ],
)
@pytest.mark.parametrize('memmap', [False, True])
def test_da_traverse_flat(
    name,
    num_docs,
    num_matches,
    num_chunks,
    traversal_paths,
    memmap,
    json_writer,
    ephemeral_tmpdir,
):
    if num_docs == 1000 and num_chunks == 1000 and num_matches == 1000:
        pytest.skip('problems with memory')

    def _traverse_flat(da):
        da.traverse_flat(traversal_paths)

    def _build_da():
        docs = _get_docs(num_docs)
        for doc in docs:
            if num_matches > 0:
                doc.matches.extend(_get_docs(num_matches))
            if num_chunks > 0:
                doc.chunks.extend(_get_docs(num_matches))

        da = (
            DocumentArray()
            if not memmap
            else DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap')
        )
        da.extend(docs)

        return (), dict(da=da)

    mean_time, std_time = benchmark_time(
        setup=_build_da, func=_traverse_flat, n=NUM_REPETITIONS
    )
    if memmap:
        name = name.replace('_da_', '_dam_')
    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_TRAVERSE,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(
                num_docs=num_docs,
                num_matches=num_matches,
                num_chunks=num_chunks,
                traversal_paths=traversal_paths,
                memmap=memmap,
            ),
        )
    )
