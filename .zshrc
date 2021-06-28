export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="zeit"

plugins=(
  git
  zsh-autosuggestions
  history-substring-search
  zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh

alias play="spt.py play"

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
