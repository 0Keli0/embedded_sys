from machine import Pin, I2C, SPI
from sdcard import SDCard # module to handle SD card operations
import uos  #module for file system operations
import utime
import ds3231 #to interact with the RTC

#initialize I2C for RTC
i2c = I2C(1, scl=Pin(27), sda=Pin(26)) 
rtc = ds3231.DS3231(i2c)

#Initialize SPI for sd Card using GP10-GP15
spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))# Create an SPI object with SCK on GP10, MOSI on GP11, and MISO on GP12
cs = Pin(15, Pin.OUT) # Set GP15 as the chip select pin for the SD card
sd = SDCard(spi, cs)  # Create an SDCard object using the SPI and chip select pin

# Mount SD Card

uos.mount(sd, "/sd") # Mount the SD card to the /sd directory


# Function for the timestamps
## Function hour:minute
def get_Time():
    current_time = rtc.datetime()
    hour = current_time[4];minute = current_time[5]
    time_str = "{:02d}:{:02d}".format(hour,minute)
    return time_str

## Function current time for log texts
def current_time():
    #Get the current timestamp from the RTC
    timestamp = rtc.datetime()
    #Format the timestamp into a readable string
    formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        timestamp[0], timestamp[1], timestamp[2], 
        timestamp[4], timestamp[5], timestamp[6]
    )
    return formatted_time
# Function to log activity
def log_activity(message):
    # Get the current time formatted
    formatted_time = current_time()
    # Create a log message with the timestamp and provided message
    log_message = "[{}] {}\n".format(formatted_time, message)
    
    # Open the log file on the SD card in append mode
    try:
        with open("/sd/log.txt", "a") as f:
            f.write(log_message) # Write the log message to the file
        print(log_message) # Print the log message to the console
    except OSError:
        print( "Error: Unable to write in the log file.")
 
# Function to print the contesnts of the log file
def print_log_file():
    try:
        with open("/sd/log.txt","r") as f:
            print("Log File Contents:")
            print(f.read()) # Read the entire contents
    except OSError:
        print( "Error: Unable to open or read the log file.")
        

# Funciton to delete the contents of the log file
def clear_log_file():
    try:
        with open("/sd/log.txt", "w") as f: # Open the file in w mode to clear its contents
            f.write("") #clear the content
        print("Log file cleared successfully.")
    except OSError:
        print("Error: Unable to clear the log file.")
        
        
# Function to create a backup of the log file
def create_backup():
    try:
        with open("/sd/log.txt", "r") as f:
            log_content = f.read() # Read the contents
        
        # Get current date and time from RTC
        rtc_time = rtc.datetime()
        rtc_timestamp = "{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}".format(
            rtc_time[0], rtc_time[1], rtc_time[2],
            rtc_time[4], rtc_time[5], rtc_time[6])
        
        # Create a unique backup file name using RTC timestamp
        backup_file_name = "/sd/backup/log_backup_{}.txt".format(rtc_timestamp)
            
        with open(backup_file_name, "a") as backup_file:
            backup_file.write(log_content)    
        print("Log file backed up successfully to:", backup_file_name)
    except OSError:
        print("Error: Unable to create backup of the log file.")













#print_log_file()    
#log_activity("System initialized")  # Log system initialization
#utime.sleep(2)  # Wait for 2 seconds
#log_activity("Performing task A")  # Log task A
#utime.sleep(2)  
#log_activity("Performing task B")  # Log task B
#utime.sleep(2)  
#log_activity("System shutting down")  # Log system shutdown

#utime.sleep(2)  # Wait for 2 seconds
#print_log_file()
#utime.sleep(2)  # Wait for 2 seconds

#clear_log_file()