from contextlib import ExitStack as DoesNotRaise

import pytest

from supervision import Detections

from typing import Optional, Union

import numpy as np


@pytest.mark.parametrize(
    'detections, index, expected_result, exception',
    [
        (

        )
    ]
)
def test_getitem(
        detections: Detections,
        index: Union[int, slice, np.ndarray],
        expected_result: Optional[Detections],
        exception: Exception
) -> None:
    with exception:
        result = detections[index]
        assert result == expected_result
