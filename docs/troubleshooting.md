# Troubleshooting

Most problems are one of five things: the cable, the cell, the card, the
antenna, or range. Work down this page in order.

## The charge lights

Three lights at one edge of the board: **input**, **CHG** (red) and
**DONE** (green).

| Input | CHG (red) | DONE (green) | Meaning | What to do |
|---|---|---|---|---|
| dark | dark | dark | No power is reaching the board. | It is the cable or the charger, not the board. Try an A-to-C cable and a wall charger. |
| lit | lit | dark | Charging normally. | Nothing. |
| lit | dark | lit | Full. | Nothing. |
| lit | dark | dark | The charger is declining to charge. | Charging is blocked below about 0 °C and above about 60 °C. Let the board reach room temperature and retry. Still declining with a known-good cell: email us. |

## Nothing lights up on USB

In order of likelihood:

1. **C-to-C cable.** The board is a plain 5 V load with no negotiation
   chip. Many C-to-C cables never switch the power on for it. Use an
   **A-to-C** cable from a **USB-A wall charger**.
2. **Power bank.** Banks switch off below the charger's idle draw. Use a
   wall charger.
3. **No cell fitted.** USB only feeds the charger. The board does not run
   on USB alone. Fit the cell.

## The board does not boot with a cell in

1. **Cell backwards.** The holder's protection stops a backwards cell from
   doing harm, and also from running. Turn it around, positive end at the
   **+** mark.
2. **Wrong cell.** A 3.7 V Li-ion 26650 is not the right cell and should
   not be in the holder. The board wants a 3.2 V IFR26650 LiFePO4.
3. **Flat cell.** A cell that sat on a shelf can be too flat to boot. Put
   the panel in the sun for a day, or top up over USB, and try again.

## The node boots but never shows a photo

1. **The card is exFAT.** Every card over 32 GB ships that way and the
   firmware cannot read it. Reformat it FAT32 as described in
   [First boot](first-boot.md#the-microsd-card). This looks exactly like
   dead hardware and is the most common cause.
2. **The camera ribbon is in upside down or not latched.** Contacts face
   down, toward the board, and the latch is pressed closed.

## The node is not in the app

1. **Antenna.** Is the pigtail clicked onto **J9** and the whip screwed
   on?
2. **Range.** The node needs a radio path to a gateway or another node.
   Try it next to the gateway first; if it appears there, the problem is
   the path, not the node. Height helps more than anything.
3. **Gateway.** Is the gateway online in the app?

## The motion sensor never triggers

1. The dome must be clear of the box and clear of silicone.
2. The sensor senses heat moving across its view. A hand waved directly at
   it from a few centimetres triggers it; a warm body walking past at ten
   metres does too. A deer standing still does not.

## Dead on arrival

A board is dead on arrival if it fails this check as shipped. Do it with
nothing but a cell and a USB cable, before fitting anything else.

1. Fit a charged IFR26650 LiFePO4 cell in the holder, positive end at the
   **+** mark. Fit nothing else.
2. Connect a USB-A wall charger with an A-to-C cable to **J1**. Expected:
   the **input** light lights, and **CHG** lights red (or **DONE** lights
   green if the cell is already full). Input lit with both others dark
   means the charger declined; let the board reach room temperature and
   retry.
3. Connect **J1** to a computer instead. A USB serial device appears. Open
   it in a serial terminal. Expected: boot output from the MeshCam
   firmware, ending in the board's identity line.

A board that does all three is not dead on arrival. A board that does none
of them with a known-good cell and cable is, and an email to
hello@getmeshcam.com with the serial number on the board gets it replaced.
Buyer assembly, soldering and part substitutions are outside that
replacement.

## Fixing the guide

If a step here was wrong or missing, the guide is a public repository.
Open an issue or send a change; a correction there helps every builder
after you.
