import enum
import logging

logger = logging.getLogger(__name__)


class BytestreamBuffer(object):
    GCM_TAG_LENGTH = 12

    class States(enum.Enum):
        NEW = 0
        START_BYTE = 1
        SYSTEM_TITLE = 2
        DATA_LENGTH = 3
        FRAME_COUNTER = 4
        RESULT = 5
        STATE_INVALID = 99

    def __init__(self) -> None:
        self._state = self.States.NEW
        self._start = 0
        self._buffer = bytearray()
        self._encrypted_telegram = bytearray()
        self._data_length = 0
        self._system_title_length = -1
        self._system_title = None
        self._frame_counter = None

    def _check_state(self) -> None:
        """Continuously checks the state in the buffer. Target is to finally reach
        ``State.RESULT``.
        """
        buffer_length = len(self._buffer)

        if self._state == self.States.STATE_INVALID:
            logger.error(
                'Message buffer is already invalidated - no state detection possible!'
            )
            return self._state

        # Desired state: START_BYTE
        if self._state == self.States.NEW:
            end = self._start + 1
            # start byte 0xDB
            if buffer_length == end:
                if self._buffer[self._start] != int('0xdb', 16):
                    logger.error(f'Start byte {self._buffer[self._start]} != 0xDB')
                    self._state = self.States.STATE_INVALID
                    return self._state

                self._start = end
                self._state = self.States.START_BYTE
                return self._state

        # Desired state: SYSTEM_TITLE
        if self._state == self.States.START_BYTE:
            # length of system title
            if (self._system_title_length == -1) and (buffer_length == self._start + 1):
                self._system_title_length = int(self._buffer[self._start])
                logger.debug(f"System title length: {self._system_title_length}")
                # We do not shift _start - on next parsing loop we still want to be on
                # original starting position

            if buffer_length == self._start + self._system_title_length + 2:
                # system title itself
                self._start = self._start + 1
                end = self._start + self._system_title_length
                self._system_title = self._buffer[self._start:end]
                logger.debug(f"System title: {self._system_title}")
                self._start = end

                # system title needs to be followed by fixed seperator 0x82
                end = self._start + 1
                if self._buffer[self._start] != int('0x82', 16):
                    logger.error(
                        f"Expected seperator 0x82 but got {self._buffer[self._start]}"
                    )
                    return self.States.STATE_INVALID

                self._start = end
                self._state = self.States.SYSTEM_TITLE
                return self._state

        # Desired state: DATA_LENGTH
        if self._state == self.States.SYSTEM_TITLE:
            if buffer_length == self._start + 3:

                # 2 bytes defining the length of data following
                end = self._start + 2
                self._data_length = int(self._buffer[self._start:end].hex(), 16)
                logger.debug(f"Data length: {self._data_length}")
                self._start = end

                # Data length must be followed by fixed seperator 0x30
                end = self._start + 1
                if self._buffer[self._start] != int('0x30', 16):
                    logger.error(
                        f"Expected seperator 0x30 but got {self._buffer[self._start]}"
                    )
                    return self.States.STATE_INVALID

                self._start = end
                self._state = self.States.DATA_LENGTH
                return self._state

        # Desired state: FRAME_COUNTER
        if self._state == self.States.DATA_LENGTH:
            # frame counter (4 bytes long)
            end = self._start + 4
            if buffer_length == end:
                self._bframe_counter = self._buffer[self._start:end]
                self._frame_counter = int(self._bframe_counter.hex(), 16)
                logger.debug(f"Frame counter: {self._frame_counter}")
                self._start = end
                self._state = self.States.FRAME_COUNTER
                return self._state

        # Desired state: RESULT
        if self._state == self.States.FRAME_COUNTER:
            if buffer_length == self._start + self._data_length - 5:

                # Extracting the encrypted frame
                end = self._start + (self._data_length - self.GCM_TAG_LENGTH - 5)
                self._encrypted_telegram = self._buffer[self._start:end]
                self._start = end

                # GCM TAG
                end = self._start + self.GCM_TAG_LENGTH
                self._gcm_tag = self._buffer[self._start:end]
                logger.debug(f"GCM Tag: {self._gcm_tag.hex()}")

                self._start = end
                self._state = self.States.RESULT
                return self._state

        return self._state

    def push_byte(self, data: bytes) -> States:
        """Push new data to buffer and immediatle check the state if a complete telegram
        message was found

        Args:
            data (bytes): encrypted data bytes as received from raw interface
        """
        self._buffer += data
        return self._check_state()

    @property
    def current_state(self) -> States:
        """current state in state machine
        """
        return self._state

    @property
    def encrypted_telegram(self) -> bytearray:
        """encrypted telegram as bytearray
        """
        return self._encrypted_telegram

    @property
    def system_title(self) -> bytearray:
        """system title provided in the unencrpyted part of the byte stream
        """
        return self._system_title

    @property
    def frame_counter(self) -> int:
        """frame counter as integer
        """
        return self._frame_counter

    @property
    def binary_frame_counter(self) -> bytearray:
        """frame counter integer as 4 byte array in big indian
        """
        return self._frame_counter.to_bytes(4, 'big')
