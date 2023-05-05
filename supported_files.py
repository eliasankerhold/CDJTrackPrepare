from type_lib import FileType, FileFormat, CDJSpecs
from handling_lib import MP3Manager, WAVManager

mp3_reader = MP3Manager(mode=None)
wav_reader = WAVManager(mode=None)

# MP3
mpeg_1_format = FileFormat(name='MPEG-1 AUDIO LAYER-3',
                           bit_rate=(32000, 320000),
                           sampling_frequencies=[32000, 44100, 48000],
                           version=1,
                           layers=3)

mpeg_2_format = FileFormat(name='MPEG-2 AUDIO LAYER-3',
                           bit_rate=(8000, 160000),
                           sampling_frequencies=[16000, 22050, 24000],
                           version=2,
                           layers=3)

mp3_type = FileType(name='MP3',
                    extensions=['.mp3'],
                    file_formats=[mpeg_1_format, mpeg_2_format],
                    track_manager=mp3_reader)

# AAC
aac_2_format = FileFormat(name='MPEG-2 AAC LC',
                          bit_rate=(16000, 320000),
                          sampling_frequencies=[16000, 22050, 24000, 32000, 44100, 48000],
                          version=2)

aac_4_format = FileFormat(name='MPEG-2 AAC LC',
                          bit_rate=(16000, 320000),
                          sampling_frequencies=[16000, 22050, 24000, 32000, 44100, 48000],
                          version=4)

# aac_type = FileType(name='AAC',
#                     extensions=['.m4a', '.aac', '.mp4'],
#                     file_formats=[aac_2_format, aac_4_format])

# WAVE
wav_format = FileFormat(name='WAV',
                        sampling_frequencies=[44100, 48000],
                        bit_depths=[16, 24])

wav_type = FileType(name='WAV',
                    extensions=['.wav'],
                    file_formats=[wav_format],
                    track_manager=wav_reader)

# AIFF
aiff_format = FileFormat(name='AIFF',
                         sampling_frequencies=[44100, 48000],
                         bit_depths=[16, 24])

# aiff_type = FileType(name='AIFF',
#                      extensions=['.aiff', '.aif'],
#                      file_formats=[aiff_format])

# CDJ NEXUS 2000
cdj_nxs_2000_specs = CDJSpecs(model='CDJ Nexus 2000', _file_types=[mp3_type, wav_type])
