# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com
from machine import Pin, I2C, SPI
import utime

from mfrc522 import MFRC522

from rtc_sdCard import *
import uos
import ds3231




spi = SPI(0,baudrate=2500000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

spi.init()
rdr = MFRC522(spi=spi, gpioRst=21, gpioCs=22)

# Card reader
def read_card_info():
    r = ""
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            #print(f"uid: {card_id}")
            r = card_id 
    return r

MASTER_CARD_ID = "0x868ec425"#0x868ec425
card_db_file = "/sd/card_db.txt"



#Initialize MASTER_CARD_ID

def initialize_Master_card():
    global MASTER_CARD_ID
    r = read_card_info()
    while r=="":
        r = read_card_info()
    print("Master Initialize:")
    MASTER_CARD_ID = r
    add_card_db(r,r)
    utime.sleep(1)
    #print_db_file()
    return r




# Load card database UID,status
def load_card_db():
    cards = {}
    try:
        with open(card_db_file, "r") as f:
            # Skip the comment line
            f.readline()
            
            for line in f:
                card_id, status = line.strip().split(",")
                cards[card_id] = status
    except OSError:
        print("Error: Not able to access to card_db.")
    return cards


def print_db_file():
    try:
        with open(card_db_file,"r") as f:
            print("Log File Contents:")
            print(f.read()) # Read the entire contents
    except OSError:
        print( "Error: Unable to open or read the database file.")
        

#Functionalities:

# Modify Card Management Functions

## Save card on database
def save_card_db(cards):
    with open(card_db_file, "w") as f:
        # Description of the file
        datetime_stamp = current_time()
        f.write(f"## CARD_DATABASE {datetime_stamp}\n")
        for card_id, status in cards.items():
            f.write(f"{card_id},{status}\n")
        #print(f"{cards.items()}//\n")    


def clean_db():
    with open(card_db_file, "w") as f:
        f.write("")
    print("CLEAN")
## Add card to database
def add_card_db(card_id, auth_card_id):
    global MASTER_CARD_ID
    succesful = False
    
    if auth_card_id == MASTER_CARD_ID:
        if card_id == MASTER_CARD_ID:
            cards = load_card_db()
            cards[card_id] = "MASTER"
            save_card_db(cards)
            
        else:
            cards = load_card_db()
            #print(cards)
            cards[card_id] = "active"
            #print(cards)
            save_card_db(cards)
        succesful = True
    return succesful

## Remove card from database
def remove_card(card_id, auth_card_id):
    global MASTER_CARD_ID
    succesful = False
    if auth_card_id == MASTER_CARD_ID and card_id != auth_card_id:
        cards = load_card_db()
        #print("cards_before == ",cards)
        if card_id in cards:
            print(card_id in cards)
            del cards[card_id]
        #print("cards_after == ",cards, "\n")
            succesful = True
        save_card_db(cards)
        
    return succesful

## Block card from database
def block_card(card_id,auth_card_id):
    global MASTER_CARD_ID
    succesful = False
    if auth_card_id == MASTER_CARD_ID and card_id!=auth_card_id:
        cards = load_card_db()
        #print("cards_before == ",cards)
        if card_id in cards:
            print(card_id in cards)
            cards[card_id] = "bloked"
        #print("cards_after == ",cards, "\n")
            succesful = True
        save_card_db(cards)
        
    return succesful

## Check Status
def check_Status(card_id):
    cards = load_card_db()
    status = ""
    if card_id in cards:
        status = cards[card_id]
    return status
    

    
