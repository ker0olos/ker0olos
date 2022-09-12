[[ -f ~/.znap/zsh-snap/znap.zsh ]] ||
    git clone --depth 1 -- \
        https://github.com/marlonrichert/zsh-snap.git ~/.znap/zsh-snap

source ~/.znap/zsh-snap/znap.zsh

# ZSH_THEME="zeit"

# plugins=(
#   git
#   zsh-autosuggestions
#   history-substring-search
#   zsh-syntax-highlighting
# )

znap prompt sindresorhus/pure

alias xdg-open="~/.bin/xdg-open"

znap source marlonrichert/zsh-autocomplete
znap source zsh-users/zsh-autosuggestions
znap source zsh-users/zsh-syntax-highlighting
znap source zsh-users/zsh-history-substring-search

eval "$(zoxide init zsh --cmd cd)"

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
