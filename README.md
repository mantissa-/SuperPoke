# SuperPoke

Iterative poking tool for Blender

![SuperPoke UI](https://imgur.com/FsokgmO.png)

### Installation

Download the zip and install as an addon in Blender 2.80 or higher.
SuperPoke settings can be found in the side panel of the 3D viewport.

# Overview

**Keep Original:** Keep a copy of the original mesh

**Apply Modifiers:** Apply the current modifier stack before processing

**Iterations:** Number of times to poke all faces of the mesh

**Poke Offset:** How far the poke pushes out (positive values) or in (negative values)

**Offset Multiplier:** The poke offset gets multiplied by this amount every iteration, set to 1 if you want to keep the amount the same on every iteration

**Alternate Offset:** Enable this to alternate between poking in- and outward on each iteration

**Create Shape Keys:** This option creates a shape key for each iteration so they can be animated, use with cuation as this is slower than the regular static algorithm

___

### Examples

![Iterations](https://imgur.com/D6psaKm.png)
_Iterations example, other settings are left default._

![Alternate Offset](https://imgur.com/heaCjzK.jpg)
_Same settings, but with alternate offset disabled and enabled respectively._
