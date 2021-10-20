from typing import List  # noqa: F401
import os
import subprocess
from libqtile import bar,layout,widget
from libqtile.config import Click,Drag,Group,Key,Match,Screen,ScratchPad,DropDown,Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from custom.windowname import WindowName as CustomWindowName

mod  = "mod4"
mod1 = "alt"

keys = [
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),# Switch between windows
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key(["mod1"], "Tab", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.# Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
 
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
        
    # volume control 
    Key([], "XF86AudioRaiseVolume",lazy.spawn("/usr/local/bin/volume-up"), desc="Increase volume",),
    Key([], "XF86AudioLowerVolume",lazy.spawn("/usr/local/bin/volume-down"), desc="Decrease volume",),
    Key([], "XF86AudioMute",lazy.spawn("amixer set Master toggle"), desc="Toggle mute",), 
    # brightness control
    Key([], "XF86MonBrightnessUp", lazy.spawn("/usr/local/bin/backlight-up"), desc="Increase screen brightness",), 
    Key([], "XF86MonBrightnessDown", lazy.spawn("/usr/local/bin/backlight-down"),desc="decrease screen brightness",),
    
    Key([mod] ,"Return", lazy.spawn("alacritty")),
    Key([mod] ,"t", lazy.spawn("st")),

    Key([mod] ,"e",lazy.spawn("brave")),
    Key([mod] ,"f",lazy.spawn("thunar")),
    Key([mod] ,"b",lazy.spawn("qutebrowser")),
    
    Key([mod] ,"n",lazy.spawn("st -e nmtui")),
    Key([mod] ,"m",lazy.spawn("st -e ncmpcpp")),
    
    Key(["mod1"] ,"m",lazy.spawn("st-e ncmpcpp")),
    Key(["mod1"] ,"f",lazy.spawn("pcmanfm")),
    Key(["mod1"] ,"t",lazy.spawn("st")),
    Key(["mod1"] ,"space",lazy.spawn("rofi -show run")),
    Key(["mod1"] ,"Return", lazy.spawn("alacritty")),
    
]

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6",]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
group_labels = ["", "", "", "","", ""]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        #Key(["mod1"], "Tab", lazy.screen.next_group()),
        #Key(["mod", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

# Define colors

colors = [
    ["#2e3440", "#2e3440"],  # background
    ["#d8dee9", "#d8dee9"],  # foreground
    ["#3b4252", "#3b4252"],  # background lighter
    ["#bf616a", "#bf616a"],  # red
    ["#a3be8c", "#a3be8c"],  # green
    ["#ebcb8b", "#ebcb8b"],  # yellow
    ["#81a1c1", "#81a1c1"],  # blue
    ["#b48ead", "#b48ead"],  # magenta
    ["#88c0d0", "#88c0d0"],  # cyan
    ["#e5e9f0", "#e5e9f0"],  # white
    ["#4c566a", "#4c566a"],  # grey
    ["#d08770", "#d08770"],  # orange
    ["#8fbcbb", "#8fbcbb"],  # super cyan
    ["#5e81ac", "#5e81ac"],  # super blue
    ["#242831", "#242831"],  # super dark background
]

layout_theme = {
    "border_width": 5,
    "margin": 9,
    "border_focus": "#d8dee9",
    "border_normal": "3b4252",
    "font": "FiraCode Nerd Font",
    "grow_amount": 2,
}

layouts = [
    layout.Columns(border_focus_stack='#d75f5f'),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
     layout.Bsp(),
    # layout.Matrix(),
     layout.MonadTall(),
     layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(font='FiraCode Nerd Font',fontsize=12,padding=3,background=colors[0])

extension_defaults = widget_defaults.copy()

def open_powermenu():
    qtile.cmd_spawn("sh /home/sri/.config/rofi/bin/powermenu")
    
def open_network():
    qtile.cmd_spawn("sh /home/sri/.config/rofi/bin/network")
    
def open_pavu():
    qtile.cmd_spawn("pavucontrol")
    
def open_launcher():
    qtile.cmd_spawn("sh /home/sri/.config/rofi/bin/launcher")

def kill_window():
    qtile.cmd_spawn("xdotool getwindowfocus windowkill")
def open_htop():
    qtile.cmd_spawn("st")

screens = [
    Screen(
        wallpaper="~/.config/qtile/dnord4k_dark.png",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
              widget.TextBox(
                    text="",
                    foreground=colors[13],
                    background=colors[0],
                    font="Font Awesome 5 Free Solid",
                    fontsize=18,
                    padding=2,
                    mouse_callbacks={"Button1": open_launcher},
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=2,
                    size_percent=50,
                ),
               widget.Image(filename='~/.config/qtile/icons/fillC1.png'),
               widget.GroupBox(font="Font Awesome 5 Free Solid",
					fontsize=12,
					padding = 5,
					borderwidth = 4,
					active =  colors[9],
					inactive =  colors[10],
					disable_drag =  True,
					rounded =  True,
					highlight_color =  colors[2],
					block_highlight_text_color =  colors[6],
					#highlight_method =  block,
					this_current_screen_border =  colors[14],
					this_screen_border =  colors[7],
					other_current_screen_border =  colors[14],
					other_screen_border =  colors[14],
					foreground =  colors[1],
					background =  colors[14],
					urgent_border =  colors[3],
					),
               widget.Image(filename='~/.config/qtile/icons/fillC2.png'),
               widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=2,
                    size_percent=50,
                ),
                widget.TextBox(
                    text=" ",
                    foreground=colors[12],
                    background=colors[0],
                    # fontsize=38,
                    font="Font Awesome 5 Free Solid",
                ),
                CustomWindowName(	
                    background=colors[0],
                    foreground=colors[12],
                    width=bar.CALCULATED,
                    empty_group_string="Desktop",
                    max_chars=165,
                    mouse_callbacks={"Button2": kill_window},
                ),
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=10,
                    size_percent=50,
                ),
               
                widget.Prompt(
                    foreground=colors[7],
                    background=colors[14],               
                ),
                
                widget.Spacer(),
                widget.Image(filename='~/.config/qtile/icons/fillC1.png'),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                    foreground=colors[2],
                    background=colors[14],
                    padding=-2,
                    scale=0.45,
                ),
               widget.Image(filename='~/.config/qtile/icons/fillC2.png'),
				
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=2,
                    size_percent=50,
                ),

                widget.Image(filename='~/.config/qtile/icons/fillC1.png'),
                widget.Memory(
                    background=colors[14],
                    foreground=colors[12],
                    format='{MemUsed: .0f}{mm}',
                    measure_mem='M',
                    mouse_callbacks={"Button1": open_htop},
                ),
				widget.Image(filename='~/.config/qtile/icons/fillC2.png'),


				widget.Image(filename='~/.config/qtile/icons/fillC1.png'),
                widget.TextBox(
                    text=" ",
                    foreground=colors[8],
                    background=colors[14],
                    font="Font Awesome 5 Free Solid",
                    padding_y=50
                    # fontsize=38,
                ),
                
               #widget.PulseVolume(
                widget.Volume(
                    foreground=colors[8],
                    background=colors[14],
                    limit_max_volume="True",
                    mouse_callbacks={"Button3": open_pavu},
                ),
				widget.Image(filename='~/.config/qtile/icons/fillC2.png'),
				
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=2,
                    size_percent=50,
                ),
				widget.Image(filename='~/.config/qtile/icons/fillC1.png'),
                 widget.TextBox(
                    text=" ",
                    font="Font Awesome 5 Free Solid",
                    foreground=colors[7],  # fontsize=38
                    background=colors[14],
                ),
                widget.Net(
                    interface="wlp7s0",
                    format='↓↑',
                    foreground=colors[7],
                    background=colors[14],
                    padding=5,
                    mouse_callbacks={"Button1": open_network},
                ),
				widget.Image(filename='~/.config/qtile/icons/fillC2.png'),
				
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=2,
                    size_percent=5,
                ),
				widget.Image(filename='~/.config/qtile/icons/fillC1.png'),
                widget.TextBox(
                    text=" ",
                    font="Font Awesome 5 Free Solid",
                    foreground=colors[5],  # fontsize=38
                    background=colors[14],
                ),
                widget.Clock(
                    format="%a, %b %d",
                    background=colors[14],
                    foreground=colors[5],
                ),
				widget.Image(filename='~/.config/qtile/icons/fillC2.png'),
				
                widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=2,
                    size_percent=25,
                ),
                widget.Image(filename='~/.config/qtile/icons/fillC1.png'),
                widget.TextBox(
                    text=" ",
                    font="Font Awesome 5 Free Solid",
                    foreground=colors[4],  # fontsize=38
                    background=colors[14],
							 ),
                widget.Clock(
                    format="%I:%M %p",
                    foreground=colors[4],
                    background=colors[14],
                    # mouse_callbacks={"Button1": todays_date},
							),
				widget.Image(filename='~/.config/qtile/icons/fillC2.png'),
				widget.Sep(
                    linewidth=0,
                    foreground=colors[2],
                    padding=2,
                    size_percent=25,
                ),			
                widget.TextBox(
                    text="⏻",
                    foreground=colors[13],
                    font="Font Awesome 5 Free Solid",
                    fontsize=18,
                    padding=5,
                    mouse_callbacks={"Button1": open_powermenu},
							),
            ],
            30,
        ),
        #bottom=bar.Gap(10),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
