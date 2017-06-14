#!/usr/bin/env bash


SERVER_IP="${SERVER_IP:-128.199.96.206}"
SSH_USER="root"
SSH_SERVER="${SSH_USER}@${SERVER_IP}"
APP_NAME="Pronto"
eval IDENTITY_FILE="${HOME}/.ssh/id_rsa_do1"


function git_init () {
    local DIRECTORY="/var/www/${APP_NAME}"
    echo "Initialize git repo and hooks..."
    echo "Current Directory: $(pwd)"

    scp -i  "${IDENTITY_FILE}" "./configs/post-receive" "${SSH_SERVER}:/tmp/post-receive"
    ssh -t -i "${IDENTITY_FILE}" "${SSH_SERVER}" bash -c "'
sudo apt-get update && sudo apt-get install -y -q git
sudo rm -rf ${DIRECTORY}.git ${DIRECTORY}
sudo mkdir -p ${DIRECTORY}.git ${DIRECTORY}
sudo git --git-dir=${DIRECTORY}.git --bare init

sudo mv /tmp/post-receive ${DIRECTORY}.git/hooks/post-receive
sudo chmod +x ${DIRECTORY}.git/hooks/post-receive
sudo chown -R ${SSH_USER}:${SSH_USER} ${DIRECTORY}.git
sudo chown -R ${SSH_USER}:${SSH_USER} ${DIRECTORY}
'"
    echo "Done!"
}

function git_remote_add () {
    echo "Setting up git remotes..."
#    local REMOTE="ssh://${SSH_USER}@${SERVER_IP}:/var/www/${APP_NAME}.git"
    local REMOTE="${SSH_USER}@{$APP_NAME}-push:/var/www/${APP_NAME}.git"
    git remote remove production
    git remote add production ${REMOTE}
    echo "Done!"
}

function setup () {
    git_init
    git_remote_add
}

function copy_post_receive () {
    echo "Copying post receive from present location to server"
    scp -i  "${IDENTITY_FILE}" "./configs/post-receive" "${SSH_SERVER}:/var/www/${APP_NAME}.git/hooks/post-receive"
    echo "Done"
}

function help_menu () {
cat << EOF
Usage: deploy ( -h | -r | -c | -s )

OPTIONS:
   -h|--help                  Show this message
   -c|--copy                  Copies post receive hook from config folder to server .git hook
   -r|--remote                Adds the remote for the server
   -s|--setup                 Setups environment for server and development and adds remote

EXAMPLES:
  Sets up the server. Only do this once:
       $ deploy -s

EOF
}

# If no commands
if (( $# == 0 )); then
  help_menu
fi

while [[ $# > 0 ]]
do
case "${1}" in
  -c|--copy)
  copy_post_receive
  shift
  ;;
  -r|--remote)
  git_remote_add
  shift
  ;;
  -s|--setup)
  setup
  shift
  ;;
  -h|--help)
  help_menu
  shift
  ;;
  *)
  echo "${1} is not a valid flag, try running: ${0} --help"
  shift
  ;;
esac
done
