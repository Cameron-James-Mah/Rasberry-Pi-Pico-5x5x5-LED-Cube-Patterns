# Rasberry-Pi-Pico-5x5x5-LED-Cube-Patterns
These are patterns for a 5x5x5 LED cube I made with my dad. The LED's are controlled using a method called multiplexing which I will explain its use further in wiring section. The programming was done using micropython.

# Components used(This will vary depending on size of cube, microcontroller, etc):
- Copper wire(For forming the frame and connecting columns and layers)
- 125 LED's(Will obviously depend on the size of the cube)
- 125 resistors(Don't want to burn out LED's)
- 5 transistors(toggle a layers connection to ground, will elaborate further in wiring section)
- 2 shift registers(Need extra GPIO pins)

# Building the cube


# Wiring
To understand the wiring you have to understand basic circuits. I personally had very little knowledge about circuits before doing this project but there isn't much you need to know for this. The first thing to understand is that for an LED to light up it needs to be part of a complete circuit. In other words the LED would need to recieve voltage(not too much and not too little) through its anode(longer lead) and exit through its cathode(shorter lead) and reach ground.

Using this knowledge, the most intuitive thing might be to hook up each LED individually and manipulate them. However it would take much more time, compoenents and would look worse. Instead we can use a method called multiplexing. I don't think I can give an adequate summary of what multiplexing is in general and any explanation found online will be much better. However in this project we can use multiplexing to control each LED without connecting them individually. Imagine in our 5x5x5 cube we have columns of copper wire that connect a column of LED's via there anode. Imagine that all layers of LED's are also connected to each other via their cathode. Now all we would need is for each column of copper wire to be powered via a GPIO pin in our rasberry pi and each layer to be connected to ground pins in our rasberry pi and we would now have a fully lit up cube. Every single LED would be part of a complete circuit from the rasberry pi, through all copper columns, through all LED anodes, out all LED cathodes, to the copper layer, back to ground via a rasberry pi ground pin. Once this is understood you can manipulate a column's power and layers connection to ground to turn on specific LED's




# Troubleshooting

#Conclusion



