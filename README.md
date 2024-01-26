Using wallpaper engine's playInWindow feature + wine to properly run wallpaper engine under plasma5 (and other DE's provided you can use xwinwrap)

in order to use it on plasma, go to system settings -> workspace -> window management -> window rules and then import wallpaper_rules.kwinrules, edit the position as fit

then set your steam library position in wallpapers.py and change the configs in wallpaper_mapping
then run the script

if you want to make it react to music click on the wallpaper engine icon in the system tray and press configure, then go to general then go to audio, I had to change the default recording device and set the recording volume up to 2000

mpris_server.py and winrt_client.py are pretty much useless right now due to a longstanding "bug" where wine doesn't have proper support for media controls

the applyProperties command is busted rn because of yet another wine bug, i assume it's to do with SetCurrentProcessExplicitAppUserModelID not being implemented and wallpaper engine using its own groups for the "location" parameter but again i don't care enough to patch wine to fix it