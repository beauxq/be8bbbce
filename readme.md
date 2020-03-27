# Ben Eater's 8-bit Breadboard Computer Emulator
### (be8bbbce)

Ben Eater has a Youtube playlist building an 8-bit computer from scratch on breadboards.

https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU

I programmed an emulator for that computer.

It is a "simple-as-possible" architecture.

Run main.py (text) or visual.py (gui).

The gui uses the pygame python package that must be installed.
Note this bug with pygame: https://github.com/pygame/pygame/issues/201
Don't resize the window from the corner. Use the sides.


I programmed the emulator so that I could easily change the number of bits.
So then I made a 16-bit version with the exact same architecture.

Then I programmed software subroutines for multiplication, division, adding fractions,
and reducing fractions.
