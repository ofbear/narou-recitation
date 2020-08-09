import os
import sys

from configparser import ConfigParser

from mimi import Mimi
from narou import Narou

if __name__ == '__main__':
    config = ConfigParser()
    config.read(os.getcwd() + '\setting.conf')

    n = Narou('dailypoint')
    err, result = n.getrank()
    if err:
        print(result)
        sys.exit(1)

    auth = {
        'applicationId' : config.get('mimi', 'applicationId'),
        'clientId' : config.get('mimi', 'clientId'),
        'clientSecret' : config.get('mimi', 'clientSecret'),
        'scope' : eval(config.get('mimi', 'scope')),
    }

    m = Mimi(auth)

    for v in result:
        if 'title' not in v:
            continue

        title = v['title']
        story = v['story']

        if len(title) > 15:
            title = title[0:15] + '...'
        title += '.wav'

        if os.path.isfile(title):
            continue

        params = {
            'text' : story, # UTF-8
            'audio_format' : 'WAV', # WAV, RAW, ADPCM, Speex
            'audio_endian' : 'Little', # Little, Big
            'gender' : 'female', # female, male
            'age' : '14',
            'native' : 'yes', # yes, no
            'lang' : 'ja', # ja, en, id, ko, vi, my, th, zh, zh-TW
            'engine' : 'nict',
        }

        err, result = m.speech(params)
        if err:
            print(f'title:{title}')
            print(f'story:{story}')
            print(result)
            continue

        with open(title, 'wb') as fout:
            fout.write(result)

    print('OK')
