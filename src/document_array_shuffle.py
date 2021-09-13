import pytest
from jina import Document, DocumentArray
from jina.types.arrays.memmap import DocumentArrayMemmap

from .utils.benchmark import benchmark_time
from .pages import Pages

NUM_REPETITIONS = 5


@pytest.mark.parametrize('memmap', [False, True])
@pytest.mark.parametrize("n_docs", [1000, 10_000])
def test_da_shuffle(name, memmap, n_docs, ephemeral_tmpdir, json_writer):
    def _setup(memmap, n_docs):
        docs = [Document(text=f"Document{i}") for i in range(n_docs)]
        da = (
            DocumentArrayMemmap(f'{str(ephemeral_tmpdir)}/memmap')
            if memmap
            else DocumentArray()
        )
        da.extend(docs)
        return (), dict(da=da)

    def _shuffle_da(da):
        da.shuffle()

    def _teardown():
        import os
        import shutil

        if os.path.exists(f'{str(ephemeral_tmpdir)}/memmap'):
            shutil.rmtree(f'{str(ephemeral_tmpdir)}/memmap')

    mean_time, std_time = benchmark_time(
        setup=_setup,
        func=_shuffle_da,
        teardown=_teardown,
        n=NUM_REPETITIONS,
        kwargs=dict(memmap=memmap, n_docs=n_docs),
    )
    if memmap:
        name = name.replace('_da_', '_dam_')
    json_writer.append(
        dict(
            name=name,
            page=Pages.DA_SHUFFLE,
            iterations=NUM_REPETITIONS,
            mean_time=mean_time,
            std_time=std_time,
            unit="ms",
            metadata=dict(n_nodes=memmap, n_docs=n_docs),
        )
    )
