# Fixes CRLF issues for battlezone
# Operates on all files in folder or specific files

import argparse
import glob
import subprocess
import re
import os
from utils import is_binary_file
from pydub import AudioSegment
from gtts import gTTS

parser = argparse.ArgumentParser(description='TXT -> WAV')
parser.add_argument('path',help='file or directory to operate on')

args = parser.parse_args()

def espeakSay(text,voice="en",out="tmp.wav",speed=175):
  subprocess.call('espeak "{}" -v {} -s {} -w {}'.format(text,voice,speed,out),shell=True)
  return "wav"

def googleSay(text,lang="en",out="tmp.wav"):
  tts = gTTS(text, lang)
  tts.save(out)
  return "mp3"

def say(voice_d,text,out="tmp.wav",speed):
  if(voice_d[0] == "GOOGLE"):
    return googleSay(text,voice_d[1],out)
  else
    return espeakSay(text,voice_d[1],out)

if(os.path.isfile(args.path)):
  files = [args.path]
else:
  files = [n for n in glob.glob("{}/*.txdi".format(args.path)) if not is_binary_file(n)]


def interpretFile(fileName,context={}):
  cmds = []
  dic = os.path.dirname(os.path.realpath(fileName))
  with open(fileName,'r') as f:
    content = f.read()
    parts = re.split("START",content)
    meta = parts[0]
    for line in meta.split("\n"):
      tokens = line.split(" ")
      if(tokens[0] == "PARENT"):
        cmds = cmds + interpretFile(dic + "/" + tokens[1],context)
      elif(tokens[0] == "VOICE"):
        
        context[tokens[1]] = tokens[2:]
    if(len(parts) > 1):
      body = parts[1].replace("\n","")
      diags = body.split(";")
      for diag in diags:
        s = diag.split(":")
        if(len(s) > 1):
          person, data = s
          segments = re.split("\[(\d+)\]",data)
          for i in range(0,len(segments),2):
            if(segments[i].strip()):
              cmds.append({"voice": context[person],"text": segments[i].strip(), "delay": int(segments[i+1]) if (i+1) < len(segments) else 0})
  return cmds

for file in files:
  try:
    uext = os.path.realpath(file).lower().split(".")[0]
    cmds = interpretFile(file)
    fileIndex = 0
    for i in cmds:
      i["file"] = "tmp_voice_{}.wav".format(fileIndex)
      i["format"] = say(i["voice"],i["text"],i["file"])
      fileIndex += 1
    
    out_audio = AudioSegment.empty()
    for i in cmds:
      out_audio += AudioSegment.from_file(i["file"],format=i["format"])
      if(i["delay"] > 0):
        out_audio += AudioSegment.silent(duration=i["delay"])
      os.remove(i["file"])
    out_audio.export("{}.wav".format(uext),format="wav")
  except:
    print("Failed to generate audio for {}".format(file))
