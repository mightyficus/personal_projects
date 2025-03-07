# North America

## Tutorial (10 pts)
## New Orleans (10 pts)
`447e: <create_password>` creates the same static password at address `0x2400` every time it runs
`44b2: <get_password>` gets a password from the user and stores it at address `0x439b`
`44bc: <check_password>` checks the entered password stored in memory to the actual byte by byte
Solution: - Not the same thing every time. First, run the program up to the `<get_password>` function. When it asks for input, press wait, and look at the value in `0x2400`

## Vancouver (10 pts)
`443e: <main>`
* sets `r13` to 0x400
* clears `r14`
* sets `r15` to 0x2400
* calls `<memset>`
* sets `r14` to 0x3ff
* sets `r15` to 0x2400 again
* gets the debug payload from the user and stores it at 0x2400
* effectively stores first two bytes of payload in `r11`
	* gets whatever the first byte of the payload is, stores it in `r11`, and swaps the high order byte with the low order byte (0x0074 -> 0x7400)
	* takes the second byte of the payload and stores it in `r15`
	* ORs together `r11` and `r15` and stores it in `r11`
* if 3rd byte of payload is < 2, the payload is invalid. Otherwise, it executes
	* stores 3rd byte of payload and stores it in `r10`
	* if `r10` - 0x2 < 0, jump to `0x4486`
* store 3rd byte of payload (`r10`) in `r13`
* store address of 4th byte of payload in `r14`
* store first 2 bytes of payload in `r15`
* call `<memcpy>`
* Finally, call the program at address in `r11` (First 2 bytes of payload)
`450e: <memset>` Not positive yet what this does
`44fc: <memcpy>`
* `r12` - byte 1+2, payload start address
* `r13` - byte 3, program length
* `r14` - byte 4, first byte of program
* Assembly logic:
	* store the 2 bytes of payload in `r15` in `r12`
	* jump to `0x4508`
	* if value in `r13` is not 0, go to `0x4500`
	* move the next byte of the payload into the address in `r12`, then increment `r12` and `r14`
	* decrement `r13`
PoC: Replace first .string with HELLO, WORLD!: `45 7a 0d 48 45 4c 4c 4f 2c 20 57 4f 52 4c 44 21`

We know that it inserts the code into whatever part of memory it's told and runs it, so we just need to write instructions that open the lock. In the manual, we can see several interrupts, including `0x7f`, which interfaces with the deadbolt to trigger an unlock. We can use the [disassembler/assembler](https://microcorruption.com/assembler) on the website to see that this code to send an unlock interrupt:
```
push #0x7f
call #0x44a8
```
Translates to this: `30127f00b012a844`
If we add that on to an acceptable "header" (two byte address+length), we get this: `80003030127f00b012a844`, which unlocks the door.

## Cold Lake


## Halifax


# Asia

## Baku
* User input is saved at `0x43f0`
* `46fa <aes_ecb_decrypt>` is so convoluted that I don't think it's worth deciphering yet, but it basically scrambles the input string
* `47ee <memcmp>` seems to be doing the validation
	* It sets `r15` to a pointer to "ACCESS GRANTED!" @ `488f`
	* `r14` is already set to a pointer to the scrambled user input @ `43f0`
	* it loads the first letter of each into `r11` and `r12` respectively and increments the pointers
	* It compares them
		* if they're equal, it loops until the entire string matches, and `r15` is cleared and the function returns
		* if it doesn't, it puts the mismatched input character into `r14` and the known good character into `r15`, Then it does `r15 - r14` and stores the result in `r15`, and finally returns
# Australia

## Sydney