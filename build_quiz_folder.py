from lxml import etree
import os
import datetime
import shutil
import collections
import posixpath
import zipfile
import sys

# Global variables for silent mp3s and Score Sheet
audio_folder = r'F:\GWD\Quiz Cue Music and 4 Second Silent MP3'
score_sheet = r'F:\GWD\GWD OFFICIAL Open Office Scoresheet.ods'

# Locates 4 second and 8 second mp3s in mp3s folder
def get_silence_mp3s(path):
    silence_paths = []
    for o in os.scandir(path):
        if o.name == 'Silence - 4 seconds.mp3':
            silence_paths.append(o.path)
        elif o.name == 'Silence - 8 seconds.mp3':
            silence_paths.append(o.path)
    if silence_paths:
        return silence_paths

# Builds playlist order
# 8s silence -> R2Q1 -> 4s silence -> R2Q1 (repeat) -> 8s Silence -> R2Q2... etc.
# R2 and R7 are on the same playlist
def audio_rounds_dict(quiz_folder):
    
    if not os.path.exists(audio_folder):
        print('\n\n')
        print("{} is not a valid path!".format(audio_folder))
        print('\n\n')
        return None
    
    audio_rounds_dict = collections.OrderedDict()
    silence_paths = get_silence_mp3s(audio_folder)
    
    if silence_paths[0].startswith('/'):
        four_sec = posixpath.join('file:///', silence_paths[0][1:])
        eight_sec = posixpath.join('file:///', silence_paths[1][1:])
    else:
        four_sec = posixpath.join('file:///', silence_paths[0])
        eight_sec = posixpath.join('file:///', silence_paths[1])
        
    f_list = sorted(os.scandir(quiz_folder), key=lambda x: x.name)
    for o in f_list:
        if o.name.startswith('R'):
            if o.name.endswith('.zip'):
                with zipfile.ZipFile(o.path, 'r') as zip_ref:
                    extract_dir_name = o.name.replace('.zip', '')
                    extract_dir = os.path.join(os.path.dirname(o.path), extract_dir_name)
                    zip_ref.extractall(extract_dir)
                os.remove(o.path)
                
    f_list = sorted(os.scandir(quiz_folder), key=lambda x: x.name)
    for o in f_list:
        if o.is_dir():       
            if o.name.startswith('R'): 
                for root, dirs, files in os.walk(o.path):
                    for d in dirs:
                        if d == '__MACOSX':
                            shutil.rmtree(os.path.join(root, d))
                    for f in sorted(files):
                        if f.endswith('.mp3'):
                            if o.name not in audio_rounds_dict:
                                audio_rounds_dict[o.name] = []
                                audio_rounds_dict[o.name].append(eight_sec)
                            f_path = posixpath.join(root, f)
                            if f_path.startswith('/'):
                                f_path = posixpath.join('file:///', f_path[1:])
                            else:
                                f_path = posixpath.join('file:///', f_path)
                            audio_rounds_dict[o.name].append(f_path)
                            audio_rounds_dict[o.name].append(four_sec)
                            audio_rounds_dict[o.name].append(f_path)
                            audio_rounds_dict[o.name].append(eight_sec)

    return audio_rounds_dict

# Creates etree object for playlist XML
def build_playlist(rounds_dict):
    nsmap = {'vlc':"http://www.videolan.org/vlc/playlist/ns/0/"}
    playlist = etree.Element('playlist', nsmap=nsmap)
    playlist.attrib['xmlns'] = 'http://xspf.org/ns/0/'
    playlist.attrib['version'] = '1'

    title = etree.Element('title')
    title.text = 'Playlist'
    playlist.append(title)

    tracklist = etree.Element('trackList')
    playlist.append(tracklist)


    index_counter = 0

    for key, value in rounds_dict.items():
        for v in value:
            
            track = etree.Element('track')

            location = etree.Element('location')
            location.text = v
            track.append(location)

            extension = etree.Element('extension')
            extension.attrib['application'] = "http://www.videolan.org/vlc/playlist/0"

            vlc = etree.Element('{http://www.videolan.org/vlc/playlist/ns/0/}id')
            vlc.text = str(index_counter)
            index_counter += 1
            extension.append(vlc)
            
            track.append(extension)
            tracklist.append(track)

    playlist_tree = etree.ElementTree(playlist)
    return playlist_tree

def build_quiz(quiz_folder):
    
    # Unzips folder if still zipped
    if quiz_folder.endswith('.zip'):
        print("Unzipping {}".format(os.path.basename(quiz_folder)))
        orig_zip = quiz_folder
        with zipfile.ZipFile(quiz_folder, 'r') as zip_ref:
            extract_dir_name = quiz_folder.replace('.zip', '')
            extract_dir = os.path.join(os.path.dirname(quiz_folder), extract_dir_name)
            zip_ref.extractall(extract_dir)
            quiz_folder = extract_dir
        
    # Gets quiz folder name
    if quiz_folder[-1] == '/' or quiz_folder[-1] == '\\':  
        quiz_folder_name = os.path.basename(quiz_folder[:-1])
    else:
        quiz_folder_name = os.path.basename(quiz_folder)

    # Creates playlist order using audio_rounds_dict()
    print("Building VLC Playlist")
    rounds_dict = audio_rounds_dict(quiz_folder)
    if not rounds_dict:
        return None

    # Builds playlist etree object using build_playlist()
    playlist_tree = build_playlist(rounds_dict)
    playlist_path = os.path.join(quiz_folder, '{}_audio_rounds.xspf'.format(quiz_folder_name))
    playlist_tree.write(playlist_path, xml_declaration=True, encoding='utf-8')

    # Copies scoresheet and renames it based on the quiz folder title
    print("Copying Score Sheet into Quiz Folder")
    fn, ext = os.path.splitext(score_sheet)
    quiz_scores_orig = os.path.join(quiz_folder, os.path.basename(score_sheet))
    quiz_scores = os.path.join(quiz_folder, '{}_scores{}'.format(quiz_folder_name, ext))
    shutil.copy(score_sheet, quiz_scores_orig)
    os.rename(quiz_scores_orig, quiz_scores)

    # Prints path to quiz folder
    print("\n")
    msg = "Prepared quiz folder can be found here:"
    print("*" * len(msg))
    print(msg)
    print(quiz_folder)
    print("*" * len(msg))
    print("\n")

    
if __name__ == '__main__':
    path = sys.argv[-1]
    path = os.path.realpath(path)
    if not os.path.exists(path):
        print("{} does not exist".format(path))
    else:
        build_quiz(path)
