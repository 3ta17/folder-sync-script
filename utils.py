import logging
import xxhash

def setup_logging(log_file):
    # Configure logging settings
    logging.basicConfig(filename=log_file, filemode="a", format="%(asctime)s - %(message)s", level=logging.INFO)
    console = logging.StreamHandler()
    logging.getLogger().addHandler(console)

def get_hash(f):
    # Compute file hash using xxHash
    h = xxhash.xxh64()
    try:
        with open(f, "rb") as file:
            while chunk := file.read(4096):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None
