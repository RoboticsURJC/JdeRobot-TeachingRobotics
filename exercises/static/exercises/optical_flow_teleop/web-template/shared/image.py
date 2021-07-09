import numpy as np
import mmap
from posix_ipc import Semaphore, O_CREX, ExistentialError, O_CREAT, SharedMemory, unlink_shared_memory
from ctypes import sizeof, memmove, addressof, create_string_buffer
from structure_img import MD

# Probably, using self variables gives errors with memmove
# Therefore, a global variable for utility
md_buf = create_string_buffer(sizeof(MD))

class SharedImage:
    def __init__(self, name):
        # Initialize variables for memory regions and buffers and Semaphore
        self.shm_buf = None; self.shm_region = None
        self.md_buf = None; self.md_region = None
        self.image_lock = None

        self.shm_name = name; self.md_name = name + "-meta"
        self.image_lock_name = name

        # Initialize or retreive metadata memory region
        try:
            self.md_region = SharedMemory(self.md_name)
            self.md_buf = mmap.mmap(self.md_region.fd, sizeof(MD))
            self.md_region.close_fd()
        except ExistentialError:
            self.md_region = SharedMemory(self.md_name, O_CREAT, size=sizeof(MD))
            self.md_buf = mmap.mmap(self.md_region.fd, self.md_region.size)
            self.md_region.close_fd()

        # Initialize or retreive Semaphore
        try:
            self.image_lock = Semaphore(self.image_lock_name, O_CREX)
        except ExistentialError:
            image_lock = Semaphore(self.image_lock_name, O_CREAT)
            image_lock.unlink()
            self.image_lock = Semaphore(self.image_lock_name, O_CREX)

        self.image_lock.release()

    # Get the shared image
    def get(self):
        # Define metadata
        metadata = MD()

        # Get metadata from the shared region
        self.image_lock.acquire()
        md_buf[:] = self.md_buf
        memmove(addressof(metadata), md_buf, sizeof(metadata))
        self.image_lock.release()

        # Try to retreive the image from shm_buffer
        # Otherwise return a zero image
        try:
            self.shm_region = SharedMemory(self.shm_name)
            self.shm_buf = mmap.mmap(self.shm_region.fd, metadata.size)
            self.shm_region.close_fd()

            self.image_lock.acquire()
            image = np.ndarray(shape=(metadata.shape_0, metadata.shape_1, metadata.shape_2),
                               dtype='uint8', buffer=self.shm_buf)
            self.image_lock.release()

            # Check for a None image
            if(image.size == 0):
                image = np.zeros((3, 3, 3), np.uint8)

        except ExistentialError:
            image = np.zeros((3, 3, 3), np.uint8)

        return image

    # Add the shared image
    def add(self, image):
        # Get byte size of the image
        byte_size = image.nbytes
        
        # Get the shared memory buffer to read from
        if not self.shm_region:
            self.shm_region = SharedMemory(self.shm_name, O_CREAT, size=byte_size)
            self.shm_buf = mmap.mmap(self.shm_region.fd, byte_size)
            self.shm_region.close_fd()

        # Generate meta data
        metadata = MD(image.shape[0], image.shape[1], image.shape[2], byte_size)

        # Send the meta data and image to shared regions
        self.image_lock.acquire()
        memmove(md_buf, addressof(metadata), sizeof(metadata))
        self.md_buf[:] = md_buf[:]
        self.shm_buf[:] = image.tobytes()
        self.image_lock.release()

    # Destructor function to unlink and disconnect
    def close(self):
        self.image_lock.acquire()
        self.md_buf.close()

        try:
            unlink_shared_memory(self.md_name)
            unlink_shared_memory(self.shm_name)
        except ExistentialError:
            pass

        self.image_lock.release()
        self.image_lock.close()
