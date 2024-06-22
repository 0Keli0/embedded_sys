import machine
import utime

keypad_rows = [machine.Pin(pin, machine.Pin.OUT) for pin in (9,8,7,6)]
keypad_cols = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN) for pin in (1,13,4,5)]

keypad_matrix = [
    ['1','2','3','S'],
    ['4', '5', '6','GO'],
    ['7', '8', '9','L'],
    ['ENT', '0', 'ESC','P'],
]


keypad_matrix_define_pass = [
    ['1','2','3','S'],
    ['4', '5', '6',''],
    ['7', '8', '9',''],
    ['ENT', '0', 'ESC',''],
]

keypad_matrix_disarmed = [
    ['1','2','3','S'],
    ['4', '5', '6','GO'],
    ['7', '8', '9','L'],
    ['', '0', '','P'],
]

     
        


# Function to scan the keypad buttons
def scan_keypad():
    for row_num, row_pin in enumerate(keypad_rows):
        row_pin.value(1)
        for col_num, col_pin in enumerate(keypad_cols):
            if col_pin.value() == 1:
                while True: #don't go next till stop pressing the button
                    if col_pin.value() != 1:
                        break  
                return keypad_matrix[row_num][col_num]
        row_pin.value(0)
    return ""

#Scan using the keypad_passwrd
def scan_keypad_passwrd():
    for row_num, row_pin in enumerate(keypad_rows):
        row_pin.value(1)
        for col_num, col_pin in enumerate(keypad_cols):
            if col_pin.value() == 1:
                while True: #don't go next till stop pressing the button
                    if col_pin.value() != 1:
                        break  
                return keypad_matrix_define_pass[row_num][col_num]
        row_pin.value(0)
    return ""

# Function to define the password
def define_pass():
    recording = True
    passwrd = ""
    print("Set Password:")
    while recording:
        digit = scan_keypad_passwrd()
        if digit != "":
            if digit == "ENT":
                print("Comparing Passwords")
                recording = False
            elif digit == "S":
                passwrd = passwrd[:-1]
                print("Key Value:", passwrd)
            elif digit == "ESC":
                password = ""
                print("Key Value:", passwrd)
            else:
                passwrd = passwrd+ digit
                print("Key Value:", passwrd)
            
    return passwrd   