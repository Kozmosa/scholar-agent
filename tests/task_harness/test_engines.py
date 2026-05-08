from __future__ import annotations

import pytest

from ainrf.task_harness.engines import get_engine


def test_get_engine_unknown():
    with pytest.raises(ValueError, match="Unknown execution engine"):
        get_engine("unknown")
