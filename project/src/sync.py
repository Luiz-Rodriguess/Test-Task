import os
import shutil
from filecmp import dircmp
import time
import sys
from logger import Logger
import re
import signal

running = True

# Signal handler to shutdown the bprogram when SIGTERM is received
def handle_sigterm(signum, frame):
    global running
    print(f"Received SIGTERM (signal {signum}), shutting down program")
    running = False

# Register signal handler
signal.signal(signal.SIGTERM, handle_sigterm)

def sync_folders(source, replica) -> Logger:
    logger = Logger() # Initialize the logger object to track changes

    # Check if the source directory exists, raise an error if not
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source folder {source} not found.\nStopping Execution")
    
    # Check if the replica directory exists
    if not os.path.exists(replica):
        # Since it's not specified we can either stop the program or create a new replica folder
        raise FileNotFoundError(f"Replica folder {replica} not found.\nStopping Execution")
        # os.makedirs(replica)

    sync_directories(source, replica, logger)

    return logger

def sync_directories(source, replica,logger : Logger):
    
    # Compare the contents of source and replica directories
    comparison = dircmp(source, replica)
    
    # Handle files and directories that are only present in the source (new files)
    for item in comparison.left_only:
        source_path = os.path.join(source, item)
        replica_path = os.path.join(replica, item)
        if os.path.isdir(source_path):
            logger.addCreated(f"Created new directory {item}")
            shutil.copytree(source_path, replica_path)
        else:
            logger.addCreated(f"Created new file {item}")
            shutil.copy2(source_path, replica_path)
    
    # Handle files and directories that are only present in the replica (deleted in source)
    for item in comparison.right_only:
        replica_path = os.path.join(replica, item)
        if os.path.isdir(replica_path):
            logger.addDeleted(f"Deleted directory {item}")
            shutil.rmtree(replica_path)
        else:
            logger.addDeleted(f"Deleted File {item}")
            os.remove(replica_path)

    # Handle files that exist in both but differ in content (modified files)
    for item in comparison.diff_files:
        source_path = os.path.join(source, item)
        replica_path = os.path.join(replica, item)
        logger.addChanged(f"Changed file {item}")
        shutil.copy2(source_path, replica_path)
    
    # Recursive call to syncronize the contents of the subdirectories contained in source
    for common_dir in comparison.common_dirs:
        sync_directories(os.path.join(source, common_dir), os.path.join(replica, common_dir),logger)

def main(argv):
    global running
    source_dir = argv[1]  # Get the source directory from command line arguments
    replica_dir = argv[2]  # Get the replica directory from command line arguments
    
    # Validate and extract the time between syncronizations (in seconds)
    if re.match(r'\d+',argv[3]):
        timeout = eval(argv[3])
    else:
        print("Timeout should be a number","Stopping Execution")
        return
    
    log_filepath = argv[4]  # Get the log file path from command line arguments
    
    print("Starting program...")
    # Main program loop, runs until interrupted or SIGTERM is received
    while running:
        try :
            logger = sync_folders(source_dir, replica_dir)
            time.sleep(timeout)
            print(logger.simpleLog())
            with open(log_filepath,"a") as log_file:
                log_file.write(logger.detailedLog())
        except FileNotFoundError as e:
            # Handle missing source/replica directories and stop execution
            running = False
            print(e)
        except KeyboardInterrupt as e:
            # Handle keyboard interruption by the user (Ctrl+C)
            running = False
            print("Program interrupted by user")

if __name__ == "__main__":
    # Validate that exactly 4 arguments are provided (source, replica, timeout, log file)
    if len(sys.argv) < 5 :
        print("Missing arguments")
    elif len(sys.argv) > 5 :
        print("Too many arguments")
    else :
        main(sys.argv)