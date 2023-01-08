# Rasberry-Pi-Pico-5x5x5-LED-Cube-Patterns
These are patterns for a 5x5x5 LED cube I made with my dad. The LED's are controlled using a method called multiplexing which I will explain its use further in wiring section. The programming was done using micropython.

# Components/Equipment used(This will vary depending on size of cube, microcontroller, etc):
- Copper wire(For forming the frame and connecting columns and layers)
- 125 LED's(Will obviously depend on the size of the cube)
- 125 resistors(Don't want to burn out LED's)
- 5 NPN transistors(toggle a layers connection to ground, will elaborate further in wiring section)
- 2 shift registers(Need extra GPIO pins)
- Soler, Soldering iron(Solder LED leads, copper wire, etc)
- Other tools depending on how you want to build your cube frame

# Building the cube


# Wiring
To understand the wiring you have to understand basic circuits. I personally had very little knowledge about circuits before doing this project but there isn't much you need to know for this. The first thing to understand is that for an LED to light up it needs to be part of a complete circuit. In other words the LED would need to recieve voltage(not too much and not too little) through its anode(longer lead) and exit through its cathode(shorter lead) and reach ground.

Using this knowledge, the most intuitive thing might be to hook up each LED individually and manipulate them. However it would take much more time, compoenents and would look worse. Instead we can use a method called multiplexing. I don't think I can give an adequate summary of what multiplexing is in general and any explanation found online will be much better. However in this project we can use multiplexing to control each LED without connecting them individually. Imagine in our 5x5x5 cube we have columns of copper wire that connect a column of LED's via there anode. Imagine that all layers of LED's are also connected to each other via their cathode. Now all we would need is for each column of copper wire to be powered via a GPIO pin in our rasberry pi and each layer to be connected to ground pins in our rasberry pi and we would now have a fully lit up cube. Every single LED would be part of a complete circuit from the rasberry pi, through all copper columns, through all LED anodes, out all LED cathodes, to the copper layer, back to ground via a rasberry pi ground pin. Once this is understood you can manipulate a column's power and layers connection to ground to turn on specific LED's. For example if I had a 5x5x5 cube and I give voltage to only one column and only have my top layer connected to ground, then only the LED on the top layer of that column would light up. Every LED in that column would be recieving voltage, however only the LED in the top layer of that column would be connected to ground and therefore part of a complete circuit. Similarily other LED's on the top layer will be connected to ground but not recieve voltage so will not be part of a complete circuit either. Using this knowledge we can then control which LED's we light up.

Once everything up to here is understood, the next logical thing to think is then how do you toggle giving voltage to columns and toggle connecting a layer to ground. You can toggle a columns voltage by connecting them to one of your your rasberry pi's GPIO pins and turning on the output for that pin via programming. To toggle your connection to ground you can use NPN transistors. Transistors can be used as a switch or an amplifier, in this case we use it as a switch. To put it simply when we put the transistor between a layers connection to ground, if the transistor is not recieving voltage then it acts as an open switch meaning it does not complete that layers connection to ground. If the transistor is recieving enough voltage, the transistor acts like a closed switch completing the layer's connection to ground. So if for every layer we put a transistor between its connection to ground, then we can connect a GPIO pin to that transistor and toggle its connection by either giving it power(connecting it to ground) or not giving it power(no longer connected to ground). 

It is important to note that atleast on the rasberry pi pico, you only have 26 GPIO pins. So if you plan to do a 5x5x5 that means 25 GPIO pins for each column. But you will still need 5 more for the transistors. In a case like this where you need more GPIO pins, we need to use shift registers. I think shift registers can very and may have different specs, the one I used was() and it takes 3 inputs(GPIO pins) but gives us 8 outputs giving us a total of 5 extra outputs per shift register. If you are using a rasberry pi aswell, this video is perfect for you: https://www.youtube.com/watch?v=-lEtgzlNSnA. This video explains what shift registers are, how to use them, and gives a code example.


#Programming



# Troubleshooting

# Conclusion



