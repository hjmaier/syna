# Building this fork

This branch targets **Hugo 0.168.0 or newer** and **Dart Sass 1.106.1 or newer**.
Those are the tested minimum versions. LibSass and older Hugo versions are no
longer supported. Newer versions still need to be checked when upgrading.

On macOS, install Hugo and the official Sass tap's compiler:

```sh
brew install hugo sass/sass/sass
hugo version
sass --version
hugo env
```

Use `brew upgrade` for tools already installed. Hugo must find the native Dart
Sass executable on `PATH`; the JavaScript-only npm `sass` package is not a
replacement for Hugo's embedded-protocol compiler. An unpacked official Sass
release also works when its directory is added to the build process's `PATH`.

From a website using this theme:

```sh
hugo --minify
hugo server --environment development
```

Sass source maps are generated only in development. Native Dart Sass includes
local file URLs in those debug maps, so do not deploy development outputs.

The theme ships its JavaScript and fonts. A website build does not require
`npm install`, Yarn, or a JavaScript rebuild. Install additional PostCSS tools
only if you deliberately enable `params.postcss`; that optional pipeline has
not been validated by the Sass migration tests.

## Project configuration

Use `locale = "de-DE"` (or the appropriate locale) instead of `languageCode`.
The theme reads `.Site.Language.Locale`, and language selectors use
`hugo.Sites`. Language buttons retain their existing `/language-code` links.

For a project previously using `disableKinds = ["RSS", "taxonomy",
"taxonomyTerm"]`, the behavior-preserving Hugo 0.168 replacement is
`disableKinds = ["rss", "taxonomy"]`. It leaves `term` enabled. Adding `term`
would change which pages Hugo generates.

## Sass sources and development dependencies

Bootstrap remains **4.5.1** and Font Awesome Free remains **5.14.0**. Their
vendored SCSS and Syna's SCSS use modules, namespaced built-ins, `math.div`,
modern color functions, and the current Sass `if()` syntax. Do not overwrite
these directories with the original npm package sources. License notices are
retained.

Bootstrap's helpers used during variable initialization are separated from
helpers consuming those variables to avoid a module cycle. Font Awesome's
shared variables are configured once. The RFS module explicitly reads
Bootstrap's responsive-font-size option, which remains disabled by default. Theme colors remain configurable through
`params.colors`; custom SCSS must import the modules whose members it uses.

The unused `node-sass` development dependency and its exclusive lockfile
dependencies are removed. The post-install hook only copies webfonts; it does
not replace migrated SCSS. The separate historical Webpack/Cypress development
stack has not been rebuilt or modernized by this change.

Run the synthetic tests with the selected Hugo binary and Dart Sass on `PATH`:

```sh
python3 _tests/hugo-compat/test_compatibility.py --hugo /absolute/path/to/hugo
```

See [_tests/hugo-compat/README.md](_tests/hugo-compat/README.md) for coverage and
limits. Success cases fail the tests if Hugo reports warnings. No warning
suppression is configured.

CI or hosting systems that build sources must install the same Hugo and native
Dart Sass prerequisites first. The historical demo Netlify/Cypress files still
pin older tooling and are not validated build recipes for this branch; port
those separately before using them. Hosting that only serves generated HTML
does not need either compiler.
