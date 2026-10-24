# Hugo compatibility regression tests

These tests use Python 3's standard library and an explicitly selected Hugo
binary. They do not install dependencies, rebuild JavaScript, or use any private
website. All content, configuration, and remote API responses are synthetic.

Run the complete suite with Hugo Extended:

```sh
python3 _tests/hugo-compat/test_compatibility.py --hugo /absolute/path/to/hugo
```

Use `--group language`, `paths`, `css`, `navigation`, `repositories`, or `smoke`
to review each fix separately. Use `--theme-root /path/to/unmodified/syna` to
check a regression against the original source. `--artifacts /new/output/path`
preserves generated fixtures, exact build commands, output, and build logs;
without it, temporary directories are removed at the end of each test.

The repository tests bind a short-lived HTTP server to `127.0.0.1` on an
automatically selected port. Only in the temporary fixture, they replace the
fixed GitHub API origin with this local origin. Hugo's HTTP allowlist is
restricted to that exact local endpoint. No requests are sent to GitHub.
Environments that prohibit binding or contacting localhost must allow this
group separately; such failures are environment errors, not passing tests.

Coverage:

- Language-specific page fragments, default-language global fallback, local
  precedence, the headless `_index/index` bundle, and global fragments on
  generated 404 pages that have no backing content file.
- The actual theme head partial in development and production, including Sass,
  minification, and fingerprint references. PostCSS is deliberately not enabled:
  it needs separately installed `postcss` / `postcss-cli` dependencies.
- Navigation with one and two languages.
- Repository sorting, count, fork exclusion, allowlist, empty results, HTTP
  404/500, and invalid JSON.
- A complete synthetic theme build with actual theme assets, HTML and search
  JSON, homepage and section fragments, a regular page, navigation, and a 404
  page with global navigation, hero, and the not-found fragment.

The language, path, CSS, navigation, and full-theme groups also run on Hugo
0.88.1 Extended. The repository group requires `resources.GetRemote`, introduced
in Hugo 0.91.0; `theme.toml` therefore declares this new minimum. Hugo 0.91.0
and 0.122.0 have not been installed or tested by this change.

The complete suite has been run with Homebrew's Hugo 0.168.0
(`extended+withdeploy`, darwin/arm64). The other five groups have also been run
with Hugo 0.88.1 Extended. These results do not establish support for every
intermediate version or for optional PostCSS, which requires additional tools.

The suite does not suppress deprecation warnings or validate browser behavior.
Remaining warnings (including LibSass, `.Page.Sites`, and `.Site.LanguageCode`)
should be assessed separately from these compatibility fixes.
