from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
import re

####################################################################################################

PLUGIN_TITLE = 'Wilkommen Osterreich'
PLUGIN_PREFIX = '/video/wilkommen'

# http://85.124.236.114/Folge97/F97P2/F97P2.mp4
URLS = [ "http://willkommen-tv.at/player.php?fid=start", "http://85.124.236.114/Folge%s/F%sP%s/F%sP%s.flv", "http://85.124.236.114/Folge%s/F%sP%s/F%sP%s.mp4" ]

# http://willkommen-tv.at/content/images/vidscr/F80/F80P2.jpg
THUMB_URL = 'http://willkommen-tv.at/content/images/vidscr/F%s/F%sP%s.jpg'
CACHE_INTERVAL = 3600

# Default artwork and icon(s)
PLUGIN_ARTWORK = 'art-default.png'
PLUGIN_ICON_DEFAULT = 'icon-default.png'
PLUGIN_ICON_PREFS = 'icon-prefs.png'

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE)

  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('Details', viewMode='InfoList', mediaType='items')

  # Set the default MediaContainer attributes
  MediaContainer.title1 = PLUGIN_TITLE
  MediaContainer.viewGroup = 'List'
  MediaContainer.art = R(PLUGIN_ARTWORK)

  # Set the default cache time
  HTTP.SetCacheTime(CACHE_INTERVAL)

####################################################################################################

def MainMenu():
  mc = MediaContainer(noCache=True)
  

  site = XML.ElementFromURL(URLS[0], isHTML=True, errors='ignore')
  numEpisodes = 0
  for aElem in site.xpath("//a"):
    aId = aElem.get("id")
    if(aId and aId[0] == "F"):
      numEpisodes+=1

  Log("Episodes:"+str(numEpisodes), debugOnly=False)
  Log(site)

  for episode in range(1, numEpisodes+1):
    title = F("EPISODE", str(episode))
    #mc.Append(VideoItem(url, title=title))
    thumb = THUMB_URL % (episode, episode, 2)
    mc.Append(Function(DirectoryItem(Parts, title=title, thumb=thumb), title=title, episode=episode))

  #mc.Append(PrefsItem(L("PREFERENCES"), thumb=R(PLUGIN_ICON_PREFS)))
  return mc

####################################################################################################

def Parts(sender, title, episode):
  dir = MediaContainer(title2=title, viewGroup='Details')
  
  for part in range(1, 7):
    if episode < 80:
      url = URLS[1] % (episode, episode, str(part), episode, str(part))
    else:
      url = URLS[2] % (episode, episode, str(part), episode, str(part))
    Log(url)
    thumb = THUMB_URL % (episode, episode, part)
    dir.Append(VideoItem(url, title="Part "+str(part), thumb=thumb))
    
  return dir