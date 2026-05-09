import sys
import time
from typing import Iterable, Iterator, Optional, TypeVar


T = TypeVar("T")


def progress_iter(iterable: Iterable[T], desc: str = "Progress", total: Optional[int] = None) -> Iterator[T]:
    """Yield items while printing lightweight progress without third-party dependencies."""
    start_time = time.time()

    for index, item in enumerate(iterable, start=1):
        yield item

        if total:
            elapsed = time.time() - start_time
            rate = index / elapsed if elapsed > 0 else 0.0
            sys.stderr.write(f"\r{desc}: {index}/{total} [{rate:.2f}it/s]")
            sys.stderr.flush()
        else:
            sys.stderr.write(f"\r{desc}: {index}")
            sys.stderr.flush()

    sys.stderr.write("\n")
    sys.stderr.flush()
