from machine import Pin, I2C
import ssd1306
import time

time.sleep(0.5)  # Small startup delay

# Define GPIO pins for the LEDs
led_pins = [Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT)]

# Rotary Encoder pins
clk = Pin(16, Pin.IN, Pin.PULL_UP)
dt = Pin(17, Pin.IN, Pin.PULL_UP)
sw = Pin(18, Pin.IN, Pin.PULL_UP)

# Set up I2C and OLED display
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # 128x64 OLED

# Variables to store the state
current_led = 0              # Index of the selected LED
toggle_states = [False] * 5  # LED states (all OFF initially)

# Function to update OLED display
def update_display():
    oled.fill(0)  # Clear display
    oled.text(f"Selected LED: {current_led + 1}", 0, 0)
    oled.text(f"State: {'ON' if toggle_states[current_led] else 'OFF'}", 0, 20)
    oled.show()

# Function to handle rotary encoder movement
def rotary_callback(pin):
    global current_led

    time.sleep_ms(2)  # Small debounce delay
    if clk.value() == dt.value():
        current_led = (current_led + 1) % 5  # Clockwise rotation
    else:
        current_led = (current_led - 1) % 5  # Counterclockwise rotation

    update_display()

# Attach interrupt to CLK pin (triggers on falling edge)
clk.irq(trigger=Pin.IRQ_FALLING, handler=rotary_callback)

# Function to toggle LED on button press
def toggle_led():
    toggle_states[current_led] = not toggle_states[current_led]
    led_pins[current_led].value(toggle_states[current_led])  # Toggle LED state
    update_display()

# Main loop
update_display()  # Initial display update

while True:
    # Check if the rotary encoder button is pressed (Active Low)
    if not sw.value():
        toggle_led()
        time.sleep(0.3)  # Debounce delay
        while not sw.value():  # Wait until the button is released
            pass
    
    time.sleep(0.01)  # Small delay for stability
