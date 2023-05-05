from type_lib import FileCheckReport, CDJSpecs, TrackManager

import os
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import numpy as np


class LibraryManager:
    def __init__(self, source_lib: str, mode: str, cdj_specs: CDJSpecs, target_lib: str = None):
        self.mode = mode.lower()
        assert self.mode in ['copy', 'replace'], "Choose 'copy' or 'replace' mode!"
        if self.mode == 'copy':
            assert target_lib is not None, "Specify target lib in copy mode!"

        self.source = source_lib
        self.target = target_lib
        self.cdj_specs = cdj_specs
        self.ignore = 'PIONEER'
        self.library_size = 0

        self.faulty_files = {}
        self.tracks_by_file_type = {'other': []}
        for file_type_name in self.cdj_specs.file_type_dict:
            self.tracks_by_file_type[file_type_name] = []
            self.faulty_files[file_type_name] = []

    def scrape_library(self):
        for root, dirs, files in os.walk(self.source):
            if self.ignore not in root:
                for f in files:
                    self.library_size += 1
                    extension = os.path.splitext(f)[1]
                    if extension not in self.cdj_specs.extensions:
                        self.tracks_by_file_type['other'].append(os.path.join(root, f))

                    else:
                        for i, extensions in enumerate(self.cdj_specs.extensions_dict.values()):
                            if extension in extensions:
                                self.tracks_by_file_type[list(self.cdj_specs.extensions_dict.keys())[i]].append(
                                    os.path.join(root, f))

        print(f"Library scraped, found {self.library_size:6.0f} files.")

    def diagnose_library(self):
        for file_type_name, paths in self.tracks_by_file_type.items():
            if file_type_name == 'other':
                continue
            print(f"\nDiagnosing {file_type_name} files...")
            file_type = self.cdj_specs.file_type_dict[file_type_name]
            manager = file_type.track_manager

            for audio in paths:
                print(f"\nDiagnosing {audio}...")
                manager.track_path = audio
                report = manager.diagnose_file()
                if np.any(report.error_array):
                    self.faulty_files[file_type_name].append(report)

    def fix_library(self):
        for file_type_name, reports in self.faulty_files.items():
            print(f"\nFixing {file_type_name} files...")
            file_type = self.cdj_specs.file_type_dict[file_type_name]
            manager = file_type.track_manager

            for report in reports:
                print(f"\nFixing {report.file_path}...")
                manager.treat_file(report)


class MP3Manager(TrackManager):
    def __init__(self, **kwargs):
        self.name = 'MP3 Reader'
        super().__init__(**kwargs)

    def open_file(self):
        assert self.track_path is not None, "Specify track path!"
        self.audio = MP3(self.track_path)

    def diagnose_file(self):
        self.open_file()
        self.update_stream_info()
        f_format = self.file_type.get_file_format_by_version(version=self.stream_info.version)
        report = FileCheckReport(file_path=self.track_path)

        if self.stream_info.bitrate < f_format.bit_rate[0] or self.stream_info.bitrate > f_format.bit_rate[1]:
            report.bit_rate_error = True

        if self.stream_info.sample_rate not in f_format.sampling_frequencies:
            report.sample_rate_error = True

        if self.stream_info.layer != f_format.layers:
            report.layer_error = True

        report.update_status_array()

        if not np.any(report.error_array):
            print("All checks passed.")
            print(self.stream_info.pprint())

        else:
            print('Conflict found!')
            if report.bit_rate_error:
                print(f"Bit rate conflict! \n"
                      f"Required: {f_format.bit_rate[0]} to {f_format.bit_rate[1]}\n"
                      f"Actual: {self.stream_info.bitrate}")

            if report.sample_rate_error:
                print(f"Sample rate rate conflict! \n"
                      f"Required: {f_format.sampling_frequencies}"
                      f"Actual: {self.stream_info.sample_rate}")

        return report


    def treat_file(self):
        pass


class WAVManager(TrackManager):
    def __init__(self, **kwargs):
        self.name = 'WAV Reader'
        super().__init__(**kwargs)

    def open_file(self):
        assert self.track_path is not None, "Specify track path!"
        self.audio = WAVE(self.track_path)

    def diagnose_file(self):
        self.open_file()
        self.update_stream_info()
        f_format = self.file_type.file_formats[0]
        report = FileCheckReport(file_path=self.track_path)

        if self.stream_info.sample_rate not in f_format.sampling_frequencies:
            report.sample_rate_error = True

        if self.stream_info.channels not in [1, 2]:
            print(self.stream_info.channels)
            report.wav_header_error = True

        with open(self.track_path, "rb") as f:
            f.seek(20, 0)
            if f.read(2) != b'\x01\x00':
                report.wav_header_error = True
                # new_header = header[:20] + b'\x01\x00' + header[22:]
                # with open(file_path, "wb") as f_out:
                #     f_out.write(new_header)
                # print(f"Fixed wrong bytes in header.")

        report.update_status_array()
        if not np.any(report.error_array):
            print("All checks passed.")
            print('Stream Info:', self.stream_info.pprint())

        else:
            print('Conflict found!')

            if report.sample_rate_error:
                print(f"Sample rate conflict!"
                      f"Required: {f_format.sampling_frequencies}"
                      f"Actual: {self.stream_info.sample_rate}")

            if report.wav_header_error:
                print(f"Detected wrong bytes in header.")

        return report

    def treat_file(self, report: FileCheckReport):
        if report.wav_header_error:
            with open(report.file_path, "rb+") as f:
                f.seek(20, 0)
                fixed_bytes = b'\x01\x00'
                f.write(fixed_bytes)

            print(f"Fixed faulty bytes in header.")
