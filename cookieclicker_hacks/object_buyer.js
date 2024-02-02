var object_buyer = setInterval(function(){
    for (key in Game.Objects) {
        if(Game.cookies >= Game.Objects[key].price){
            Game.Objects[key].buy()
        }
    }
},1)