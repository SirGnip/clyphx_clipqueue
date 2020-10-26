# Clip Triggering Queue ClyphX script for Ableton Live

### Summary
(Note: This is currently just a personal project.  It is far from a polished
product.  No promises are made about its ability to use used in multiple
situations.  But, give it a try!  I'd love to hear feedback!)

This script for Ableton provides a way to author a sequence of ClyphX scripts in
Ableton Live and interactively trigger them in sequence with
a controller mapped to the "next" and "previous" actions.

### Motivation
This script can be used for a lot of different things, but it was originally
written to provide [MainStage's](https://www.apple.com/mainstage/) style "next/previous"
patch selection for Sunday Keys for Ableton Live.  This allows you to bring a bit of
MainStage's "Concert, Set, and Patch" hierarchy for organizing instrument changes
to Ableton Live.  It makes it easy to roll through patch changes in order with one tap
on a MIDI controller.  I was originally using MainStage, but now am using 
Sunday Keys for Ableton Live and this script enables a MainStage-like way of 
selecting patch changes in Sunday Keys.


# Requirements
- [Ableton Live 10](https://www.ableton.com/en/live/)
- [Sunday Keys for Ableton Live](https://sundaysounds.com/patches/sunday-keys-for-ableton)
- [ClyphX](http://forum.nativekontrol.com/thread/992/current-version-clyphx-live-9) (have only tested with the "free" version, not the "Pro" version)


# Installation
(This is admittedly a complex set of instructions. I'm working on simplifying this.)

### Setup scripts in Ableton:
- Have ClyphX installed and working in Ableton Live
- Have Sunday Keys installed and working in Ableton Live
- Do a `git checkout` of this repo in the folder where you installed the ClyphX scripts (usually something like C:\ProgramData\Ableton\Live 10 Intro\Resources\MIDI Remote Scripts\ClyphX)
- Edit `MIDI Resource Scrits\ClyphX\ClyphXUserActions.py` and add the following lines to the bottom of the `__init__` method:


        import sundaykeys_relative_patch_select.rel_patch_sel
        sundaykeys_relative_patch_select.rel_patch_sel.register(self)
         
- Add the lines below to the `[USER CONTROLS]` section of `ClyphX\UserSettings.txt`.  Change the control
to be "note" or "cc", change the MIDI channel number and note number to suit your needs.


        # For sundaykeys_relative_patch_select custom User Actions
        # CONTROL_NAME = MSG_TYPE, MIDI_CHANNEL, NOTE_OR_CC_NUM, CLYPH_ACTION_LIST
        GNIP_CLIPQUEUE_PREVSONG = note, 10, 44, GNIP_PREVSONG
        GNIP_CLIPQUEUE_NEXTSONG = note, 10, 45, GNIP_NEXTSONG
        GNIP_CLIPQUEUE_PREVSCRIPT = note, 10, 46, UP; SCENE 8; PLAY
        GNIP_CLIPQUEUE_NEXTSCRIPT = note, 10, 47, DOWN; SCENE 8; PLAY


### Setup a Performance with Ableton:
- Launch Ableton and open your Sunday Keys Set
- Change to Ableton's Session View
- Move all of the "Off" Sunday Keys clips from Scene #3 to a scene beyond all of your clips (ex: Scene 8)
    - This is time consuming, so save a copy after you have done this once. 
- Create a new empty MIDI track in Ableton for each "song" of patch changes.
- For each patch change you want in your song...
    - Create an empty MIDI clip (double click the empty cell)
    - Rename the clip to include a ClyphX script that clears all currently active instruments and selects the patch you'd like to play:
        - ex: `[] SCENE 8; 2/PLAY 5`  (this first selects the "Off" clips new located on SCENE 8 to clear any active instruments and then starts playing the instrument at the 5th scene of the 2nd track)
    - Add these patch change ClyphX scripts to your new tracks like this.  Pressing the play button for these clips should activate the specific instrument.
        

            Track1:IntroSong                Track2:Interlude
            [] SCENE 8; 2/PLAY 5            [] SCENE 8; 2/PLAY 7
            [] SCENE 8; 4/PLAY 2            [] SCENE 8; 5/PLAY 3
            [] SCENE 8; 1/PLAY 1;3/PLAY 3   [] SCENE 8; 2/PLAY 7
                                            [] SCENE 8; 5/PLAY 3

### Use the patch and song changes
- Launch Ableton and open your Sunday Keys Set
- Change to Ableton's Session View
- Locate the track that represents your first "song".  Click the play button for the first "clip".  This
will activate the first instrument of the first song.
- Now, press the control on your MIDI controller that you have configured for the `GNIP_CLIPQUEUE_NEXTSCRIPT` controller in Clyph's `UserSettings.txt`. This should automatically clear your old instrument selection and select your the next instrument.
- Repeatedly press the controller mapped to `GNIP_CLIPQUEUE_NEXTSCRIPT` to advance through the patch changes.
- When at the end of the song, press the controller mapped to `GNIP_CLIPQUEUE_NEXTSONG`. The first patch of the next song will be activated.
- You can move forward and back through patches with the controllers mapped to `GNIP_CLIPQUEUE_NEXTSCRIPT` and `GNIP_CLIPQUEUE_PREVSCRIPT`.
- You can move forward and back through songs with the controllers mapped to `GNIP_CLIPQUEUE_NEXTSONG` and `GNIP_CLIPQUEUE_PREVSONG`
    

### Known Issues
- Very complex setup.  Specific to Sunday Keys.  Make more generic instructions.
- If the `GNIP_CLIPQUEUE_NEXTSCRIPT` action is triggered and the cursor moves onto an empty clip with no name, patch selection will fail until you do a next/prev song.

![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https%3A%2F%2Fgithub.com%2FSirGnip%2Fclyphx_clipqueue)
