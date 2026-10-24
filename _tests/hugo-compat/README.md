# Hugo and Dart Sass regression tests

Requires Python 3 (standard library only), Hugo 0.168.0 or newer, and native
Dart Sass 1.106.1 or newer on the test process's `PATH`. The tested tool pair is
Homebrew Hugo 0.168.0 (`extended+withdeploy`, darwin/arm64) and the official
Dart Sass 1.106.1 macOS arm64 release. Older Hugo and LibSass are not targets.

```sh
python3 _tests/hugo-compat/test_compatibility.py --hugo /absolute/path/to/hugo
```

Use `--group language`, `paths`, `css`, `navigation`, `repositories`, or `smoke`
to review an area separately. `--theme-root /path/to/syna` selects the theme
under test. `--artifacts /new/output/path` preserves synthetic fixtures, exact
commands, output, and build logs; otherwise temporary directories are removed.
No private website content or public API is used.

Coverage:

- German/English page resources, global fallback, local precedence, headless
  `_index/index` bundles, and generated 404 pages without a backing file.
- The real theme head partial in development and production, Sass compilation,
  minification, fingerprint references, and responsive fonts disabled by default
  or explicitly enabled. PostCSS is not enabled: it requires
  separately installed tools and needs its own integration test.
- Navigation with one and two languages and the existing language button URLs.
- Remote repository sorting, limits, forks, allowlist, empty data, HTTP 404/500,
  and invalid JSON, using a short-lived server on a free `127.0.0.1` port.
  Only a temporary partial copy redirects the API origin; its HTTP allowlist is
  restricted to that local endpoint. A prohibited localhost server is an
  environment error, not a passing test.
- A complete theme build with real assets, configured colors propagated through
  Sass modules, locale attributes, search JSON, home/section/regular pages, and
  global navigation/hero/not-found fragments on the 404 page.

Successful builds must emit no warnings. The suite does not rebuild JavaScript,
run the historical Cypress/Netlify setup, or prove browser behavior for every
optional fragment. See [BUILDING.md](../../BUILDING.md) for the supported local
build workflow and the separate legacy development-stack limitations.
