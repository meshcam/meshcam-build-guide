# First boot

The firmware is already on the board. First boot is plugging in the modules,
inserting the card, and watching the node name itself and join your mesh. Do
all of it on the bench, before the box.

## Take the cell out first

The board is live whenever the cell is in. Take the cell out of the holder
before you plug anything into it, and put it back as the last step.

## 1. The camera

1. Find the ribbon connector marked **J2** at the top edge of the board.
2. Lift the connector's latch.
3. Slide the camera ribbon in with the **metal contacts facing down**,
   toward the board.
4. Press the latch closed.

## 2. The motion sensor

Plug the sensor's 3-pin lead into the connector marked **J3**. The plug
only fits one way.

## 3. The weather sensor

Push the BME280 module onto the 4-pin socket marked **J10**, with the
module's pin labels matching the labels on the board.

## The microSD card

The node stores every photo on the card, so the card has to be one the
firmware can read.

Any microSD card works, but **cards larger than 32 GB must be reformatted
FAT32**. They ship exFAT, which the camera cannot read. 32 GB and under are
usually FAT32 already. **Do not use the SD Association's "SD Memory Card
Formatter"** for a big card: it follows the SD spec and puts exFAT back.

- **macOS**: Disk Utility, select the card itself, Erase, **MS-DOS (FAT)**.
- **Windows**: the Explorer format dialog still refuses FAT32 above 32 GB.
  Use a third-party FAT32 formatter, or `format /FS:FAT32` from a Command
  Prompt on a Windows 11 build new enough to allow it.
- **Linux**: `mkfs.vfat -F 32 -s 64 /dev/sdX` (the whole card, not a
  partition).

A card the node cannot read looks exactly like a dead board. It is the
first thing to check if a node that boots never shows a photo.

## 4. The card

Push the card into the slot marked **J8** until it clicks. Push again to
eject.

## 5. Boot

1. Check the antenna is still on **J9**.
2. Put the cell back in the holder, positive end at the **+** mark.

The board boots, names itself, and starts looking for your mesh. Within a
few minutes it appears in the app under your gateway.

## 6. Check it works

1. Take a test photo from the app.
2. Wave a hand in front of the motion sensor's white dome. A capture should
   follow.
3. Check the weather readings appear with the photo.

## Optional: watch it boot on a computer

The same USB-C connector (**J1**) that charges the cell is also a serial
console. Connect it to a computer with an A-to-C cable and a USB serial
device appears. Open it in any serial terminal and you see the firmware's
boot output, ending in the board's identity line.

<!-- The exact identity line must be confirmed against the ship image before
this paragraph names it. The QC gate looks for "[radio] wire identity:" on
the test image; the ship image may differ. -->

## Dead on arrival?

If nothing in this chapter happens with a known-good cell, run the three
checks under [Troubleshooting](troubleshooting.md#dead-on-arrival) before
emailing. Those three checks are the replacement test.

<!-- Photo plan: J2 latch open with the ribbon going in contacts-down; J3
and J10 plugged; the card half-in at J8; the app showing the node's first
capture. -->
