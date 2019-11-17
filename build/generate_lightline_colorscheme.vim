" Generate expanded lightline palette from a gui-only palette. Speeds up load
" time by 80% by avoiding loading and calling `lightline#colorscheme#fill`.
" See `:help lightline-colorscheme`

" load fullly expanded lightline palette
packadd! lightline.vim
source _gruvbox_lightline_palette.vim

" put palette into register `a`
redir @a
silent echo palette
redir END

" clear existing colorscheme
edit autoload/lightline/colorscheme/gruvbox_custom.vim
%delete

" write it down
put! ='  let g:lightline#colorscheme#gruvbox_custom#palette = '
put a
%join
put! ='if exists(\"g:lightline\")'
normal! G
put ='endif'

silent wq
