# summon the temporary entity
execute as @e[nbt = {SelectedItem:{id: "minecraft:carrot_on_a_stick", tag:{short:1b}}}, scores = {shot = 1..2147483647}] at @s run summon marker ^ ^ ^4 {Tags:["direction"]}

# get the coordinates of the player and the entity
execute store result score #playerX pos run data get entity @s Pos[0] 1000
execute store result score #playerY pos run data get entity @s Pos[1] 1000
execute store result score #playerZ pos run data get entity @s Pos[2] 1000
execute store result score #targetX pos as @e[type=marker,tag=direction,limit=1] run data get entity @s Pos[0] 1000
execute store result score #targetY pos as @e[type=marker,tag=direction,limit=1] run data get entity @s Pos[1] 1000
execute store result score #targetZ pos as @e[type=marker,tag=direction,limit=1] run data get entity @s Pos[2] 1000

# do the math
scoreboard players operation #targetX pos -= #playerX pos
scoreboard players operation #targetY pos -= #playerY pos
scoreboard players operation #targetZ pos -= #playerZ pos

# summon the projectile entity
execute as @e[nbt = {SelectedItem:{id: "minecraft:carrot_on_a_stick", tag:{short:1b}}}, scores = {shot = 1..2147483647}] at @s run summon arrow ~ ~1 ~ {Tags:["projectile"]}

# apply motion to projectile
execute store result entity @e[type=arrow,tag=projectile,limit=1] Motion[0] double 0.001 run scoreboard players get #targetX pos
execute store result entity @e[type=arrow,tag=projectile,limit=1] Motion[1] double 0.001 run scoreboard players get #targetY pos
execute store result entity @e[type=arrow,tag=projectile,limit=1] Motion[2] double 0.001 run scoreboard players get #targetZ pos

# clean up, ready for the next player
tag @e[tag=projectile] remove projectile
kill @e[tag=direction]
execute as @e[nbt = {SelectedItem:{id: "minecraft:carrot_on_a_stick", tag:{short:1b}}}, scores = {shot = 1..2147483647}] at @s run scoreboard players set @s shot 0