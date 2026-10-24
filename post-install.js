const fs = require('fs');

// SCSS is vendored and migrated to Dart Sass modules. Never overwrite it with
// the legacy npm packages during a dependency install.
fs.cpSync('./node_modules/@fortawesome/fontawesome-free/webfonts', './static/fonts', {
  recursive: true,
});
