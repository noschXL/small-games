var upgrade_buyer = setInterval(function(){
    for (key in Game.Upgrades) {
        if(Game.cookies >= Game.Objects[key].basePrice){
            Game.Upgrades[key].buy()
        }
    }
},1)