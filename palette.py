#!/usr/bin/env python3

import mido

def abs_to_rel(track):
    curr_time = 0
    rel_track = mido.MidiTrack()
    sorted = track.copy()
    sorted.sort(key=lambda x: x.time)

    for note in sorted:
        note.time = note.time - curr_time
        rel_track.append(note)
        curr_time += note.time

    return rel_track

def rel_to_abs(track):
    curr_time = 0
    abs_track = mido.MidiTrack()

    for note in track.copy():
        curr_time += note.time
        note.time = curr_time
        abs_track.append(note)

    return abs_track

def palette(start_note, start_vel, n):
    track = mido.MidiTrack()
    for i in range(n):
        on = mido.Message('note_on', note=start_note+i, velocity=start_vel+i, time=0)
        track.append(on)

        off = mido.Message('note_off', note=start_note+i, time=1200000)
        track.append(off)

    return track

if __name__ == '__main__':
    with mido.MidiFile() as f:
        f.type = 0
        track = abs_to_rel(palette(36, 1, 64))
        f.tracks.append(track)
        f.save('lights/pro-mk2-page1.mid')

        f.tracks[0] = abs_to_rel(palette(36, 65, 63))
        f.save('lights/pro-mk2-page2.mid')
