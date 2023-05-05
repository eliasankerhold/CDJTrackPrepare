from dataclasses import dataclass
from abc import ABC, abstractmethod
from mutagen import StreamInfo
from numpy.typing import NDArray
import numpy as np


@dataclass
class FileCheckReport:
    file_path: str
    bit_rate_error: bool = False
    sample_rate_error: bool = False
    bit_depth_error: bool = False
    layer_error: bool = False
    version_error: bool = False
    wav_header_error: bool = False
    error_array: NDArray = None

    def __post_init__(self):
        self.update_status_array()

    def update_status_array(self):
        self.error_array = np.array(
            [self.bit_rate_error, self.sample_rate_error, self.bit_depth_error, self.layer_error,
             self.version_error, self.wav_header_error], dtype=bool)


class TrackManager(ABC):
    def __init__(self, mode: str, track_path: str = None, stream_info: StreamInfo = None):
        self.track_path = track_path
        self.file_type = None
        self.audio = None
        self.mode = mode
        self.stream_info = stream_info

    def update_stream_info(self):
        assert self.audio is not None, "Open file first!"
        self.stream_info = self.audio.info

    @abstractmethod
    def open_file(self):
        pass

    @abstractmethod
    def diagnose_file(self) -> FileCheckReport:
        pass


@dataclass
class FileFormat:
    name: str
    sampling_frequencies: list[int]
    bit_rate: tuple[int, int] = None
    bit_depths: list[int] = None
    layers: int = None
    version: int = None


@dataclass
class FileType:
    name: str
    extensions: list[str]
    file_formats: list[FileFormat]
    track_manager: TrackManager

    def __post_init__(self):
        self.track_manager.file_type = self

    def get_file_format_by_version(self, version: int):
        for f in self.file_formats:
            if f.version == version:
                return f


@dataclass
class CDJSpecs:
    model: str
    _file_types: list[FileType]

    def __post_init__(self):
        self.extensions = [ex for i in self._file_types for ex in i.extensions]
        self.extensions_dict = {}
        self.file_type_dict = {}
        for f in self._file_types:
            self.file_type_dict[f.name] = f
            self.extensions_dict[f.name] = f.extensions
