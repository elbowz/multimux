# multimux

Mux multiple video and audio files

## Introduction

This simple script mux audio track with correct video file. 
If you have many video files (tv series episodies) and realtive audio files, this scirpt try to match the correct track for each video. 

The match is made by regex.

*note: multimux use 'ffmpeg' for mux, but you can use what you want*

## Usage
```
multimux [-m VIDEOMASK] [-a AUDIOMASK] [-t AUDIOTARGET] [-d DEST] [-p POSTFIX] [-c EXECCMD] [-sv] <video-files>
multimux -i

   es: multimux /path/to/video
       multimux -t '/path/to/audio/*.mp3' /path/to/video/*.avi
       multimux -v '([0-9]+)x([0-9]+).*\.(?:avi)' -v 's([0-9]+)e([0-9]+).*\.(?:avi)' /path/to/video

Mux video with relative audio file. Match correct file with regex sub-match.
es. foo.01x03.avi => sub-match: '01' and '03' => match with: pippo.s01e03.mp3

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -m VIDEOMASK, --video-mask=VIDEOMASK
                        regex to match video files. Submatch for match with
                        audio (e.s episodie number, season). Repeatable
                        option.
  -a AUDIOMASK, --audio-mask=AUDIOMASK
                        regex to match audio files. Submatch for match with
                        video (e.s episodie number, season). Repeatable
                        option.
  -t AUDIOTARGET, --audio-target=AUDIOTARGET
                        directory where are audio to mux
  -d DEST, --dest=DEST  directory dest, where are saved muxed files. Default:
                        same path of video-files
  -p POSTFIX, --dest-postfix=POSTFIX
                        Muxed files postfix (es. video.avi =>
                        videopostfix.avi). Default: .muxed
  -c EXECCMD, --exec-cmd=EXECCMD
                        program executed with matched viedo and audio
                        (placeholder: %(video)s, %(audio)s %(dest)s)
  -s, --trial           perform a trial run with no changes made
  -v, --verbose         Enable (and increase) verbosity. Repeatable option.
  -i, --info            view default regex mask and exec-cmd
```
## Example

if you have a directory content like this:

*ls*

> Doctor.Who.2005.2x00.Bonus.Christmas.Invasion.althus.DVD.avi
> Doctor.Who.2005.2x01.New.Earth.m00tv.DVD.avi
> Doctor.Who.2005.2x02.Tooth.And.Claw.SAiNTS.DVD.avi
> Doctor.Who.2005.2x03.School.Reunion.SAiNTS.DVD.avi
> Doctor.Who.2005.2x04.The.Girl.In.The.Fireplace.SAiNTS.DVD.avi
> Doctor.Who.2005.2x05.Rise.Of.The.Cyberman.(Part.1).FoV.DVD.avi
> Doctor.Who.2005.2x06.The.Age.Of.Steel.(Part.2).FoV.DVD.avi
> Doctor.Who.2005.2x07.The.Idiots.Lantern.FoV.DVD.avi
> Doctor.Who.2005.2x08.The.Impossible.Planet.(Part.1).m00tv.DVD.avi
> Doctor.Who.2005.2x09.The.Satan.Pit.(Part.2).m00tv.DVD.avi
> Doctor.Who.2005.2x10.Love.And.Monsters.m00tv.DVD.avi
> Doctor.Who.2005.2x11.Fear.Her.m00tv.DVD.[tvu.org.ru].avi
> Doctor.Who.2005.2x12.Army.Of.Ghosts.(Part.1).m00tv.DVD.avi
> Doctor.Who.2005.2x13.Doomsday.(Part.2).m00tv.DVD.avi
> Doctor.Who.2x00.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x01.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x02.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x03.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x04.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x05.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x06.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x07.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x08.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x09.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x10.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x11.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x12.Audio.ITA.per.DVDRip.by.trexios.mp3
> Doctor.Who.2x13.Audio.ITA.per.DVDRip.by.trexios.mp3

you can execute: *multimux -v .*

> Matched video (Doctor.Who.2005.2x02.Tooth.And.Claw.SAiNTS.DVD.avi) and audio (Doctor.Who.2x02.Audio.ITA.per.DVDRip.by.trexios.mp3)!
> executed: ffmpeg -i "Doctor.Who.2005.2x02.Tooth.And.Claw.SAiNTS.DVD.avi" -i "Doctor.Who.2x02.Audio.ITA.per.DVDRip.by.trexios.mp3" -acodec copy -vcodec copy "Doctor.Who.2005.2x02.Tooth.And.Claw.SAiNTS.DVD.muxed.avi" ...with exit code: 0
> Matched video (Doctor.Who.2005.2x08.The.Impossible.Planet.(Part.1).m00tv.DVD.avi) and audio (Doctor.Who.2x08.Audio.ITA.per.DVDRip.by.trexios.mp3)!
> executed: ffmpeg -i "Doctor.Who.2005.2x08.The.Impossible.Planet.(Part.1).m00tv.DVD.avi" -i "Doctor.Who.2x08.Audio.ITA.per.DVDRip.by.trexios.mp3" -acodec copy -vcodec copy "Doctor.Who.2005.2x08.The.Impossible.Planet.(Part.1).m00tv.DVD.muxed.avi" ...with exit code: 0
> Matched video (Doctor.Who.2005.2x05.Rise.Of.The.Cyberman.(Part.1).FoV.DVD.avi) and audio (Doctor.Who.2x05.Audio.ITA.per.DVDRip.by.trexios.mp3)!
> executed: ffmpeg -i "Doctor.Who.2005.2x05.Rise.Of.The.Cyberman.(Part.1).FoV.DVD.avi" -i "Doctor.Who.2x05.Audio.ITA.per.DVDRip.by.trexios.mp3" -acodec copy -vcodec copy "Doctor.Who.2005.2x05.Rise.Of.The.Cyberman.(Part.1).FoV.DVD.muxed.avi" ...with exit code: 0
> Matched video (Doctor.Who.2005.2x13.Doomsday.(Part.2).m00tv.DVD.avi) and audio (Doctor.Who.2x13.Audio.ITA.per.DVDRip.by.trexios.mp3)!
> executed: ffmpeg -i "Doctor.Who.2005.2x13.Doomsday.(Part.2).m00tv.DVD.avi" -i "Doctor.Who.2x13.Audio.ITA.per.DVDRip.by.trexios.mp3" -acodec copy -vcodec copy "Doctor.Who.2005.2x13.Doomsday.(Part.2).m00tv.DVD.muxed.avi" ...with exit code: 0
> Matched video (Doctor.Who.2005.2x06.The.Age.Of.Steel.(Part.2).FoV.DVD.avi) and audio (Doctor.Who.2x06.Audio.ITA.per.DVDRip.by.trexios.mp3)!
> executed: ffmpeg -i "Doctor.Who.2005.2x06.The.Age.Of.Steel.(Part.2).FoV.DVD.avi" -i "Doctor.Who.2x06.Audio.ITA.per.DVDRip.by.trexios.mp3" -acodec copy -vcodec copy "Doctor.Who.2005.2x06.The.Age.Of.Steel.(Part.2).FoV.DVD.muxed.avi" ...with exit code: 0
> Matched video (Doctor.Who.2005.2x03.School.Reunion.SAiNTS.DVD.avi) and audio (Doctor.Who.2x03.Audio.ITA.per.DVDRip.by.trexios.mp3)!
> executed: ffmpeg -i "Doctor.Who.2005.2x03.School.Reunion.SAiNTS.DVD.avi" -i "Doctor.Who.2x03.Audio.ITA.per.DVDRip.by.trexios.mp3" -acodec copy -vcodec copy "Doctor.Who.2005.2x03.School.Reunion.SAiNTS.DVD.muxed.avi" ...with exit code: 0
> 
> [...]
> 
> Matched video (Doctor.Who.2005.2x01.New.Earth.m00tv.DVD.avi) and audio (Doctor.Who.2x01.Audio.ITA.per.DVDRip.by.trexios.mp3)!
> executed: ffmpeg -i "Doctor.Who.2005.2x01.New.Earth.m00tv.DVD.avi" -i "Doctor.Who.2x01.Audio.ITA.per.DVDRip.by.trexios.mp3" -acodec copy -vcodec copy "Doctor.Who.2005.2x01.New.Earth.m00tv.DVD.muxed.avi" ...with exit code: 0                                                                          
> tot. matched: 14 succes execcmd: 14/14      

if you have other files in same directory, and you would ignore this one with different extension: *multimux -v -t '`*`.mp3' '`*`.avi'*