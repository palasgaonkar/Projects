import urllib
import json
import webbrowser
import os
import collections

data_dictionary = {}
replace = ["E SuB xRG", ".avi", "1.4", "5.1", "-", "DVDRip", "BRRip", "XviD", "1CDRip", "aXXo", "[", "]", "(", ")", "{",
           "}", "{{", "}}"
                      "x264", "720p", "DvDScr", "MP3", "HDRip", "WebRip", "ETRG", "YIFY", "StyLishSaLH",
           "StyLish Release", "TrippleAudio",
           "EngHindiIndonesian", "385MB", "CooL GuY", "a2zRG", "x264", "Hindi", "AAC", "AC3", "MP3", " R6", "HDRip",
           "H264", "ESub", "AQOS",
           "ALLiANCE", "UNRATED", "ExtraTorrentRG", "BrRip", "mkv", "mpg", "DiAMOND", "UsaBitcom", "AMIABLE", "BRRIP",
           "XVID", "AbSurdiTy",
           "DVDRiP", "TASTE", "BluRay", "HR", "COCAIN", "_", ".", "BestDivX", "MAXSPEED", "Eng", "500MB", "FXG", "Ac3",
           "Feel", "Subs", "S4A", "BDRip", "FTW", "Xvid", "Noir", "1337x", "ReVoTT",
           "GlowGaze", "mp4", "Unrated", "hdrip", "ARCHiViST", "TheWretched", "www", "torrentfive", "com", "1080p",
           "1080", "SecretMyth", "Kingdom", "Release", "RISES", "DvDrip", "ViP3R", "RISES", "BiDA", "READNFO",
           "HELLRAZ0R", "tots", "BeStDivX", "UsaBit", "FASM", "NeroZ", "576p", "LiMiTED", "Series", "ExtraTorrent",
           "DVDRIP", "~",
           "BRRiP", "699MB", "700MB", "greenbud", "B89", "480p", "AMX", "007", "DVDrip", "h264", "phrax", "ENG", "TODE",
           "LiNE",
           "XVid", "sC0rp", "PTpower", "OSCARS", "DXVA", "MXMG", "3LT0N", "TiTAN", "4PlayHD", "HQ", "HDRiP", "MoH",
           "MP4", "BadMeetsEvil",
           "XViD", "3Li", "PTpOWeR", "3D", "HSBS", "CC", "RiPS", "WEBRip", "R5", "PSiG", "'GokU61", "GB", "GokU61",
           "NL", "EE", "Rel", "NL",
           "PSEUDO", "DVD", "Rip", "NeRoZ", "EXTENDED", "DVDScr", "xvid", "WarrLord", "SCREAM", "MERRY", "XMAS", "iMB",
           "7o9",
           "Exclusive", "171", "DiDee", "v2", "Scr", "SaM", "MOV", "BRrip", "CharmeLeon", "Silver RG", "1xCD", "DDR",
           "1CD", "X264", "ExtraTorrenRG",
           "Srkfan", "UNiQUE", "Dvd", "crazy torrent", "Spidy", "PRiSTiNE", "HD", "Ganool", "TS", "BiTo", "ARiGOLD",
           "rip", "Rets", "teh", "ChivveZ", "song4",
           "playXD", "LIMITED", "600MB", "700MB", "900MB"

]


def finder(subdir):
    all_subdirs = [d for d in os.listdir(subdir)]

    for name in all_subdirs:


        year = 0
        for y in range(1900, 2014):
            if str(y) in name:
                name = name.replace(str(y), " ")
                year = y
                break
        for value in replace:
            name = name.replace(value, " ")

        name = name.lstrip()
        name = name.rstrip()

        datalist = []

        if year != 0:
            url = "http://www.omdbapi.com/?t=" + name + "&y=" + str(year)

        else:
            url = "http://www.omdbapi.com/?t=" + name

        response = urllib.urlopen(url).read()
        jsonvalues = json.loads(response)
        if jsonvalues["Response"] == "True":
            imdbrating = jsonvalues['imdbRating']
            imdburl = "http://www.imdb.com/title/" + jsonvalues['imdbID']
            imdbgenre = jsonvalues['Genre']
            imdbyear = jsonvalues['Year']
            imdbruntime = jsonvalues['Runtime']
            imdbactors = jsonvalues['Actors']
            imdbplot = jsonvalues['Plot']
            imdbawards = jsonvalues['Awards']


        else:
            imdbrating = "Could not find"
            imdburl = "NA"
            imdbgenre = "NA"
            imdbyear = "NA"
            imdbruntime = "NA"
            imdbactors = "NA"
            imdbplot = "NA"
            imdbawards = "NA"

        moviename = name
        datalist.append(imdbrating.encode('utf-8'))
        datalist.append(imdbgenre.encode('utf-8'))
        datalist.append(imdburl.encode('utf-8'))
        datalist.append(imdbyear.encode('utf-8'))
        datalist.append(imdbruntime.encode('utf-8'))
        datalist.append(imdbactors.encode('utf-8'))
        datalist.append(imdbplot.encode('utf-8'))
        datalist.append(imdbawards.encode('utf-8'))

        if moviename not in data_dictionary:
            data_dictionary[moviename] = datalist

    sorted_dict = collections.OrderedDict(reversed(sorted(data_dictionary.items(), key=lambda t: t[1][0])))
    if os.path.isfile("moviefile.xls"):
        os.remove("moviefile.xls")
    with open("moviefile.xls", "ab+") as data:
        data.write("Movie Name\tRating\tGenre\tUrl\tYear\tRuntime\tActors\tPlot\tAwards\n")
    for movie, [rating, genre, url, year, runtime, actors, plot, awards] in sorted_dict.iteritems():
        with open("moviefile.xls", "ab+") as data:
            data.write(
                str(movie) + "\t" + str(rating) + "\t" + str(genre) + "\t" + str(url) + "\t" + str(year) + "\t" + str(
                    runtime) +
                "\t" + str(actors) + "\t" + str(plot) + "\t" + str(awards) + "\n")
    webbrowser.open("moviefile.xls")

#folder = sys.argv[1]
finder('/home/likewise-open/PUNESEZ/vishal.palasgaonkar/Fun/imdb')