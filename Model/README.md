# lattice1
A grid-maze prototype with separator objects between cells.

This is a follow-up to the implementation in `DungeonAdventure`,
which has some deficiencies:
- Relies on boolean door-or-wall attributes in `Room` instances,
which requires the corresponding attributes of orthogonally adjacent
rooms be kept synchronized.
- Each room has an attribute for its coordinates within its container grid,
but no direction linkage to adjacent rooms. This necessitates interaction
with the grid in order to traverse/peer. Also complicates adding rooms to
a grid after its initial creation. Also complicates any configuration other
than simple rectangle.