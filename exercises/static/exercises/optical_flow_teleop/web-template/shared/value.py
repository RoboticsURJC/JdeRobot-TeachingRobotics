import numpy as np
import mmap
from posix_ipc import Semaphore, O_CREX, ExistentialError, O_CREAT, SharedMemory, unlink_shared_memory
from ctypes import sizeof, memmove, addressof, create_string_buffer, c_float
import struct

class SharedValue:
    def __init__(self, name):
        # Initialize varaibles for memory regions and buffers and Semaphore
        self.shm_buf = None; self.shm_region = None
        self.value_lock = None

        self.shm_name = name; self.value_lock_name = name

        # Initialize shared memory buffer
        try:
            self.shm_region = SharedMemory(self.shm_name)
            self.shm_buf = mmap.mmap(self.shm_region.fd, sizeof(c_float))
            self.shm_region.close_fd()
        except ExistentialError:
            self.shm_region = SharedMemory(self.shm_name, O_CREAT, size=sizeof(c_float))
            self.shm_buf = mmap.mmap(self.shm_region.fd, self.shm_region.size)
            self.shm_region.close_fd()

        # Initialize or retreive Semaphore
        try:
            self.value_lock = Semaphore(self.value_lock_name, O_CREX)
        except ExistentialError:
            value_lock = Semaphore(self.value_lock_name, O_CREAT)
            value_lock.unlink()
            self.value_lock = Semaphore(self.value_lock_name, O_CREX)

        self.value_lock.release()

    # Get the shared value
    def get(self):
        # Retreive the data from buffer
        self.value_lock.acquire()
        value = struct.unpack('f', self.shm_buf)[0]
        self.value_lock.release()

        return value

    # Add the shared value
    def add(self, value):
        # Send the data to shared regions
        self.value_lock.acquire()
        self.shm_buf[:] = struct.pack('f', value)
        self.value_lock.release()

    # Destructor function to unlink and disconnect
    def close(self):
        self.value_lock.acquire()
        self.shm_buf.close()

        try:
            unlink_shared_memory(self.shm_name)
        except ExistentialError:
            pass

        self.value_lock.release()
        self.value_lock.close()
