from collections import namedtuple

import yaml

COLORSCHEME_NAME = "gruvbox-custom"
SOURCE_FILE = "./build/gruvbox.yaml"
OUTPUT_FILE = f"./colors/{COLORSCHEME_NAME}.vim"
FTPLUGIN_DIR = "./after/ftplugin"


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


def get_ftplugins_highlights(color_table, ftplugins):
    result = {}
    for ft_name, ft_highlights in ftplugins.items():
        highlight_cmds = [
            make_highlight_command(color_table, Highlight(name=name, **attrs))
            for name, attrs in ft_highlights.items()
        ]
        result[ft_name] = highlight_cmds
    return result


def write_colorscheme(highlight_cmds, terminal_colors_variables):
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"let g:colors_name='{COLORSCHEME_NAME}'\n")
        for line in highlight_cmds + terminal_colors_variables:
            f.write(f"{line}\n")


def write_ftplugins(ftplugins_highlights):
    for ft_name, highlight_cmds in ftplugins_highlights.items():
        with open(f"{FTPLUGIN_DIR}/{ft_name}.vim", "w") as f:
            for line in highlight_cmds:
                f.write(f"{line}\n")


def main():
    sections = parse_colorscheme_template()
    color_table = make_color_table(sections["colors"])

    highlight_cmds = [
        make_highlight_command(color_table, Highlight(name=name, **attrs))
        for name, attrs in sections["highlights"].items()
    ]
    terminal_colors_variables = make_terminal_colors_variable(sections["colors"])
    write_colorscheme(highlight_cmds, terminal_colors_variables)

    ftplugins_highlights = get_ftplugins_highlights(color_table, sections["ftplugins"])
    write_ftplugins(ftplugins_highlights)


if __name__ == "__main__":
    main()
