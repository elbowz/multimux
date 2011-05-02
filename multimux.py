#!/usr/bin/python

# =======================================
# mux-series v0.1b - Copyright 2011
# Writted by muttley
# Get last version from muttley.eb2a.com
# =======================================

import os
import sys
import glob
import re
import shlex
import subprocess
from optparse import OptionParser

# GLOBAL VAR

# Script file name
g_script = os.path.basename(sys.argv[0])
# Script file absolute path
g_script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
# Verbosity
g_verbosity = 0

# Default ffmpeg command line
G_FFMPEG_CLI = 'ffmpeg -i "%(video)s" -i "%(audio)s" -acodec copy -vcodec copy "%(dest)s"'
# Default muxed file postfix (es. video.avi => videopostfix.avi)
G_DEST_POSTFIX = '.muxed'

# Default regexs tupla for video mask
G_VIDEO_MASK = ( r'(0?[0-9]{1,2})x(0?[0-9]{1,2}).*\.(?:avi|mpg)$', r'S(0?[0-9]{1,2}).?e(0?[0-9]{1,2}).*\.(?:avi|mpg)$' )
# Default regexs tupla for audio mask
G_AUDIO_MASK = ( r'(0?[0-9]{1,2})x(0?[0-9]{1,2}).*\.(?:mp3|wav)$', r'S(0?[0-9]{1,2}).?e(0?[0-9]{1,2}).*\.(?:mp3|wav)$' )

def main ():
	
	global g_verbosity
	
	# Help message
	usage = "usage: %prog [-m VIDEOMASK] [-a AUDIOMASK] [-t AUDIOTARGET] [-d DEST] [-p POSTFIX] [-c EXECCMD] [-sv] <video-files>\n"\
			"       %prog -i\n\n"\
			"   es: %prog /path/to/video\n"\
			"       %prog -t '/path/to/audio/*.mp3' /path/to/video/*.avi\n"\
			"       %prog -v '([0-9]+)x([0-9]+).*\.(?:avi)' -v 's([0-9]+)e([0-9]+).*\.(?:avi)' /path/to/video"
			
	description = "Mux video with relative audio file. Match correct file with regex sub-match.\n"\
				  "es. foo.01x03.avi => sub-match: '01' and '03' => match with: pippo.s01e03.mp3"
	version =" %prog 0.6b"	# --version to print
	epilog= " Copyright 2011"
	
	# Program parsed option
	
	parser = OptionParser(usage=usage, description=description, epilog=epilog, version=version)
	parser.add_option("-m", "--video-mask", action="append", type="string", dest="videoMask", default=G_VIDEO_MASK, 
					  help="regex to match video files. Submatch for match with audio (e.s episodie number, season). Repeatable option.")
					  
	parser.add_option("-a", "--audio-mask", action="append", type="string", dest="audioMask", default=G_AUDIO_MASK,
					  help="regex to match audio files. Submatch for match with video (e.s episodie number, season). Repeatable option.")
					  
	parser.add_option("-t", "--audio-target", action="append", type="string", dest="audioTarget", default=None,
					  help="directory where are audio to mux")
					  
	parser.add_option("-d", "--dest", type="string", dest="dest", default=None,
					  help="directory dest, where are saved muxed files. Default: same path of video-files")
					
	parser.add_option("-p", "--dest-postfix", type="string", dest="postfix", default=G_DEST_POSTFIX,
					  help="Muxed files postfix (es. video.avi => videopostfix.avi). Default: " + G_DEST_POSTFIX )
					  
	parser.add_option("-c", "--exec-cmd", type="string", dest="ffmpegCli", default=G_FFMPEG_CLI, metavar="EXECCMD",
					  help="program executed with matched viedo and audio (placeholder: %(video)s, %(audio)s %(dest)s)")
	
	parser.add_option("-s", "--trial", action="store_true", dest="trial", default=False,
					  help="perform a trial run with no changes made")
	
	parser.add_option("-v", "--verbose", action="count", dest="verbosity", default=g_verbosity,
					  help="Enable (and increase) verbosity. Repeatable option.")
	
	parser.add_option("-i", "--info", action="store_true", dest="info",
					  help="view default regex mask and exec-cmd")
	  
	(options, args) = parser.parse_args()
	
	# Manage param and error  
	
	if options.info is True:
		myPrint( 'Default regex mask:\n video: {0}\n audio: {1}\n'.format( G_VIDEO_MASK, G_AUDIO_MASK ), STR_STDOUT )
		myPrint( '\nnote:  overwrite regex mask with -m and -a options.\n', STR_STDOUT )
		myPrint( '\nDefault exec cmd: "{0}"\n'.format( options.ffmpegCli ), STR_STDOUT )
		myPrint( '\nnote: for set your execcmd, use -c and set correct placholder.\n\n', STR_STDOUT )
		sys.exit(0)
	
	if len(args) == 0:
		myPrint( clr( 'ERROR:', 4) + ' Set video-files!\n\n', STR_STDERR )
		parser.print_help()
		sys.exit(1)
	
	if options.dest is None:
		(filepath, filename) = os.path.split( args[0] )
		options.dest = filepath
	
	if options.audioTarget is None:
		options.audioTarget = args
		
	if options.trial is True:
		myPrint( clr( 'Trial mode: ON', 3 ) + ' (perform a trial run with no changes made)\n\n', STR_STDOUT )
	
	g_verbosity = options.verbosity
	
	# the core of app :)
	matched, successOnExec = muxVideoAudio( args, options.audioTarget, options.dest, options.postfix, options.videoMask, options.audioMask, execffmpegCli, options.ffmpegCli , options.trial)
	
	myPrint( "tot. matched: %d succes execcmd: %d/%d\n" % (matched, successOnExec, matched) , STR_STDOUT, 1, g_verbosity )
	
	# exit without errors
	sys.exit(0)
	
# Expand wildcards (*,?,[],~) in a list of path and return files list for directory
# @lstPath: list[string] - list of path to expand (dirs or files)
# @return: list[string] - expanded list
def expandWildCard( lstPath ):
	
	lstExpandedPath = []
	
	for path in lstPath:
		# expand ~ to HOME path
		lstPathGlobize = os.path.expanduser( path )
		# expand *.?.[] wildcards
		lstPathGlobize = glob.glob( lstPathGlobize )
		for pathGlobize in lstPathGlobize:
			# return file list for dir path
			if os.path.isdir(pathGlobize):
				for file in os.listdir( pathGlobize ):
					filePath = os.path.join( pathGlobize, file )
					if os.path.isfile( filePath ):
						lstExpandedPath.append( filePath )
			else:
				lstExpandedPath.append( pathGlobize )
	
	return lstExpandedPath
	
# Match Video with correct Audio file by compare sub-group finded with regex Mask
# @lstTargetVideo: list[string] - list of path video target
# @lstTargetAudio: list[string] - list of path audio target
# @lstVideoMask: list[string] - list of regex with sub-grup to match video files (es. (0?[0-9]{1,2})x(0?[0-9]{1,2}).*\.(?:avi|mpg))
# @lstAudioMask: list[string] - list of regex with sub-grup to match audio files (es. (0?[0-9]{1,2})x(0?[0-9]{1,2}).*\.(?:mp3|wav))
# @callBack: function - this function is call for each match with 2 params: videoFilename, audioFilename
# @return: int, int - matched and sugges 
def muxVideoAudio( lstTargetVideo, lstTargetAudio, dest, postfix, lstVideoMask = None, lstAudioMask = None, callBack = None, ffmpegCli = None, trial = False ):

	# get audio and video files list
	lstTargetAudio = expandWildCard(lstTargetAudio)
	lstTargetVideo = expandWildCard(lstTargetVideo)
	
	countMatched = 0
	countSuccessOnExec = 0
	
	# for each video search the correct audio (match on regex sub-group)
	for targetVideo in lstTargetVideo:
		
		# set True when find correct audio
		matched = False
		(filepathVideo, filenameVideo) = os.path.split(targetVideo)
		
		myPrint( "> target video: %s\n" % filenameVideo , STR_STDOUT, 2, g_verbosity )
		
		# for each videoMask: regex with sub-group (es. season and episodie) 
		for videoMask in lstVideoMask:
			
			if matched is True: break;
			
			# get sub-group: foo.S01E10.*.avi => ('01', '10')
			objMatchedVideo = re.search(videoMask, filenameVideo, re.IGNORECASE)
			# if not match => next videoMask
			if objMatchedVideo is None:
				myPrint( "  video mask '%s' not usable!\n" % videoMask , STR_STDOUT, 3, g_verbosity )
				continue
			
			# convert to list of int
			lstMatchedVideo = list(objMatchedVideo.groups())
			for i in range(len(lstMatchedVideo)): lstMatchedVideo[i] = int(lstMatchedVideo[i])
			
			myPrint( "  video mask '%s' match: %s\n" % ( videoMask, lstMatchedVideo ) , STR_STDOUT, 2, g_verbosity )
			
			# for each audio
			for targetAudio in lstTargetAudio:
				
				if matched is True: break;
				
				(filepathAudio, filenameAudio) = os.path.split(targetAudio)
				
				myPrint( "  + target audio: %s\n" % filenameAudio , STR_STDOUT, 2, g_verbosity )
				
				# for each audioMask: regex with sub-group (es. season and episodie)
				for audioMask in lstAudioMask:
					
					# get sub-group: foo.S01E10.*.mp3 => ('01', '10')
					objMatchedAudio = re.search(audioMask, filenameAudio, re.IGNORECASE)
					# if not match => next audioMask
					if objMatchedAudio is None:
						myPrint( "    audio mask '%s' not usable!\n" % audioMask , STR_STDOUT, 3, g_verbosity )
						continue
					
					# convert to list of int
					lstMatchedAudio = list(objMatchedAudio.groups())
					for i in range(len(lstMatchedAudio)): lstMatchedAudio[i] = int(lstMatchedAudio[i])
					
					myPrint( "    audio mask '%s' match: %s\n" % ( audioMask, lstMatchedAudio ) , STR_STDOUT, 2, g_verbosity )
					
					if lstMatchedVideo == lstMatchedAudio:
						myPrint( "Matched video (" + clr( os.path.join( filepathVideo, filenameVideo ), 2 ) + ") and audio (" + clr( os.path.join( filepathAudio, filenameAudio ), 2 ) + ")!\n", STR_STDOUT, 1, g_verbosity )
						retCode = callBack( os.path.join( filepathVideo, filenameVideo ), os.path.join( filepathAudio, filenameAudio ), dest, postfix, ffmpegCli, trial )
						
						if( retCode is 0 ): countSuccessOnExec +=1
						
						countMatched += 1
						matched = True
						break
					else:
						myPrint( "    not match: '%s' with '%s'\n" % ( filenameVideo , filenameAudio ), STR_STDOUT, 3, g_verbosity )
	return countMatched, countSuccessOnExec

# Execute ffmpegCli
# @videoFile: string - video file full path
# @audioFile: string - audio file full path
# @dest: string - path to dest
# @postfix: string - filname postfix (es. video.avi => videoPOSTFIX.avi)
# @ffmpegCli: string - execcmd with placeholder: %(video)s, %(audio)s, %(dest)s
# @trial: bool - don't execute cmd
# @return: int - value returned from execcmd
def execffmpegCli( videoFile, audioFile, dest, postfix, ffmpegCli, trial = False ):
	
	# create full dest file path with prefix (es. /path/do/dest/<video-filename><postfix>.ext)
	(path, filename) = os.path.split(videoFile)
	(shortname, extension) = os.path.splitext(filename)
	dest = os.path.join(dest, shortname + postfix + extension)
	
	ffmpegCli = ffmpegCli % {"video": videoFile, "audio": audioFile, "dest": dest}
	
	if( trial ): 
		myPrint( "fake exec: " + ffmpegCli + '\n' ) 
		retCode = 0
	else:
		retCode = subprocess.call( ffmpegCli, shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w') )
		myPrint( "executed: %s ...with exit code: %d\n" % ( ffmpegCli, retCode), STR_STDOUT, 1, g_verbosity )
		
		# Manage return code
		#if retCode != 0:
		#	if ret < 0:
		#		print "Killed by signal", -ret
		#	else:
		#		print "Command failed with return code", ret
		#else:
		#	print "SUCCESS!! %d" % ret
	return retCode

	
STR_STDOUT = 0
STR_STDERR = 1
# Print on screen follow verbosity and stream type
# @text: string - text to print
# @streamType: int - STR_STDOUT or STR_STDERR
# @verbosity: int - verbosity associed to text
# @requestVerbosity: int - request verbosity
# @return: bool - return if printed
def myPrint( text, streamType = STR_STDOUT, verbosity = 1 , requestVerbosity = 1 ):
	
	if verbosity <= requestVerbosity:
		
		if streamType == STR_STDOUT:
			sys.stdout.write( text )
		else: 
			sys.stderr.write( text )
		return True
	else:
		return False
		
		
G_COLOR = ( '\033[95m', '\033[94m', '\033[92m', '\033[93m', '\033[91m' )
G_COLOR_ENDC = '\033[0m'
# Colorize string
# @string: string - text to colorize
# @color: int - color type, see G_COLOR tuple
# @return: string - return colored string
def clr( string, color ):
	
	return G_COLOR[color] + string + G_COLOR_ENDC
	
if __name__ == "__main__":
	main()
	


