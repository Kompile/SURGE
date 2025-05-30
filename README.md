# SURGE
A Blender addon for generating surf ramp meshes.

For instructions on how to use this addon, check out my tutorial video: https://youtu.be/WWZm1lRNFAs

If you like verbose single-script Python, then have I got a repository for you!

This is my first addon for Blender and my first piece of Python I’ve written, so naturally it’s not the best block of code you are likely to see, but it works! At least in Blender 2.91...

Essentially, It’s just one script file and a custom icon folder. The script is far too long at this point and needs to be separated into multiple files and refactored somewhat, but that’s perhaps something another contributor would like to get involved with. Feel free to fix my code!

DONT FORGET $concave
THIS ALLOWS THE PHYSICS MESH TO CURVE WITH THE RAMP, WITHOUT THIS YOU WILL ONLY BE ABLE TO MAKE STRAIGHT RAMPS
Example qc:
$modelname "ramsay/ramps/ramp.mdl"
$cdmaterials "models/ramsay/ramps/"
$body "ramp" "ramp.smd"


$collisionmodel "ramp_phys.smd"
{
    $mass 1
    $inertia 1
    $damping 1
    $rotdamping 1
    $concave
}

$staticprop
$sequence idle "ramp.smd" fps 1
