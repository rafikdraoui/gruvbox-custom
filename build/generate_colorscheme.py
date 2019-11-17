from collections import namedtuple

import yaml

COLORSCHEME_NAME = "gruvbox-custom"
SOURCE_FILE = "./build/gruvbox.yaml"
OUTPUT_FILE = f"./colors/{COLORSCHEME_NAME}.vim"
FTPLUGIN_DIR = "./after/ftplugin"
LIGHTLINE_PALETTE_FILE = "./_gruvbox_lightline_palette.vim"


Highlight = namedtuple(
    "Highlight", ["name", "link", "fg", "bg", "gui", "guisp"], defaults=[None] * 5
)


def parse_colorscheme_template():
    with open(SOURCE_FILE) as f:
        data = f.read()
    return yaml.safe_load(data)


def make_color_table(colors):
    palette = colors["palette"]
    main_colors = colors["aliases"]

    result = {name: palette[value] for name, value in main_colors.items()}
    result.update({"fg": "fg", "bg": "bg", "NONE": "NONE"})
    return result


def make_highlight_command(color_table, highlight):
    if highlight.link:
        return f"hi! link {highlight.name} {highlight.link}"

    fg = color_table.get(highlight.fg)
    bg = color_table.get(highlight.bg)
    gui = highlight.gui
    guisp = color_table.get(highlight.guisp)

    result = [f"hi {highlight.name}"]
    if fg:
        result.append(f"guifg={fg}")
    if bg:
        result.append(f"guibg={bg}")
    if gui:
        result.append(f"gui={gui}")
    if guisp:
        result.append(f"guisp={guisp}")
    return " ".join(result)


def make_terminal_colors_variable(colors):
    palette = colors["palette"]
    terminal_colors = colors["terminal"]

    return [
        f"let g:terminal_{name} = '{palette[value]}'"
        for name, value in terminal_colors.items()
    ]


def make_fzf_colors(fzf_colors):
    result = ["let g:fzf_colors = {"]
    result += [rf"\ '{name}': ['fg', '{hl}']," for name, hl in fzf_colors.items()]
    result += [r"\ }"]
    return "\n".join(result)


def get_ftplugins_highlights(color_table, ftplugins):
    result = {}
    for ft_name, ft_highlights in ftplugins.items():
        highlight_cmds = [
            make_highlight_command(color_table, Highlight(name=name, **attrs))
            for name, attrs in ft_highlights.items()
        ]
        result[ft_name] = highlight_cmds
    return result


def make_lightline_palette(color_table, lightline):
    p = {}
    for mode, config in lightline.items():
        p[mode] = {}
        for where, component_highlights in config.items():
            p[mode][where] = [
                [color_table.get(attr, attr) for attr in hl]
                for hl in component_highlights
            ]
    return p


def write_colorscheme(highlight_cmds, terminal_colors_variables, fzf_colors):
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"let g:colors_name='{COLORSCHEME_NAME}'\n")
        for line in highlight_cmds + terminal_colors_variables:
            f.write(f"{line}\n")
        f.write(f"{fzf_colors}\n")


def write_ftplugins(ftplugins_highlights):
    for ft_name, highlight_cmds in ftplugins_highlights.items():
        with open(f"{FTPLUGIN_DIR}/{ft_name}.vim", "w") as f:
            for line in highlight_cmds:
                f.write(f"{line}\n")


def write_lightline_colorscheme(lightline_palette):
    with open(LIGHTLINE_PALETTE_FILE, "w") as f:
        f.write(f"let palette = lightline#colorscheme#fill({lightline_palette})\n")


def main():
    sections = parse_colorscheme_template()
    color_table = make_color_table(sections["colors"])

    highlight_cmds = [
        make_highlight_command(color_table, Highlight(name=name, **attrs))
        for name, attrs in sections["highlights"].items()
    ]
    terminal_colors_variables = make_terminal_colors_variable(sections["colors"])
    fzf_colors = make_fzf_colors(sections["fzf_colors"])
    write_colorscheme(highlight_cmds, terminal_colors_variables, fzf_colors)

    ftplugins_highlights = get_ftplugins_highlights(color_table, sections["ftplugins"])
    write_ftplugins(ftplugins_highlights)

    lightline_palette = make_lightline_palette(color_table, sections["lightline"])
    write_lightline_colorscheme(lightline_palette)


if __name__ == "__main__":
    main()
