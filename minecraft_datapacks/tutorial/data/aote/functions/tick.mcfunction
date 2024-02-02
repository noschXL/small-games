execute as @e[type = item, nbt = {Item:{tag:{tp:1b}}}] if entity @e[type = item, nbt = {Item:{tag:{tp:1b}}}] run give @p diamond_sword{display: {Name:'{"text": "Aspect of the End", "color": "#0000FF"}'}, tp:1b}
execute as @p if entity @e[type = item, nbt = {Item:{tag:{tp:1b}}}] run function aote:tp
execute as @e[type = item, nbt = {Item:{tag:{tp:1b}}}] if entity @e[type = item, nbt = {Item:{tag:{tp:1b}}}] run kill @s
