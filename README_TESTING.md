# Test suite – Team 4 A5/1

## Run
From this project directory, run:

```bash
python run_tests.py
```

No third-party Python package is required.

## What is covered
- TinyA5/1: key validation, output length, determinism, round trip, slide example,
  and the `process_bits()` API used by the demo.
- Standard A5/1: invalid key/frame, bit round trip, UTF-8 text round trip,
  frame-dependent output, and a published pedagogical A5/1 keystream vector.
- Demo smoke test: the TinyA5/1 demo must execute and print the trace.

## Important interpretation
Some tests are expected to fail against the repository as it currently stands.
They are regression checks that expose integration/correctness issues, not tests
that should be deleted just to make the report green. Fix the implementation and
re-run until all required tests pass.

The published A5/1 vector used here is from the pedagogical reference implementation:
key bytes `1223456789ABCDEF`, COUNT/frame `0x134`, A-to-B keystream
`534EAA582FE8151AB6E1855A728C00`. The test converts each key byte to LSB-first
bits because `StandardA51` accepts a bit string and consumes the string left to right.

A round-trip test alone does not prove standards conformance. The test vector is
the independent check for the standard implementation.

TinyA5/1 is a classroom toy algorithm, not suitable for protecting real data.
