# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder

colors = {
    "bg":        "#1a1b26",
    "bg_dark":   "#16161e",
    "bg_alt":    "#24283b",
    "fg":        "#c0caf5",
    "fg_dim":    "#565f89",
    "blue":      "#7aa2f7",
    "cyan":      "#7dcfff",
    "green":     "#9ece6a",
    "magenta":   "#bb9af7",
    "red":       "#f7768e",
    "yellow":    "#e0af68",
    "border":    "#7aa2f7",
}

mod = "mod4" #aka Windows key
terminal = "alacritty" #This is an example on how flexible Qtile is, you create variables then use them in a keybind for example (see below)
mod1 = "mod1" #alt key
filemanager = "thunar"
browser_main = "vivaldi-stable"
browser_alt = "firefox"
perplexity_app = "perplexity"
winboat_app = "winboat"
audio_mixer = "pavucontrol"


# Sticky windows

sticky_windows = []

@lazy.function
def toggle_sticky_windows(qtile, window=None):
    if window is None:
        window = qtile.current_screen.group.current_window
    if window in sticky_windows:
        sticky_windows.remove(window)
    else:
        sticky_windows.append(window)
    return window

@hook.subscribe.setgroup
def move_sticky_windows():
    for window in sticky_windows:
        window.togroup()
    return

@hook.subscribe.client_killed
def remove_sticky_windows(window):
    if window in sticky_windows:
        sticky_windows.remove(window)

# Below is an example how to make Firefox Picture-in-Picture windows automatically sticky.
@hook.subscribe.client_managed
def auto_sticky_windows(window):
    info = window.info()
    if (info['wm_class'] == ['Toolkit', 'firefox']
            and info['name'] == 'Picture-in-Picture'):
        sticky_windows.append(window)

# █▄▀ █▀▀ █▄█ █▄▄ █ █▄░█ █▀▄ █▀
# █░█ ██▄ ░█░ █▄█ █ █░▀█ █▄▀ ▄█

keys = [
    # Launch apps
    Key([mod], "b", lazy.spawn(browser_main), desc="Launch Vivaldi"),
    Key([mod], "p", lazy.spawn(perplexity_app), desc="Launch Perplexity"),
    Key([mod], "w", lazy.spawn(browser_alt), desc="Launch Firefox"),
    Key([mod], "i", lazy.spawn(winboat_app), desc="Launch WinBoat"),
    Key([mod], "a", lazy.spawn(audio_mixer), desc="Launch pavucontrol"),

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle focused window to fullscreen"),
    Key([mod], "v", lazy.window.toggle_floating(), desc="Toggle focused window to floating"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod1], "Space", lazy.spawn("rofi -theme rounded-green-dark -show drun"), desc="Spawn a command using a prompt widget"),


##CUSTOM
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +1%"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -1%"), desc='volume down'),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc='Volume Mute'),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 5%+"), desc='brightness UP'),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-"), desc='brightness Down'),
    
##Misc keybinds
    Key([mod, "control"], "p", lazy.spawn("flameshot gui"), desc='Screenshot'),
    Key(["control"], "Print", lazy.spawn("flameshot full -c -p ~/Pictures/"), desc='Screenshot'),
    Key([mod], "e", lazy.spawn(filemanager), desc="Open file manager"),
    Key([mod], "s",toggle_sticky_windows(), desc="Toggle state of sticky for current window"),
]   

# █▀▀ █▀█ █▀█ █░█ █▀█ █▀
# █▄█ █▀▄ █▄█ █▄█ █▀▀ ▄█


groups = [Group(f"{i+1}", label="⬤") for i in range(9)] #Be careful modifying this, otherwise qtile config will break

for i in groups:
    keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name),
                    ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc="Switch to & move focused window to group {}".format(i.name),
                    ),
                ]
            )


###𝙇𝙖𝙮𝙤𝙪𝙩###

layouts = [
    layout.Columns(
        margin=0,
        border_focus=colors["border"],
        border_normal=colors["bg_dark"],
        border_width=3,
    ),
    layout.Max(
        border_focus=colors["border"],
        border_normal=colors["bg_dark"],
        margin=0,
        border_width=0,
    ),
    layout.Floating(
        border_focus=colors["border"],
        border_normal=colors["bg_dark"],
        border_width=3,
        margin=0,
    ),
    layout.Matrix(
        border_focus=colors["border"],
        border_normal=colors["bg_dark"],
        border_width=3,
        margin=0,
    ),
    layout.MonadWide(
        border_focus=colors["border"],
        border_normal=colors["bg_dark"],
        border_width=3,
        margin=0,
    ),
    layout.Tile(
        border_focus=colors["border"],
        border_normal=colors["bg_dark"],
        border_width=3,
        margin=0,
    ),
]


widget_defaults = dict(
    font = "sans",
    fontsize = 12,
    padding = 4,
)

extension_defaults = widget_defaults.copy()


def open_launcher():
    qtile.cmd_spawn("rofi -theme rounded-green-dark -show drun")

def open_btop():
    qtile.cmd_spawn("alacritty --hold -e btop")

            
# █▄▄ ▄▀█ █▀█
# █▄█ █▀█ █▀▄
 
screens = [
    Screen(
        top = bar.Bar(
            [   
                widget.Spacer(
                    length = 18,
                    background = colors["bg_dark"],
                ),
                
                widget.Image(
                    filename = '~/.config/qtile/Assets/launch_Icon.png',
                    background = colors["bg_dark"],
                    mouse_callbacks = {'Button1': open_launcher},
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/6.png',
                ),

                widget.GroupBox(
                    fontsize=16,
                    borderwidth=0,
                    highlight_method='block',
                    active=colors["fg"],
                    block_highlight_text_color=colors["blue"],
                    highlight_color=colors["bg_alt"],
                    inactive=colors["fg_dim"],
                    foreground=colors["fg"],
                    background=colors["bg_alt"],
                    this_current_screen_border=colors["blue"],
                    this_screen_border=colors["bg_alt"],
                    other_current_screen_border=colors["bg_alt"],
                    other_screen_border=colors["bg_alt"],
                    urgent_border=colors["red"],
                    rounded=True,
                    disable_drag=True,
                 ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',
                ),
                
                widget.CurrentLayout(
                    background=colors["bg_alt"],
                    font='IBM Plex Mono Medium',
                    fontsize=15,
                    padding=0,
                    foreground=colors["fg"],
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',                
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',
                ),

                widget.WindowName(
                    background=colors["bg_alt"],
                    format="{name}",
                    font='IBM Plex Mono Medium',
                    fontsize=14,
                    empty_group_string='Desktop',
                    padding=0,
                    foreground=colors["fg"],
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',                
                ),  

                widget.Image(
                    filename = '~/.config/qtile/Assets/1.png',                
                    background=colors["bg_alt"],
                ),

                widget.CPU(
                    font="IBM Plex Mono Medium",
                    format='CPU:({load_percent:.1f}%/{freq_current}GHz)',
                    fontsize=15,
                    margin=0,
                    padding=0,
                    background=colors["bg_alt"],
                    foreground=colors["fg"],
                    mouse_callbacks={'Button1': open_btop},
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',                
                    background=colors["bg_alt"],
                ),  
  
                widget.Systray(
                    background=colors["bg_alt"],
                    icon_size=24,
                    padding=3,
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',                
                    background=colors["bg_alt"],
                ),                    
                                                
                widget.Spacer(
                    length = 0,
                    background=colors["bg_alt"],
                ),  
               
                widget.Memory(
                    format='RAM:({MemUsed:.0f}MB/{MemTotal:.0f}MB)',
                    font="IBM Plex Mono Medium",
                    fontsize=15,
                    padding=0,
                    background=colors["bg_alt"],
                    foreground=colors["fg"],
                    mouse_callbacks={'Button1': open_btop},
                ),

                widget.Spacer(
                    length = 6,
                    background=colors["bg_alt"],
                ),  

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/volume.svg',
                    background=colors["bg_alt"],
                    margin_y = 3,
                    scale = True,
                    mouse_callbacks = {'Button1': open_btop},
                ),

                widget.Spacer(
                    length = 4,
                    background=colors["bg_alt"],
                ), 
                
                widget.PulseVolume(
                    font= 'IBM Plex Mono Medium',
                    fontsize = 15,
                    padding = 0,
                    background=colors["bg_alt"],
                    foreground=colors["fg"],
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),                


                widget.Image(
                    filename = '~/.config/qtile/Assets/1.png',                
                    background=colors["bg_alt"],
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/calendar.svg',
                    background=colors["bg_alt"],
                    margin_y = 3,
                    scale = True,
                ),

                widget.Spacer(
                    length = 6,
                    background=colors["bg_alt"],
                ), 
        
                widget.Clock(
                    format='%d/%m/%y ',
                    background=colors["bg_alt"],
                    font="IBM Plex Mono Medium",
                    fontsize=15,
                    padding=0,
                    foreground=colors["fg"],
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/clock.svg',
                    background=colors["bg_alt"],
                    margin_y = 3,
                    margin_x = 5,
                    scale = True,
                ),

                widget.Clock(
                    format='%H:%M',
                    background=colors["bg_alt"],
                    font="IBM Plex Mono Medium",
                    fontsize=15,
                    padding=0,
                    foreground=colors["fg"],
                ),

                widget.Spacer(
                    length = 18,
                    background=colors["bg_alt"],
                ),
            ],
            30,  # Bar size (all axis)
            margin = [0,8,6,8], # Bar margin (Top,Right,Bottom,Left)
            background=colors["bg"],
        ),
        wallpaper='~/.config/qtile/Wallpaper/Skyscraper.png',
        wallpaper_mode="fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False #This basically puts your mouse in the center on the screen after you switch to another workspace
floating_layout = layout.Floating(
    border_focus=colors["border"],
    border_normal=colors["bg_dark"],
	border_width=3,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

from libqtile import hook
# some other imports
import os
import subprocess
# stuff
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh') # path to my script, under my user directory
    subprocess.call([home])

auto_fullscreen = True
focus_on_window_activation = "smart" #or focus
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
