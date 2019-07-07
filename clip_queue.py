CMD_NEXTSONG = 'GNIP_NEXTSONG'
CMD_PREVSONG = 'GNIP_PREVSONG'


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
