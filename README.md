# gruvbox-custom

**The [gruvbox][] vim colorscheme, optimized for loading speed**

On my computer, the default [gruvbox colorscheme][gruvbox] takes 12.000ms to
load when opening an empty buffer (nearly twice as long as loading all of
`$VIMRUNTIME`, and longer than loading all other 20 plugins combined) while
this version takes 0.825ms (slightly faster than vim-fugitive).

**Note:** I'm not using this exact colorscheme anymore. I used it as a base to
make the simpler [couleurs.vim][] that leverages tree-sitter highlighting.

## How?

The main gain is achieved by having the vim colorscheme script be a list of
"raw" `:highlight` commands instead of making function calls that dynamically
build strings of highlight commands and `:execute` them. Further gains are made
by moving filetype-specific highlights to `ftplugin`s (although, see caveat
below).

This is done by configuring the colors and highlights in a YAML template, and
using it to compile optimized versions of `colors/gruvbox-custom.vim` and
`after/ftplugin/*.vim`.

## Caveats

There is no attempt at keeping any customizations: most of what I don't
personally need has been removed.

- Only GUI colors are defined (so it only works with `'termguicolors'`)
- Only the high-contrast dark-background variant is defined
- No configuration for plugins and file types I don't personally use
- No customizations through [`g:gruvbox_*` options][gruvbox-config]
- A few deviations from the original theme (some taken from
  [gruvbox-community][gruvbox-community]'s fork)
- Switching back-and-forth between colorschemes will break some highlights,
  since `gruvbox-custom` doesn't clear highlights before loading, and its
  filetype-specific highlights are defined in `ftplugin`.

It should be possible to support customizations by adding new attributes to the
highlight records in the YAML template and modifying
`build/generate_colorscheme.py` to emit different commands based on them
wrapped in if-else blocks.

## See also

[couleurs.vim][]


[gruvbox]: https://github.com/morhetz/gruvbox
[gruvbox-community]: https://github.com/gruvbox-community/gruvbox
[gruvbox-config]: https://github.com/morhetz/gruvbox/wiki/Configuration
[couleurs.vim]: https://github.com/rafikdraoui/couleurs.vim
