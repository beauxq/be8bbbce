# Ben Eater's 8-bit Breadboard Computer Emulator  
### (be8bbbce)
--------------

![Tests](https://github.com/beauxq/be8bbbce/actions/workflows/tests.yml/badge.svg)

---

Ben Eater has a Youtube playlist building an 8-bit computer from scratch on breadboards.

https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU

I programmed an emulator for that computer.

It is a "simple-as-possible" architecture.

Run `main.py` (text) or `visual.py` (gui).

The gui uses the pygame python package.  
Note this bug with resizing the window in pygame: https://github.com/pygame/pygame/issues/201  
Don't resize the window from the corner. Use the sides.


### instruction set expansion
-----------------------------

I added a few instructions to the instruction set just by implementing new microcode.

 - `JI  = 0x9`  jump indirect
 - `LIN = 0xa`  load indirect
 - `SIN = 0xb`  store indirect

The parameters to these are pointers to the values that would be the parameters to, respectively, `JMP`, `LDA`, and `STA`.


### Note G:
-----------

I programmed the emulator so that I could configure the width of the bus.
So I could easily make a 16-bit version with the exact same architecture.

Then I programmed software subroutines for multiplication, division, adding fractions,
and reducing fractions.

Using these subroutines, I then programmed Ada Lovelace's Note G
Bernoulli Number calculator. (Bernoulli numbers are not integers,
but they are rational numbers.)

The program will output the numerator and then the denominator.
If you're only looking at the visualization ( `visualbernoulli.py` ),
you'll probably only see the denominator, unless you slow it
down at the right time.
You can see all the output in the console log.

Resetting the computer after it halts (not clearing the memory) will calculate the
next Bernoulli number after the last one it calculated. This might be how Ada Lovelace
planned to use this program - let the machine run to calculate one Bernoulli
number, then record that one, then start the machine again to calculate the next one.

The 16-bit computer can calculate B14, but runs into overflow when calculating B16.
The 32-bit computer can calculate B16 and beyond, but then it quickly runs into
performance issues. (It's not a very efficient algorithm, along with doing all the
multiplication by repeating adding.)
