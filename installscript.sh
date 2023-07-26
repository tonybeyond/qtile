#!/bin/bash
# ------------------------------------------------------
# Confirm Start
# ------------------------------------------------------

while true; do
    read -p "DO YOU WANT TO START THE INSTALLATION NOW? (Yy/Nn): " yn
    case $yn in
        [Yy]* )
            echo "Installation started."

        break;;
        [Nn]* ) 
            exit;
        break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# -------------------
# Install Paru
# -------------------
# Update system
sudo pacman -Syu --noconfirm

# Install paru AUR helper
sudo pacman -S --noconfirm --needed base-devel git
(cd /tmp && git clone https://aur.archlinux.org/paru.git && cd paru && makepkg -si)

# copy sources from git
git clone https://gitlab.com/stephan-raabe/dotfiles.git ~/dotfiles/
git clone https://github.com/tonybeyond/nixos_config.git ~/dotfiles/fish
git clone https://github.com/tonybeyond/nvim.git ~/dotfiles/mynvim
git clone https://github.com/jdpedersen1/polybar.git ~/dotfiles/polybar_git1
git clone https://github.com/thelinuxfraud/qtile.git ~/dotfiles/polybar_git2

# ------------------------------------------------------
# Install required packages
# ------------------------------------------------------
echo ""
echo "-> Install main packages"

packagesPacman=("nodejs" "neofetch" "tmux" "preload" "ly" "exa" "ranger" "fish" "open-vm-tools" "alacritty" "scrot" "nitrogen" "picom" "starship" "slock" "neovim" "rofi" "dunst" "ueberzug" "mpv" "xfce4-power-manager" "python-pip" "thunar" "mousepad" "ttf-font-awesome" "ttf-fira-sans" "ttf-fira-code" "ttf-firacode-nerd" "figlet" "cmatrix" "lxappearance" "polybar" "breeze" "breeze-gtk" "rofi-calc" "vlc" "python-psutil" "python-rich" "python-click");

packagesParu=("brave-bin" "pfetch" "bibata-cursor-theme" "shell-color-scripts");
    
# ------------------------------------------------------
# Function: Is package installed
# ------------------------------------------------------
_isInstalledPacman() {
    package="$1";
    check="$(sudo pacman -Qs --color always "${package}" | grep "local" | grep "${package} ")";
    if [ -n "${check}" ] ; then
        echo 0; #'0' means 'true' in Bash
        return; #true
    fi;
    echo 1; #'1' means 'false' in Bash
    return; #false
}

_isInstalledParu() {
    package="$1";
    check="$(paru -Qs --color always "${package}" | grep "local" | grep "${package} ")";
    if [ -n "${check}" ] ; then
        echo 0; #'0' means 'true' in Bash
        return; #true
    fi;
    echo 1; #'1' means 'false' in Bash
    return; #false
}

# ------------------------------------------------------
# Function Install all package if not installed
# ------------------------------------------------------
_installPackagesPacman() {
    toInstall=();

    for pkg; do
        if [[ $(_isInstalledPacman "${pkg}") == 0 ]]; then
            echo "${pkg} is already installed.";
            continue;
        fi;

        toInstall+=("${pkg}");
    done;

    if [[ "${toInstall[@]}" == "" ]] ; then
        # echo "All pacman packages are already installed.";
        return;
    fi;

    printf "Packages not installed:\n%s\n" "${toInstall[@]}";
    sudo pacman --noconfirm -S "${toInstall[@]}";
}

_installPackagesParu() {
    toInstall=();

    for pkg; do
        if [[ $(_isInstalledParu "${pkg}") == 0 ]]; then
            echo "${pkg} is already installed.";
            continue;
        fi;

        toInstall+=("${pkg}");
    done;

    if [[ "${toInstall[@]}" == "" ]] ; then
        # echo "All packages are already installed.";
        return;
    fi;

    printf "AUR ackages not installed:\n%s\n" "${toInstall[@]}";
    paru --noconfirm -S "${toInstall[@]}";
}

# ------------------------------------------------------
# Install required packages
# ------------------------------------------------------
_installPackagesPacman "${packagesPacman[@]}";
_installPackagesParu "${packagesParu[@]}";

# pywal requires dedicated installation
if [ -f /usr/bin/wal ]; then
    echo "pywal already installed."
else
    paru --noconfirm -S pywal
fi

# ------------------------------------------------------
# Enable services
# ------------------------------------------------------
sudo systemctl enable preload
sudo systemctl enable ly

# ------------------------------------------------------
# Create .config folder
# ------------------------------------------------------
echo ""
echo "-> Install .config folder"

if [ -d ~/.config ]; then
    echo ".config folder already exists."
else
    mkdir ~/.config
    echo ".config folder created."
fi

# ------------------------------------------------------
# Create symbolic links
# ------------------------------------------------------
echo ""
echo "-> Install symbolic links"

_installSymLink() {
    symlink="$1";
    linksource="$2";
    linktarget="$3";
    if [ -L "${symlink}" ]; then
        echo "Link ${symlink} exists already."
    else
        if [ -d ${symlink} ]; then
            echo "Directory ${symlink}/ exists."
        else
            if [ -f ${symlink} ]; then
                echo "File ${symlink} exists."
            else
                ln -s ${linksource} ${linktarget} 
                echo "Link ${linksource} -> ${linktarget} created."
            fi
        fi
    fi
}

_installSymLink ~/.config/qtile ~/dotfiles/qtile/ ~/.config
_installSymLink ~/.config/alacritty ~/dotfiles/alacritty/ ~/.config
_installSymLink ~/.config/picom ~/dotfiles/picom/ ~/.config
_installSymLink ~/.config/ranger ~/dotfiles/ranger/ ~/.config
_installSymLink ~/.config/rofi ~/dotfiles/rofi/ ~/.config
_installSymLink ~/.config/nvim ~/dotfiles/nvim/ ~/.config
_installSymLink ~/.config/polybar ~/dotfiles/polybar/ ~/.config
_installSymLink ~/.config/dunst ~/dotfiles/dunst/ ~/.config
_installSymLink ~/.config/dunst ~/dotfiles/fish/ ~/.config
_installSymLink ~/.config/starship.toml ~/dotfiles/starship/starship.toml ~/.config/starship.toml

# ------------------------------------------------------
# Install .bashrc
# ------------------------------------------------------
echo ""
echo "-> Install .bashrc"
while true; do
    read -p "Do you want to replace the existing .bashrc file? (Yy/Nn): " yn
    case $yn in
        [Yy]* )
            rm ~/.bashrc
            echo ".bashrc removed"
        break;;
        [Nn]* ) 
            echo "Replacement of .bashrc skipped."
        break;;
        * ) echo "Please answer yes or no.";;
    esac
done
_installSymLink ~/.bashrc ~/dotfiles/.bashrc ~/.bashrc

# ------------------------------------------------------
# Install Theme, Icons and Cursor
# ------------------------------------------------------
echo ""
echo "-> Install Theme"
while true; do
    read -p "Do you want to replace the existing theme configuration? (Yy/Nn): " yn
    case $yn in
        [Yy]* )
            if [ -d ~/.config/gtk-3.0 ]; then
                rm -r ~/.config/gtk-3.0
                echo "gtk-3.0 removed"
            fi

            if [ -f ~/.gtkrc-2.0 ]; then
                rm ~/.gtkrc-2.0
                echo ".gtkrc-2.0"
            fi

            if [ -f ~/.Xresources ]; then
                rm ~/.Xresources
                echo ".Xresources removed"
            fi
            
            if [ -d ~/.icons ]; then
                rm -r ~/.icons
                echo ".icons removed"
            fi
            
            _installSymLink ~/.gtkrc-2.0 ~/dotfiles/.gtkrc-2.0 ~/.gtkrc-2.0
            _installSymLink ~/.config/gtk-3.0 ~/dotfiles/gtk-3.0/ ~/.config/
            _installSymLink ~/.Xresources ~/dotfiles/.Xresources ~/.Xresources
            _installSymLink ~/.icons ~/dotfiles/.icons/ ~/

            echo "Existing theme removed"
        break;;
        [Nn]* ) 
            echo "Replacement of theme skipped."
        break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# ------------------------------------------------------
# Install wallpapers
# ------------------------------------------------------
echo ""
echo "-> Install wallapers"
while true; do
    read -p "Do you want to clone the wallpapers? (Yy/Nn): " yn
    case $yn in
        [Yy]* )
            if [ -d ~/wallpaper/ ]; then
                echo "wallpaper folder already exists."
            else
                git clone https://gitlab.com/stephan-raabe/wallpaper.git ~/wallpaper
                echo "wallpaper installed."
            fi
            echo "Wallpaper installed."
        break;;
        [Nn]* ) 
            if [ -d ~/wallpaper/ ]; then
                echo "wallpaper folder already exists."
            else
                mkdir ~/wallpaper
            fi
            cp ~/dotfiles/default.jpg ~/wallpaper
            echo "Default wallpaper installed."
        break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# ------------------------------------------------------
# Init pywal
# ------------------------------------------------------
echo ""
echo "-> Init pywal"
wal -i ~/dotfiles/default.jpg
echo "pywal initiated."

# ------------------------------------------------------
# DONE
# ------------------------------------------------------
clear
echo "DONE!"
echo "don't forget to check qtile/autostart.sh and picom configs, as well as the neofetch entry in .bashrc"
