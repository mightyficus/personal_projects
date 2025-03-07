# How it Works

tl;dr: Given a debugger and a device, find an input that unlocks it. Solve the level with that input.

You've been given access to a device that controls a lock. Your job: defeat the lock by exploiting bugs in the device's code.

You're playing "Capture The Flag". You collect points for each level you beat, working your way through steadily more complicated vulnerabilities. Most levels showcase a single kind of real-world software flaw; some levels chain a series of them together.

This device has a simple input: you provide a passcode, and if the passcode is correct, the lock unlocks. Just one problem: you don't know the passcode. Unlock it anyways.

We've done the tedious work for you: we got the device working, hooked a rudimentary debugger up to it, dumped the code for each level and disassembled it for you.

You'll use the debugger to reverse-engineer the code for each level. You can provide the device with input, then step through the code watching what the device does what that input. You're looking for a specific input that unlocks the device. Maybe that input is the correct passcode. More likely, though, it's something else: an input that exploits a bug in the device's code.

# Notes on the Interface

## Disassembly
Shows the code in Assembly for the authentication program. It's a "Lockitall LockIT" mock-MSP430 device, which runs a RISC architecture. \<INT> function represents an interrupt (puts characters, request input, etc), and calls the interrupt of the value most recently pushed to the stack

## Register State
Shows the value in each register. `pc` is the program counter register, `sp` is the stack pointer register, `sr` is the state register, `cg` is the constant generator register (still not sure what this one does), and `r4 - r15` are general registers. 
Hovering over the `sr` register will tell you what flags are currently raised. Hovering over a general register will translate the hex into decimal.

## Current Instruction
Obvious. How many cpu cycles have passed, current instruction in bytes, and current instruction in assembly code.

## Live Memory Dump
Also obvious. Rows of 16 bytes, ASCII translation on the side.

## I/O Console
Any program Input/Output will show up here. When the program requests input, a window will pop up allowing for input. you can check a box to enter input as raw hexcode. Any input request will immediately set a breakpoint.
## Debugger Console
Minimalist low-level debugger. Help will print all available commands. Most useful are:
* `help`
* `s/step` - step forward one instruction
* `f/out` - step out of function
* `break <address/label>` - set a breakpoint, you can also click on the instruction to set a breakpoint there
* `unbreak <address/label` - unset a breakpoint
* `c/continue` - resume execution until next break/end of program
* `let <register/addr>=<expression>` - set the value of a register or address
* `manual` - show the manual for this page


# MSP430 Assembly

## Instructions
Instructions take the form `opcode source, destination`, where source and destination refer to registers, constants, or memory locations

Instructions can operate on the following:
* Registers
* Program Counter (special register that identifies address of next instruction)
* Stack Pointer (special register that identifies a part of memory that is carved out for memory)
* Memory
* CPU flags (`sr` register, records flags)

There are technically only 2 types of instructions: arithmetic (compute values and store results) and Control transfer (decide next instruction)

Addressing modes:

| Mode                   | Syntax       | Description                                                                    |
| ---------------------- | ------------ | ------------------------------------------------------------------------------ |
| Register               | Rx           | Reference value stored in register directly                                    |
| Index                  | X(Rx)        | Reference value stored in memory at X + value in register                      |
| Symbolic               | c            | Reference value stored in memory at offset PC + c                              |
| Absolute               | &ADDR        | Reference value stored at ADDR                                                 |
| Indirect               | @Rx          | Reference value in memory stored at the address indicated in register          |
| Indirect Autoincrement | MOV @r5+, r6 | Reference the value stored at the address in register, then increment register |
| Immediate              | \#c          | The constant c                                                                 |

## Assembly Reference
* `MOV arg1, arg2` -> arg2 = arg1
* `ADD arg1, arg2` -> arg2 += arg1 (DS p56)
	* Neg bit set if result is negative, reset if positive
	* Zero bit set if result is 0, reset otherwise
	* Carry bit set if carry from result, reset otherwise
* `SUB arg1, arg2` -> arg2 = arg2 - arg1
	* Neg bit set if result is negative, reset if positive
	* Zero bit set if result is 0, reset otherwise
	* Carry bit set if carry from result, reset otherwise
* `AND arg1, arg2` -> arg2 &= arg1 (arg1 AND arg2)
* `XOR arg1, arg2` -> arg2 = arg1 XOR arg2
* `BIS arg1, arg2` -> arg2 |= arg1 (arg1 OR arg2)
* `BIC arg1, arg2` -> arg2 = Clear bits in arg1 from arg2
* `CMP arg1, arg2` -> compute arg1 - arg2, set flag, and discard results (DS p68)
	* Neg bit set if arg1 > arg2, reset if positive
	* Zero bit set if arg1 == arg2, reset otherwise
	* Carry bit set if (arg2 - arg1) < 0, reset otherwise
* `BIT arg1, arg2` -> compute arg1 & arg2, set the flags, and discard result (DS p61)
	* Neg bit set if MSB is set, reset otherwise
	* Zero bit set if result is 0, reset otherwise
	* Carry bit set if result is not 0, reset otherwise
* `TST arg1` -> Test arg1 against 0 (DS p104)
	* Neg bit set if arg1 is negative, reset if positive
	* Zero bit set if arg1 is 0, reset otherwise
	* Carry bit is always set
* `PUSH arg1` -> push arg1 onto the stack; subtract 2 bytes from SP (r1), and store arg1 in resulting location in memory
* `POP arg1` -> `MOV @SP+, arg1`; move the value stored at SP to arg1, then increment the SP by 2
* `JMP arg1` -> Jump to the location arg1 points to
* `CALL arg1` -> jumps to arg1, but first pushes the next address in memory (return address) to the stack
* `RET` -> `MOV @SP+, PC`
* `Jxx arg1` for xx NZ (not zero), Z (Zero), LO (lower), HS (higher or same), N (negative), GE (greater or equal), and L (less) are the conditional jumps, which decide based on the flag bits Z (zero), N (negative), and C (carry)

# Memory Corruption Vulnerability Examples
* Trick a device into consuming more input than it allocated for in memory to cause a buffer overflow
* Overflow a buffer that lives on the program stack to "smash the stack": overwrite another stack variable, often the return address of the current function, and use that to take control of the device, often by aiming the CPU at memory you control
* Overflow a buffer that was vreated by an allocator to "Corrupt the heap": allocators keep metadata to track the memory they're managing, and they trust that only the program can manipulate the metadata; corrupt to trick the program into writing to an arbitrary place in memory
* Integer overflow/underflow

# Sources

TI datasheet for the MSP430x1xx: https://www.ti.com/lit/ug/slau049f/slau049f.pdf
Microcorruption manual: https://microcorruption.com/public/manual.pdf