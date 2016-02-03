# format-js-sublime
Sublime plugin to integrate with format-js-cli

# Installation

- Clone this repository into your packages.

_(Maybe at: `/Users/<username>/Library/Application\ Support/Sublime\ Text\ 3/Packages`)_

- Then install the format-js-cli that contains the appropriate node scripts.

```
npm install -g format-js-cli
```

- Add the correct path to `format-js-cli/bin/formatjs` to your settings. Edit your `Preferences.sublime-settings` (brought up with `cmd+,`) to contain the `formatjs_path` setting.

```
{
  "formatjs_path": "~/node_modules/format-js-cli/bin/formatjs"
}
```

_(If the command `formatjs` is on your path you can use the command `which formatjs` to find the correct path to put here)_

- Run the command! Open a javascript file and the default keyboard shortcut is `super-shift-i`, or you can change the hotkey by modifying your keymap:

```
{ "keys": ["super+shift+f"], "command": "format_js" }
```
