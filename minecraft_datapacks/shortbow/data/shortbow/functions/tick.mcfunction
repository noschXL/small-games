execute as @a[nbt = {SelectedItem:{id: "minecraft:carrot_on_a_stick", tag:{short:1b}}}, scores = {shot = 1..2147483647}] at @s run function shortbow:shoot
kill @e[nbt = { inGround:true}]