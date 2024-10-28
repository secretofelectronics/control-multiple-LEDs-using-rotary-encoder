from machine import Pin, I2C
import ssd1306
import time

time.sleep(0.5)
# Define GPIO pins for the LEDs and Rotary Encoder
led_pins = [Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT)]

# Rotary Encoder pins
clk = Pin(16, Pin.IN, Pin.PULL_UP)
dt = Pin(17, Pin.IN, Pin.PULL_UP)
sw = Pin(18, Pin.IN, Pin.PULL_UP)

# Set up I2C and OLED display
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # Update GPIO pins for I2C as needed
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # 128x64 display resolution

# Variables to store the state
current_led = 0              # Index of the currently selected LED (0 to 4)
last_clk = clk.value()       # Last state of the CLK pin
rotation_steps = 0           # Count of encoder steps
steps_per_led_change = 3     # Number of steps required to change the LED
toggle_states = [False] * 5  # Track on/off state of each LED

# Function to update OLED display with selected LED and its state
def update_display():
    oled.fill(0)  # Clear the display
    oled.text(f"Selected LED: {current_led + 1}", 0, 0)
    oled.text(f"State: {'ON' if toggle_states[current_led] else 'OFF'}", 0, 20)
    oled.show()

# Function to update LED selection based on rotary encoder rotation
def update_led_selection():
    global current_led, last_clk, rotation_steps
    
    clk_value = clk.value()
    if clk_value != last_clk:  # Rotation detected
        if dt.value() != clk_value:
            rotation_steps += 1  # Forward rotation
        else:
            rotation_steps -= 1  # Backward rotation
        
        # Change the LED selection only after the specified number of steps
        if abs(rotation_steps) >= steps_per_led_change:
            if rotation_steps > 0:
                current_led = (current_led + 1) % 5  # Move forward
            else:
                current_led = (current_led - 1) % 5  # Move backward
            
            rotation_steps = 0  # Reset step counter after LED change
            update_display()  # Update OLED display with the new selection

    last_clk = clk_value

# Function to toggle the selected LED on button press
def toggle_led():
    toggle_states[current_led] = not toggle_states[current_led]
    led_pins[current_led].value(toggle_states[current_led])  # Set the LED to the new state
    update_display()  # Update OLED display with the new state

# Main loop
update_display()  # Initial display update
while True:
    update_led_selection()
    
    # Check if the rotary encoder button is pressed
    if not sw.value():  # Active low button press
        toggle_led()
        time.sleep(0.3)  # Debounce delay for button press
    time.sleep(0.01)  # Small delay for smooth operation