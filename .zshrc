[[ -f ~/.znap/zsh-snap/znap.zsh ]] ||
    git clone --depth 1 -- \
        https://github.com/marlonrichert/zsh-snap.git ~/.znap/zsh-snap

source ~/.znap/zsh-snap/znap.zsh

# setup zsh history

HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY
FPATH=$FPATH:$HOME/.bin/_completions

# znap

ZSH_AUTOSUGGEST_STRATEGY=(history completion)

znap source zsh-users/zsh-autosuggestions
znap source zsh-users/zsh-syntax-highlighting
# znap source zsh-users/zsh-history-substring-search
znap source marlonrichert/zsh-autocomplete

znap prompt sindresorhus/pure

# load zeit 
# znap source ohmyzsh/ohmyzsh lib/{git,theme-and-appearance}
# local resetColor="%{$reset_color%}"
# local prefix="▲"
# local dir="%{$fg_bold[white]%}%c$resetColor$resetColor"
# PROMPT='$prefix $dir $(git_prompt_info)'
# ZSH_THEME_GIT_PROMPT_PREFIX="at %{$fg_bold[white]%}"
# ZSH_THEME_GIT_PROMPT_SUFFIX="$resetColor "
# ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg_bold[red]%} ✖"
# ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg_bold[green]%} ✔"
# znap prompt

# native

eval "$(zoxide init zsh --cmd cd)"
eval $(thefuck --alias)

# aliases

alias xdg-open="~/.bin/xdg-open"

# startx

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
  exec startx
fi
