let XP = SpriteKind.create()
let char_level = 1
let xp_bar = statusbars.create(120, 4, StatusBarKind.Magic)
xp_bar.bottom = 110
xp_bar.max = 10
xp_bar.value = 0
let lta = 0
let xp_to_add = 0
xp_bar.setFlag(SpriteFlag.Invisible, true)
let gstate = "battle"
// xp_to_add = game.ask_for_number("HOW MUCH")
game.showLongText("Locked in an endless conflict, our hero has been fighting back the armies of the dark lord for some time now. Her only solace? each one defeated makes her ever stronger. Unfortunately this newfound power comes at a cost, she can only absorb it by being defeated by the same enemies she fights!", DialogLayout.Full)
let text_sprite = textsprite.create("" + xp_to_add)
text_sprite.setIcon(assets.image`EXP`)
text_sprite.left = 0
text_sprite.top = 0
text_sprite.setOutline(1, 6)
function rotate(xp: Sprite) {
    let i: number;
    if (randint(0, 1) == 1) {
        for (i = 0; i < randint(0, 120); i++) {
            transformSprites.changeRotation(xp, 3)
        }
    } else {
        for (i = 0; i < randint(0, 120); i++) {
            transformSprites.changeRotation(xp, -3)
        }
    }
    
}

function go_to_xp() {
    
    for (let pip of sprites.allOfKind(XP)) {
        
        transformSprites.rotateSprite(pip, 90)
        story.spriteMoveToLocation(pip, xp_bar.x, xp_bar.y, 500)
        sprites.destroy(pip, effects.rings, 50)
        xp_bar.value += 1
        if (xp_bar.value == xp_bar.max) {
            lta += 1
            console.log(lta)
            xp_bar.value = 0
            xp_bar.max += 20
            effects.bubbles.startScreenEffect(500)
        }
        
    }
}

function level() {
    let xp: Sprite;
    
    let n = 0
    xp_bar.setFlag(SpriteFlag.Invisible, false)
    while (n < xp_to_add) {
        xp = sprites.create(assets.image`EXP`, XP)
        xp.scale = 0.6
        story.spriteMoveToLocation(xp, randint(20, 140), randint(20, 60), 300)
        timer.background(function startrotate() {
            rotate(xp)
        })
        n += 1
        text_sprite.setText("" + (xp_to_add - n))
    }
    go_to_xp()
    xp_to_add = 0
    console.log(lta)
    for (let i = 0; i < lta; i++) {
        h1a -= 10
        h1h += 25
        h1atk += 10
        h1def += 5
    }
    sprites.setDataNumber(hero, "agi", h1a)
    sprites.setDataNumber(hero, "atk", h1atk)
    sprites.setDataNumber(hero, "def", h1def)
    sprites.setDataNumber(hero, "hp", h1h)
    console.log("agi" + sprites.readDataNumber(hero, "agi") + " ATK: " + sprites.readDataNumber(hero, "atk") + " DEF: " + sprites.readDataNumber(hero, "def") + " HP: " + sprites.readDataNumber(hero, "hp"))
    for (let bar of statusbars.allOfKind(1)) {
        sprites.destroy(bar)
    }
    for (let bars of statusbars.allOfKind(2)) {
        sprites.destroy(bars)
    }
    sprites.setDataNumber(boss, "atk", batk)
    sprites.setDataNumber(boss, "def", bdef)
    sprites.setDataNumber(boss, "agi", ba)
    setup_bars(hero)
    setup_bars(boss)
    lta = 0
    gstate = "battle"
    info.setScore(0)
    xp_bar.setFlag(SpriteFlag.Invisible, true)
}

// level()
let Actor = SpriteKind.create()
let Party = SpriteKind.create()
let hero = sprites.create(assets.image`h1`, Actor)
hero.setPosition(101, 66)
let boss_sprites = [assets.image`e1`, assets.image`e2`]
let boss = sprites.create(boss_sprites[randint(0, 1)], Actor)
boss.setPosition(29, 76)
scene.setBackgroundImage(assets.image`bg`)
let bmenuopen = false
let my_menu : miniMenu.MenuSprite = null
let h1a = 100
let ba = 170
let bh = 100
let h1h = 125
let batk = 25
let h1atk = 50
let bdef = 10
let h1def = 10
sprites.setDataBoolean(hero, "acting", false)
sprites.setDataBoolean(boss, "acting", false)
sprites.setDataNumber(hero, "agi", h1a)
sprites.setDataNumber(boss, "agi", ba)
sprites.setDataString(hero, "nam", "Hero")
sprites.setDataNumber(hero, "hp", h1h)
sprites.setDataNumber(boss, "hp", bh)
sprites.setDataNumber(hero, "atk", h1atk)
sprites.setDataNumber(boss, "atk", batk)
sprites.setDataNumber(hero, "def", h1def)
sprites.setDataNumber(boss, "def", bdef)
function setup_bars(char: Sprite) {
    let agi_bar = statusbars.create(20, 4, 2)
    agi_bar.attachToSprite(char, 2)
    agi_bar.max = sprites.readDataNumber(char, "agi")
    agi_bar.value = 0
    let health_bar = statusbars.create(20, 4, 1)
    health_bar.attachToSprite(char, 4)
    health_bar.max = sprites.readDataNumber(char, "hp")
    health_bar.value = health_bar.max
}

for (let char of sprites.allOfKind(Actor)) {
    setup_bars(char)
}
hero.setKind(Party)
function bar_prog(char: Sprite) {
    
    if (sprites.readDataBoolean(char, "acting") == true) {
        return
    }
    
    if (statusbars.getStatusBarAttachedTo(2, char).value == statusbars.getStatusBarAttachedTo(2, char).max - 1 && bmenuopen && char.kind() == Party) {
        return
    } else {
        statusbars.getStatusBarAttachedTo(2, char).value += 1
    }
    
    if (statusbars.getStatusBarAttachedTo(2, char).value == statusbars.getStatusBarAttachedTo(2, char).max && bmenuopen && char.kind() == Party) {
        return
    }
    
    if (statusbars.getStatusBarAttachedTo(2, char).value == statusbars.getStatusBarAttachedTo(2, char).max && char.kind() == Party) {
        bmenuopen = true
        pmenu(char)
    } else if (statusbars.getStatusBarAttachedTo(2, char).value == statusbars.getStatusBarAttachedTo(2, char).max && char.kind() == Actor) {
        statusbars.getStatusBarAttachedTo(2, char).value = 0
        sprites.setDataBoolean(char, "acting", true)
        timer.background(function resenatt() {
            enemy_att(char)
        })
    }
    
}

function pmenu(char: Sprite) {
    
    let my_menu = miniMenu.createMenu(miniMenu.createMenuItem("Attack"), miniMenu.createMenuItem("Defend"), miniMenu.createMenuItem("Special"))
    my_menu.setTitle(sprites.readDataString(char, "nam"))
    my_menu.setMenuStyleProperty(miniMenu.MenuStyleProperty.Rows, 2)
    my_menu.setMenuStyleProperty(miniMenu.MenuStyleProperty.Columns, 2)
    my_menu.setMenuStyleProperty(miniMenu.MenuStyleProperty.Width, 120)
    my_menu.setMenuStyleProperty(miniMenu.MenuStyleProperty.Height, 40)
    my_menu.setMenuStyleProperty(miniMenu.MenuStyleProperty.BackgroundColor, 1)
    my_menu.y = 100
    my_menu.x = 80
    my_menu.setMenuStyleProperty(miniMenu.MenuStyleProperty.UseAsTemplate, 1)
    my_menu.onButtonPressed(controller.A, function on_button_pressed(selection: any, selectedIndex: any) {
        
        statusbars.getStatusBarAttachedTo(2, char).value = 0
        my_menu.close()
        if (selectedIndex == 0) {
            bmenuopen = false
            sprites.setDataBoolean(char, "acting", true)
            timer.background(function resolveatt() {
                p_attack(char)
            })
        } else if (selectedIndex == 1) {
            bmenuopen = false
            return
        } else if (selectedIndex == 2) {
            sprites.setDataBoolean(char, "acting", true)
            if (sprites.readDataNumber(char, "agi") == h1a) {
                timer.background(function resh1sp() {
                    h1_specials(char)
                })
            }
            
        }
        
    })
}

function p_attack(char: Sprite) {
    story.spriteMoveToLocation(char, char.x - 20, char.y, 100)
    pause(500)
    story.spriteMoveToLocation(char, char.x + 20, char.y, 100)
    sprites.setDataBoolean(char, "acting", false)
    let fxspri = sprites.create(assets.image`blank`)
    fxspri.setPosition(boss.x, boss.y)
    fxspri.z = 100
    animation.runImageAnimation(fxspri, assets.animation`attsp`, 50, false)
    pause(150)
    statusbars.getStatusBarAttachedTo(1, boss).value -= sprites.readDataNumber(char, "atk") - sprites.readDataNumber(boss, "def") + 1
    fxspri.destroy()
}

function h1_specials(char: Sprite) {
    
    let my_menu = miniMenu.createMenu(miniMenu.createMenuItem("Fire"), miniMenu.createMenuItem("Big Hit"))
    my_menu.setTitle(sprites.readDataString(char, "nam") + " Specials")
    my_menu.y = 100
    my_menu.x = 80
    my_menu.onButtonPressed(controller.A, function on_button_pressed(selection: any, selectedIndex: any) {
        
        my_menu.close()
        bmenuopen = false
        if (selectedIndex == 0) {
            timer.background(function ressp1() {
                h1_fire(char)
            })
        } else {
            timer.background(function ressp2() {
                h1_bh(char)
            })
        }
        
    })
}

function h1_fire(char: Sprite) {
    story.spriteMoveToLocation(char, char.x - 20, char.y, 100)
    pause(500)
    story.spriteMoveToLocation(char, char.x + 20, char.y, 100)
    sprites.setDataBoolean(char, "acting", false)
    let fxspri = sprites.create(assets.image`blank`)
    fxspri.setPosition(boss.x, boss.y)
    fxspri.z = 100
    animation.runImageAnimation(fxspri, assets.animation`fire`, 50, false)
    pause(200)
    statusbars.getStatusBarAttachedTo(1, boss).value -= sprites.readDataNumber(char, "atk") - sprites.readDataNumber(boss, "def") + 20
    fxspri.destroy()
}

function h1_bh(char: Sprite) {
    story.spriteMoveToLocation(char, char.x - 20, char.y, 100)
    pause(500)
    story.spriteMoveToLocation(char, char.x + 20, char.y, 100)
    sprites.setDataBoolean(char, "acting", false)
    let fxspri = sprites.create(assets.image`blank`)
    fxspri.setPosition(boss.x, boss.y)
    fxspri.z = 100
    animation.runImageAnimation(fxspri, assets.animation`big`, 50, false)
    pause(250)
    statusbars.getStatusBarAttachedTo(1, boss).value -= sprites.readDataNumber(char, "atk") - sprites.readDataNumber(boss, "def") + 10
    fxspri.destroy()
}

function enemy_att(char: Sprite) {
    story.spriteMoveToLocation(char, char.x + 20, char.y, 100)
    pause(500)
    story.spriteMoveToLocation(char, char.x - 20, char.y, 100)
    sprites.setDataBoolean(char, "acting", false)
    let fxspri = sprites.create(assets.image`blank`)
    let target = sprites.allOfKind(Party)[0]
    fxspri.setPosition(target.x, target.y)
    fxspri.z = 100
    animation.runImageAnimation(fxspri, assets.animation`attsp`, 50, false)
    pause(150)
    statusbars.getStatusBarAttachedTo(1, hero).value -= sprites.readDataNumber(char, "atk") - sprites.readDataNumber(hero, "def")
    fxspri.destroy()
}

game.onUpdate(function tick() {
    
    if (gstate == "battle") {
        for (let member of sprites.allOfKind(Party)) {
            bar_prog(member)
        }
        bar_prog(boss)
    }
    
})
statusbars.onZero(StatusBarKind.Health, function on_zero(status: StatusBarSprite) {
    
    if (statusbars.getStatusBarAttachedTo(1, boss).value <= 0) {
        boss.startEffect(effects.disintegrate, 500)
        statusbars.getStatusBarAttachedTo(1, boss).value = statusbars.getStatusBarAttachedTo(1, boss).max
        if (sprites.readDataNumber(boss, "agi") > 5) {
            sprites.setDataNumber(boss, "agi", sprites.readDataNumber(boss, "agi") - 15)
        }
        
        sprites.setDataNumber(boss, "atk", sprites.readDataNumber(boss, "atk") + 5)
        sprites.setDataNumber(boss, "def", sprites.readDataNumber(boss, "def") + 5)
        sprites.setDataNumber(boss, "hp", sprites.readDataNumber(boss, "hp") + 25)
        xp_to_add += randint(8, 12)
        console.log("def: " + sprites.readDataNumber(boss, "def") + " atk: " + sprites.readDataNumber(boss, "atk") + " agi: " + sprites.readDataNumber(boss, "agi"))
        text_sprite.setText("" + xp_to_add)
        sprites.destroy(statusbars.getStatusBarAttachedTo(2, boss))
        sprites.destroy(statusbars.getStatusBarAttachedTo(1, boss))
        setup_bars(boss)
        info.changeScoreBy(1)
        boss.setImage(boss_sprites[randint(0, 1)])
    } else if (statusbars.getStatusBarAttachedTo(1, hero).value <= 0) {
        gstate = "level"
        level()
    }
    
})
