from rfid_lector import *
from LCD import *
from keypad_4x4 import *
#from PIR_Sensor_Buzzer import *

import utime, machine


initialized = False	
masterId = ""#0x868ec425

passwrd = "12345"
message = ""
last_state = ""
systemStatus = "disarmed"
cardId = ""
interruption_enabled = False


spi = SPI(0,baudrate=2500000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

spi.init()
rdr = MFRC522(spi=spi, gpioRst=21, gpioCs=22)


def system_off():
    key = ""
    message = text("System Sleep")
    log_activity("###System Off###")
    utime.sleep(2)
    message = text("")
    start_time = utime.time()
    while key != "P":
        key = scan_keypad()
        utime.sleep(0.1)
        if utime.time() - start_time >5:
            start_time = utime.time()
            message = text("")
    log_activity("###System On###")
    message = text("System Up")
    utime.sleep(0.5)

def password_card_check(message_0):
    global systemStatus
    pswd_ = ""
    key = ""
    card_placed = ""
    message_1 = message_0
    print("Set Password or Place a Card")
    while (key != "ENT" or card_placed == "") and systemStatus=="armed":
        key = scan_keypad_passwrd()
        card_placed = read_card_info()
        
        if key != "":
            if key == "ENT":
                break
            elif key == "S":
                print("Key Value:", pswd_)
                pswd_ = pswd_[:-1]
            elif key == "ESC":
                pswd_ = ""
                print("Key Value:", pswd_)
            else:
                pswd_ = pswd_ + key
                print("Key Value:", pswd_)
        if card_placed != "":
            print("Card Placed")
            status = check_Status(card_placed)
            if status == "":
                log_activity(f"not registered log! Tried with: {card_placed}")
                message = text("Not Registered")
                utime.sleep(0.5)
                message = text(message_0)
                card_placed == ""
            elif status == "bloked":
                log_activity(f"Blocked log! Tried with: {card_placed}")
                message = text("Blocked")
                utime.sleep(0.5)
                message = text(message_0)
                card_placed == ""
            else:
                message = text("Active")
                log_activity(f"Active card detected Tried with: {card_placed}")
                utime.sleep(0.5)
                systemStatus = "disarmed"
                break
                
    return pswd_





def card_manager_assistant(master):
    
    log_activity("##Card Manager Assistant##")
    message = text("1:ADD 2:BLK     3:DLT 4:RG")
    start_time = utime.time()
    while utime.time() - start_time < 30:
        key = scan_keypad()
        while key == None:
            pass
        if key == "1":
            message = text("Place Card ADD")
            card_placed = read_card_info()
            while card_placed == "":
                card_placed = read_card_info()
            log_activity(f"Card Placed: {card_placed}")
            sucessful = add_card_db(card_placed,master)
            if sucessful:
                log_activity(f"Sucessful: uid: {card_placed} was Added")
                message = text("Sucessful")
                utime.sleep(1)
                
            else:
                log_activity(f"Authory Error, was not possible to add uid: {card_placed}")
                message = text("Authory Error")
                utime.sleep(1)
            break
        
        elif key == "2":
            message = text("Place Card Blk")
            card_placed = read_card_info()
            while card_placed == "":
                card_placed = read_card_info()
            log_activity(f"Card Placed: {card_placed}")
            sucessful = block_card(card_placed,master) 
            if sucessful:
                log_activity(f"Sucessful: uid: {card_placed} was Blocked")
                message = text("Sucessful")
                utime.sleep(1)
                
            else:
                log_activity(f"Unexpected Card Error, was not possible to block uid: {card_placed}")
                message = text("Unexpected_Card_Error")
                utime.sleep(1)
            break
                
        elif key == "3":
            message = text("Place Card Del")
            card_placed = read_card_info()
            while card_placed == "":
                card_placed = read_card_info()
            log_activity(f"Card Placed: {card_placed}")
            sucessful = remove_card(card_placed,master)
            
            if sucessful:
                log_activity(f"Sucessful: uid: {card_placed} was Deleted")
                message = text("Sucessful")
                utime.sleep(1)
                
            else:
                log_activity(f"Unexpected Card Error, was not possible to delete uid: {card_placed}")
                message = text("Unexpected_Card_Error")
                utime.sleep(1)
            break
        elif key == "4":
            log_activity("#Request Push DataBase#")
            message = text("Push DB Terminal")
            print_db_file()
            utime.sleep(3)
            break
    return ""


##PIR_Sensor_Buzzer modified

sensor_pin = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer_pin = machine.Pin(18,machine.Pin.OUT)



def buzzer_interrupt_pswd(pin):
    global last_state
    global message
    global sensor_pin
    global systemStatus
    log_activity(f"30 seconds to call the Police")
    message = text("30sec Police")

    key = ""
    card_placed = ""
    pswd_ = ""
    if pin == sensor_pin:
        if pin.value()==1:
            disable_interrupt()
            sensor_pin.off()
            print("Motion Detection!")
            message_0 = text("Place Card!")
            
            start_time = utime.time()
            while (utime.time() - start_time  < 30) and systemStatus=="armed":
                play_tone(1175, 300)
                
                card_placed = read_card_info()
                if card_placed != "":
                    status = check_Status(card_placed)
                    if status == "":
                        log_activity(f"@@@not registered log! Tried with: {card_placed}")
                        message = text("Not Register")
                        card_placed = ""
                        utime.sleep(0.1)
                        message = text(message_0)

                    elif status == "bloked":
                        log_activity(f"@@@Blocked log! Tried with: {card_placed}")
                        message = text("Blocked")
                        card_placed = ""
                        utime.sleep(0.1)
                        message = text(message_0)
                    else:
                        systemStatus = "disarmed"
                        last_state = "buzzer"
                        log_activity(f"@@@Active card detected Tried with: {card_placed}")
                        message = text("Active")
                        card_placed = ""
                        
                        utime.sleep(0.1)
                        break

            if systemStatus == "armed":
                log_activity(f"Time out! Calling Emergencies!!!")
                message = text("Calling Police")
                while True:
                    play_tone(800, 400)

def play_tone(frequency, single_duration): #funtion to define the tone to play
    # Calculate the period of the tone in microseconds
    period = 1000000 // frequency 
    # Calculate half the period for on/off times
    half_period = period // 2

     # Loop for the duration, toggling the buzzer pin to generate the tone
    end_time = utime.ticks_ms() + single_duration
    while utime.ticks_ms() < end_time:
        buzzer_pin.value(1)  # Set pin high (turn buzzer on)
        utime.sleep_us(half_period)  # Wait for half the period
        buzzer_pin.value(0)  # Set pin low (turn buzzer off)
        utime.sleep_us(half_period)  # Wait for half the period

def disable_interrupt(): 
    global interruption_enabled
    global sensor_pin
    #sensor_pin.off()
    if interruption_enabled:
        sensor_pin.irq(handler=None)
        interruption_enabled = False
    return interruption_enabled

def enable_interruption():
    global interruption_enabled
    global sensor_pin
    #sensor_pin.off()
    if not interruption_enabled:
        sensor_pin = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_DOWN)
        sensor_pin.irq(trigger=machine.Pin.IRQ_RISING , handler=buzzer_interrupt_pswd)
        #sensor_pin.value(0)
        interruption_enabled = True
    return interruption_enabled




if not initialized:
    clean_db()
    disable_interrupt()
    power_up = False
#elif(masterId!=""):
#    masterId=initialize_Master_card(initialized)
while not initialized: 
    
    power = scan_keypad()
    
    if power =="P":
        power_up = True
        clear_log_file()#Initialize the system making sure there is no entries from a different session
        
        # Boot Case
        log_activity("###System Initialization###")
        message = text("System Init")
        utime.sleep(1)
        print("Define the master card")
        message = text("Define Master")
        
        #masterId=initialize_Master_card(initialized)##
        masterId=initialize_Master_card()##
        message = text("Master Defined")
        log_activity(f"Master Defined: {masterId}")
        utime.sleep(0.2)
        
        print("Define password")
        message = text("Password")
        passwrd = define_pass()
        message = text("Pswd Defined")
        log_activity(f"Pswd Defined: {passwrd}")
        print(f"Password Defined: {passwrd}")
        utime.sleep(0.2)
        initialized = True
        log_activity("###System booted up###")
        last_state = "bootUp"
        systemStatus = "disarmed"
        print_log_file()
        
while True: 
        
    if systemStatus == "disarmed":
        disable_interrupt()
        tries = 3
        if last_state!=systemStatus: #Only appear when change of state
            log_activity("##System Disarmed##")
            message = text("System Disarmed")
            last_state = systemStatus

            utime.sleep(1)
            
        message = text("1:CardM 2:armSy 3:LR P:Slp ")
        key = scan_keypad()
        while key == "":
            key = scan_keypad()
        print(key)
        if key == "P":
            system_off() ## here!
        elif key == "1":
            message = text("Place MasterId")
            card = read_card_info()
            while card == "":
                card = read_card_info()
            if card == masterId:
                #print("GOOD")
                card_manager_assistant(card) 
               
                

            else:
                log_activity(f"#Incorrect MasterId for ManageAssitantCard: Tried with {card}")
                message = text("Incorrect ID")
                utime.sleep(1)


        elif key == "2":
                    systemStatus = "armed"
                    
        elif key == "3":
                log_activity("#Creating backup#")
                create_backup()
                log_activity("#backup Finished. Pushing Log File#")
                print_log_file()
                message = text("Push LogFile   Terminal")
                utime.sleep(3)

    elif systemStatus == "armed": 
            enable_interruption() 
            if last_state!=systemStatus:
                log_activity("##System Armed##")
                message = text("System Armed")
                utime.sleep(1)
                last_state = systemStatus

            message = text("Password:")
            message_0 = message
            pswd_ = password_card_check(message_0)
            
                
            if systemStatus == "armed":
                if pswd_ == passwrd:
                    systemStatus = "disarmed"
                else:
                    tries = tries - 1
                    if tries > 0:
                        log_activity(f"Wrong Password! password: {pswd_} {tries} attempts remaining")
                        message = text("Wrong Passwd")
                        utime.sleep(1)
                        message = text(message_0)
                        pswd_ = ""
                    else:
                        log_activity(f"Wrong Password! password: {pswd_} {tries} attempts remaining")
                        buzzer_interrupt_pswd(sensor_pin)





