[[ -f ~/.znap/zsh-snap/znap.zsh ]] ||
    git clone --depth 1 -- \
        https://github.com/marlonrichert/zsh-snap.git ~/.znap/zsh-snap

source ~/.znap/zsh-snap/znap.zsh

export HISTSIZE=200

# znap

ZSH_AUTOSUGGEST_STRATEGY=(history)
znap source zsh-users/zsh-autosuggestions

znap source zsh-users/zsh-syntax-highlighting
znap source zsh-users/zsh-history-substring-search

znap source marlonrichert/zsh-autocomplete

# load ohmyzsh theme 

znap source ohmyzsh/ohmyzsh lib/{git,theme-and-appearance}

local resetColor="%{$reset_color%}"
local prefix="▲"
local dir="%{$fg_bold[white]%}%c$resetColor$resetColor"
PROMPT='$prefix $dir $(git_prompt_info)'
ZSH_THEME_GIT_PROMPT_PREFIX="at %{$fg_bold[white]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="$resetColor "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg_bold[red]%} ✖"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg_bold[green]%} ✔"

znap prompt

# fix history-substring

bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down

# native

eval "$(zoxide init zsh --cmd cd)"

alias xdg-open="~/.bin/xdg-open"
alias rm="rip --graveyard /home/$USER/.local/share/Trash/files/"

# startx

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
