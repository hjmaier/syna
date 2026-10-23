# Fragment language regression test

Requires Python 3 (standard library only) and an explicitly selected Hugo binary:

```sh
python3 _tests/hugo-compat/test_compatibility.py --hugo /absolute/path/to/hugo
```

The test creates synthetic German and English page bundles and checks that the
fragment helper selects exactly the matching language in each output. It copies
the real fragment helper and its dependency into a temporary fixture; no public
API, private website, or JavaScript build dependencies are used.

Use `--theme-root /path/to/original/syna` to reproduce the failure with unmodified
theme code. Use `--artifacts /new/output/path` to retain generated fixtures,
Hugo commands, and build logs; otherwise temporary files are removed.

This is an isolated test of fragment language selection, not a claim that the
complete theme supports the tested Hugo version. Other compatibility fixes are
outside this change. Existing Hugo warnings remain visible.
