import os
import re
import tempfile

CMD_NEXTSONG = 'GNIP_NEXTSONG'
CMD_PREVSONG = 'GNIP_PREVSONG'
CMD_SHOW_PATCHES = 'GNIP_SHOW_PATCHES'


def register(trg):
    trg._parent.log_message('Registering UserAction command:%s from:%s' % (CMD_NEXTSONG, __file__))
    # Add method from this file to the ClyphXUserActions class
    type(trg).gnip_next_song = next_song
    # Register method with ClyphX command
    trg._action_dict[CMD_NEXTSONG] = 'gnip_next_song'

    trg._parent.log_message('Registering UserAction command:%s from:%s' % (CMD_PREVSONG, __file__))
    # Add method from this file to the ClyphXUserActions class
    type(trg).gnip_prev_song = prev_song
    # Register method with ClyphX command
    trg._action_dict[CMD_PREVSONG] = 'gnip_prev_song'

    trg._parent.log_message('Registering UserAction command:%s from:%s' % (CMD_SHOW_PATCHES, __file__))
    # Add method from this file to the ClyphXUserActions class
    type(trg).gnip_show_patches = show_patches
    # Register method with ClyphX command
    trg._action_dict[CMD_SHOW_PATCHES] = 'gnip_show_patches'


def next_song(self, track, args):
    tracks = self.song().tracks
    final_track_idx = len(tracks) - 1

    sel_trk = self.song().view.selected_track
    found_idx = list(tracks).index(sel_trk)
    if found_idx < final_track_idx:
        next_track = tracks[found_idx + 1]
        self.song().view.selected_track = next_track

    self.song().view.selected_scene = self.song().scenes[0]

    self.song().view.selected_track.clip_slots[0].fire()


def prev_song(self, track, args):
    tracks = self.song().tracks

    sel_trk = self.song().view.selected_track
    found_idx = list(tracks).index(sel_trk)
    if found_idx > 0:
        prev_track = tracks[found_idx - 1]
        self.song().view.selected_track = prev_track

    self.song().view.selected_scene = self.song().scenes[0]

    self.song().view.selected_track.clip_slots[0].fire()


def show_patches(self, track, args):
    # create table of clip names
    clip_name_table = []
    for track in self.song().tracks:
        clips = []
        clip_name_table.append(clips)
        for slot in track.clip_slots:
            clip_name = '???' if slot.clip is None else slot.clip.name
            clips.append(clip_name)

    # write output to temp file
    with tempfile.NamedTemporaryFile(prefix='Ableton_clipqueue_TrackDump_', suffix='.html', delete=False) as f:
        f.write('<ul>\n')
        for track in self.song().tracks:
            f.write('<li>%s</li>\n' % track.name)
            f.write('    <ul>\n')
            for slot in track.clip_slots:
                if slot.clip is not None:
                    clip_names = _get_clip_names_from_clyphx_snippet(clip_name_table, slot.clip.name)
                    label = ', '.join(clip_names)
                    f.write('    <li>%s</li>\n' % label)
            f.write('    </ul>\n')
        f.write('</ul>\n')
    self._parent.log_message('Opening track dump file: %s' % f.name)
    os.system(r'start %s' % f.name)


#################### Supporting code
def _get_clip_names_from_clyphx_snippet(clip_name_table, script):
    """given a ClyphX script string containing "#/PLAY #" type commands, return a list of clip names looked up from the track/scene references"""
    if not script.strip().startswith('['):
        return []
    cmds = script.split(';')
    clip_names = []
    for cmd in cmds:
        cmd = cmd.strip()
        regex = r'(\d+)\s*/\s*PLAY\s*(\d+)'
        match = re.search(regex, cmd)
        if match:
            trk_idx, scene_idx = match.groups()
            trk_idx = int(trk_idx) - 1
            scene_idx = int(scene_idx) - 1
            try:
                clip_names.append(clip_name_table[trk_idx][scene_idx])
            except IndexError:
                pass
    return clip_names
