# Battery and solar

The board runs from one 26650 LiFePO4 cell in the holder on the board. The
solar panel keeps that cell charged. **USB does not power the board.** It
only feeds the charger, and with no cell fitted the board does nothing on
USB at all. That is why this chapter starts with the cell and ends with USB.

## 1. Fit the antenna

Do this before the board ever has power. The radio can be damaged if it
transmits with nothing connected.

1. Push the small round end of the pigtail onto the connector marked **J9**
   until it clicks.
2. Screw the whip antenna onto the other end of the pigtail, finger tight.

## 2. Fit the cell

1. Check the cell: it must say **IFR26650** or **LiFePO4**, 3.2 V. Put a
   3.7 V Li-ion cell back in its box.
2. Look at the holder for the **+** mark.
3. Press the cell into the holder, positive end at the **+** mark.

The holder has reverse-insertion protection. A backwards cell does no harm,
but the board will not run until the cell is turned around.

The board boots the moment the cell goes in. Leave it alone for now; the
next chapter covers what it does.

## 3. Charge it from the sun

A new cell arrives partly charged, at an unknown level. The normal way to
fill it is the same way the node will live: on the panel.

1. Plug the solar pigtail into the connector marked **J6**. The plug only
   fits one way.
2. Connect the panel to the pigtail. If the panel has bare leads, match
   red to the pigtail's **+** mark.
3. Put the panel in a sunny window, or outside, for a day or two.

The panel makes about five times what the node uses, even in poor winter
light. A flat cell is full after a couple of days of sun. While it charges,
the three small lights at the board edge tell you what is happening; the
table is below.

## 4. Optional: top up over USB

If you are impatient, or the cell is nearly flat and you want to bench-test
tonight, USB fills it in about ten hours. This step is optional. A node that
is never plugged into USB cannot have a USB problem.

1. Use a **USB-A wall charger** and an **A-to-C cable**. Not a power bank,
   and not a C-to-C cable (see [Parts list](parts.md#optional-usb) for why).
2. Plug the C end into the connector marked **J1**.
3. Read the lights.

## The charge lights

Three lights sit together at one edge of the board: **input**, **CHG**
(red) and **DONE** (green). Four combinations mean something:

| Input | CHG (red) | DONE (green) | Meaning | What to do |
|---|---|---|---|---|
| dark | dark | dark | No power is reaching the board. | It is the cable or the charger, not the board. Try another cable (A-to-C) or another wall charger. |
| lit | lit | dark | Charging normally. | Nothing. |
| lit | dark | lit | Full. | Nothing. |
| lit | dark | dark | The charger is declining to charge. | Charging is blocked below about 0 °C and above about 60 °C. Let the board reach room temperature and try again. If it still declines, email us. |

The same table is in [Troubleshooting](troubleshooting.md#the-charge-lights)
and on the [pinout page](https://docs.getmeshcam.com/pinout).

<!-- Photo plan: J9 with the pigtail clicked on; the holder with the + mark
visible and the cell half-in; J6 with the solar plug; the three LEDs lit in
the "charging" state. All from the bench photography afternoon. -->
