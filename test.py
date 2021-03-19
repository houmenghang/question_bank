import json
import os
from time import sleep
'''
data = json.load(open('bjjt_info.json', 'r'))

bjjt = []
for paging in data:
    for video_info in paging["data"]["list"]:
        data_info = {}
        for key in video_info.keys():
            data_info[key] = video_info[key]
        bjjt.append(data_info)
                                                                                                                                                                                                                                       
with open('bjjt.json', 'w+', encoding='utf-8') as f:
    json.dump(bjjt, f, ensure_ascii=False)
'''

data = json.load(open('data.json', 'r', encoding='utf-8'))
video_output_path = r'\\192.168.1.100\data\houmenghang\test\video\百家讲坛'
audio_output_path = r'\\192.168.1.100\data\houmenghang\test\audio\百家讲坛'
for key in data.keys():
    for videoinfo in data[key]:
        os.makedirs(os.path.join(video_output_path, key), exist_ok=True)
        os.makedirs(os.path.join(audio_output_path, key), exist_ok=True)
        sub_video_output_path = os.path.join(video_output_path, key)
        sub_audio_output_path = os.path.join(audio_output_path, key)
        video_file = os.path.join(
            sub_video_output_path, '{}.mp4'.format(videoinfo["title"]))
        audio_file = os.path.join(
            sub_audio_output_path, '{}.mp3'.format(videoinfo["title"]))

        if not os.path.exists(audio_file):
            video_shell = 'you-get --debug -o {} -O "{}" {}'.format(sub_video_output_path,
                                                                    videoinfo['title'],
                                                                    videoinfo['url'].replace(
                                                                        '\\', '')
                                                                    )
            os.system(video_shell)
            audio_shell = 'ffmpeg -i "{}" -f mp3 "{}"'.format(
                video_file, audio_file)
            os.system(audio_shell)
            if os.path.exists(audio_file):
                del_video_shell = 'del "{}"'.format(video_file)
                os.system(del_video_shell)
            with open('download.log', 'a+', encoding='utf-8') as f:
                f.write('{} {} is done \n'.format(key, videoinfo["title"]))
