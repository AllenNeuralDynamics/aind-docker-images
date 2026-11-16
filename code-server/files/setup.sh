#!/bin/bash

# link in vscode settings
rm /root/capsule/code/.vscode/Machine/settings.json
ln -s /.files/vscode_machine_settings.json /root/capsule/code/.vscode/Machine/settings.json

# add mcp settings to vscode if not already present
VSCODE_DIR=/root/capsule/code/.vscode/User/
VSCODE_CONFIG="$VSCODE_DIR/mcp.json"
if [ ! -f "$VSCODE_CONFIG" ]; then
  mkdir -p $VSCODE_DIR
  cp /.files/mcp.json "$VSCODE_CONFIG"
fi

DIRECTORY=/root/.dotfiles
# install dotfiles via git if $DOTFILES_REPO is set
# TODO: move this into chezmoi scripts in dotfiles instead?
if test -n "$DOTFILES_REPO"; then
  if [ -d "$DIRECTORY" ]; then
    echo "updating dotfiles"
    cd $DIRECTORY
    git pull
  else
    echo "installing dotfiles"
    git clone $DOTFILES_REPO $DIRECTORY --depth 1
    cd $DIRECTORY
  fi
  # install script should be idempotent, fast, and ideally not overwrite user changes
  bash install.sh
  cd -
fi