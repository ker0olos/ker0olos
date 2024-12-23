[[ -f ~/.znap/zsh-snap/znap.zsh ]] ||
    git clone --depth 1 https://github.com/marlonrichert/zsh-snap.git ~/.znap/zsh-snap

source ~/.znap/zsh-snap/znap.zsh

HISTFILE=~/.zsh_history

FPATH=$FPATH:$HOME/.bin/_completions

ZSH_AUTOSUGGEST_STRATEGY=(completion)

# znap

# znap source marlonrichert/zsh-autocomplete
znap source zsh-users/zsh-autosuggestions
znap source zsh-users/zsh-syntax-highlighting

source ~/plugins/zsh-autocomplete/zsh-autocomplete.plugin.zsh

# znap prompt sindresorhus/pure
# znap prompt spaceship-prompt/spaceship-prompt

# load zeit 
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

# native

# eval "$(zoxide init zsh --cmd cd)"
# eval "$(thefuck --alias)"
eval "$(atuin init zsh)"

# aliases

# alias xdg-open="~/.bin/xdg-open"

# startx

#if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
#  exec startx
#fi
