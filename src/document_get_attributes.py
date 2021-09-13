import random
import string

import numpy as np
import pytest
from jina import Document

from .utils.benchmark import benchmark_time
from .pages import Pages


def _generate_random_text(text_length):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(text_length)
    )


def _generate_random_buffer(buffer_length):
    return bytes(bytearray(random.getrandbits(8) for _ in range(buffer_length)))


def _generate_random_blob(num_dims):
    # 1 and 3 can cover from audio signals to images. 3 dimensions make the memory too high
    shape = [random.randint(100, 200)] * num_dims

    return np.random.rand(*shape)


NUM_DOCS = 10000


@pytest.mark.parametrize('text_length', [10, 100, 1000, 10000])
def test_get_attributes_text(name, text_length, json_writer):
    def _doc_get(doc):
        _ = doc.get_attributes(*['text'])

    mean_time, std_time = benchmark_time(
        _doc_get,
        NUM_DOCS,
        kwargs=dict(doc=Document(text=_generate_random_text(text_length))),
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DOCUMENT_GET_ATTRIBUTES,
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(text_length=text_length),
        )
    )


@pytest.mark.parametrize('num_dims', [1, 2])
def test_get_attribute_blob(name, num_dims, json_writer):
    def _doc_get(doc):
        _ = doc.get_attributes(*['blob'])

    mean_time, std_time = benchmark_time(
        _doc_get,
        NUM_DOCS,
        kwargs=dict(doc=Document(blob=_generate_random_blob(num_dims))),
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DOCUMENT_GET_ATTRIBUTES,
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_dims=num_dims),
        )
    )


@pytest.mark.parametrize('buffer_length', [10, 1000, 100000])
def test_get_attribute_buffer(name, buffer_length, json_writer):
    def _doc_get(doc):
        _ = doc.get_attributes(*['buffer'])

    mean_time, std_time = benchmark_time(
        _doc_get,
        NUM_DOCS,
        kwargs=dict(doc=Document(buffer=_generate_random_buffer(buffer_length))),
    )

    json_writer.append(
        dict(
            name=name,
            page=Pages.DOCUMENT_GET_ATTRIBUTES,
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(buffer_length=buffer_length),
        )
    )
