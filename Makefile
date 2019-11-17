.PHONY: build

build:
	python build/generate_colorscheme.py
	nvim -u NONE --headless -S build/generate_lightline_colorscheme.vim
	rm _gruvbox_lightline_palette.vim
