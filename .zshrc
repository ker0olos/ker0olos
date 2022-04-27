export ZSH="$HOME/.oh-my-zsh"

export NVM_LAZY_LOAD=true
export NVM_COMPLETION=true

ZSH_THEME="zeit"

plugins=(
  git
  zsh-nvm
  zsh-autosuggestions
  history-substring-search
  zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh

alias xdg-open="~/.bin/xdg-open"

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
