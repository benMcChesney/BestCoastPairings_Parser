

import enum


class ArmyListFormatType(enum.Enum):
    WARSCROLL_BUILDER = 1
    BATTLESCRIBE = 2
    AOS_MOBILE_APP = 3
    UNKNOWN = 4
 

def detect_list_type( armyList ):
    #if "list" in url :
    if 1 == 2:
        print('pass')
    elif "Created with BattleScribe" in armyList :
        format = ArmyListFormatType.BATTLESCRIBE
    elif "Warhammer Age of Sigmar: The App" in armyList :
        format = ArmyListFormatType.AOS_MOBILE_APP
    elif "Allegiance: " in armyList:
        format = ArmyListFormatType.WARSCROLL_BUILDER
    else:
        format = ArmyListFormatType.UNKNOWN

    return format 

def parseKeyValue( lineString, obj , renameKey = None ) : 
    # - Lore of the Deeps: Steed of Tides
    lineString = lineString.replace( "- " , "").strip() 
    colon_firstIndex = lineString.find( ":" )
    extracted_key = lineString[ 0 : colon_firstIndex ]
    if renameKey != None : 
        extracted_key = renameKey 
    extracted_value = lineString[ colon_firstIndex+1 : ].strip()
    

    copyIndex = 1 
    
    doesExist = 1
    objKeys = obj.keys() 
    path = extracted_key 
    if extracted_key in objKeys : 
        while doesExist == 1 : 
            path = f"{extracted_key}_{copyIndex}"
            if path in objKeys : 
                doesExist = 1
            else :
                doesExist = 0 

    # what if key already exists ? 
    obj[ path ] = extracted_value 

def parseListString( armyList ):

    formatType = detect_list_type( armyList )
    lineNum = 0 
    faction_obj = {}
    units = [] 
    leader = { } 
    unit = { } 
    leaderLineNum = -1 
    battlelineLineNum = -1
    for line in armyList.splitlines():
        if formatType == ArmyListFormatType.WARSCROLL_BUILDER and len(line) > 0 :
            if lineNum == 0 :
                faction_string = line.replace( "Allegiance: " , "" ).strip()
                faction_obj["faction"] = faction_string
            elif lineNum == 1 : 
                colon_firstIndex = line.find( ":" )
                faction_obj['subfaction'] = line[colon_firstIndex+1:].strip()
            elif lineNum == 2 : 
                colon_firstIndex = line.find( ":" )
                faction_obj['grandStrategy'] = line[colon_firstIndex+1:].strip()
            elif lineNum == 3 : 
                colon_firstIndex = line.find( ":" )
                faction_obj['triumph'] = line[colon_firstIndex+1:].strip()
            elif "Leaders" in line :
               leaderLineNum = lineNum
               print('leadesr start at line ', leaderLineNum )
            elif "Battleline" in line : 
                leaderLineNum = -1 
                battlelineLineNum = lineNum
            elif "Units":
                pass
            elif ""

            # started parsing leaders
            if leaderLineNum > 0 :
                # not a subability / enhancement to leader 
                if line[0] != "-" : 
                    # what if an existing leader ?
                    if "isGeneral" in leader.keys() :  
                        units.append( leader )
                        leader = {}
                        print('resetting leader OBJ')
                    
                    # first run 
                    print('setting value run')
                    leader["name"] = line 
                    
                # is sub ability of assumed leader
                else : 
                    # only run once for general check 
                    if "isGeneral" not in leader.keys() :  
                        if "- General" in line :
                            leader["isGeneral"] = 1 
                        else :
                            leader["isGeneral"] = 0
                    parseKeyValue( line , leader )
            #battlelineLineNum = lineNum
            # started parsing battleline
            if battlelineLineNum > 0 :
                # not a subability / enhancement to leader 
                if line[0] != "-" : 
                    # what if an existing leader ?
                    #if "isGeneral" in unit.keys() :  
                    if ( unit != {} ):
                        units.append( unit )
                        unit = {}
                        print('resetting leader OBJ')
                    
                    # first run 
                    print('setting value run')
                    x_firstIndex = line.find( "x" )
                    unit['unitsCount'] = line[:colon_firstIndex].strip()
                    unit["name"] = line[colon_firstIndex+1 : ].strip() 
                    
                # is sub ability of assumed leader
                else : 
                    # only run once for general check 
                    if "isGeneral" not in leader.keys() :  
                        if "- General" in line :
                            leader["isGeneral"] = 1 
                        else :
                            leader["isGeneral"] = 0
                    parseKeyValue( line , leader )
                    


        else:
            print('implementing later....')
        lineNum += 1 
        #print(line)
    print ( "debugger ")
    # units 
    return faction_obj 
warscroll_builder_list = """Allegiance: Idoneth Deepkin
- Enclave: Mor'Phann
- Grand Strategy: The Creeping Gloomtide
- Triumphs: Indomitable

Leaders
Eidolon of Mathlann, Aspect of the Sea (325)*
- General
- Command Trait: Endless Sea Storm
- Artefact: Arcane Tome (Universal Artefact)
- Lore of the Deeps: Steed of Tides
- Lore of the Deeps: Counter-current
Akhelian Thrallmaster (110)*
Lotann, Warden of the Soul Ledgers (115)*
Isharann Soulrender (120)**

Battleline
30 x Namarti Thralls (390)**
- Reinforced x 2
10 x Namarti Reavers (170)**
10 x Namarti Reavers (170)**

Units
3 x Aetherwings (65)**

Behemoths
Akhelian Leviadon (500)**
- Mount Trait: Reverberating Carapace

Endless Spells & Invocations
The Burning Head (20)

Core Battalions
*Command Entourage - Magnificent
**Battle Regiment

Additional Enhancements
Spell

Total: 1985 / 2000
Reinforced Units: 2 / 4
Allies: 0 / 400
Wounds: 99
Drops: 4
"""



aos_app_list = """- Army Faction: Sylvaneth
- Subfaction: Heartwood
- Season of War: The Dwindling - Grand Strategy: Take What’s Theirs
- Triumph: Inspired
LEADERS
Warsong Revenant (305)***
- General
- Command Traits: Spellsinger
- Artefacts of Power: Arcane Tome
- Spells: Verdant Blessing, Verdurous Harmony
Arch-Revenant (120)***
Branchwych (130)***
- Artefacts of Power: Acorn of the Ages
- Spells: Regrowth, Verdant Blessing
BATTLELINE
Tree-Revenants (110)*
- Scion
- Glade Banner Bearer
- Waypipes
- Protector Glaive
Tree-Revenants (110)*
- Scion
- Glade Banner Bearer
- Waypipes
- Protector Glaive
Kurnoth Hunters with Kurnoth Scythes (500)**
- Huntmaster
Kurnoth Hunters with Kurnoth Greatswords (250)**
- Huntmaster
OTHER
Spiterider Lancers (420)**
- Spiterider Scion
- 2 x Spiterider Standard Bearer
- 2 x Spiterider Hornblower
ENDLESS SPELLS & INVOCATIONS
1 x Spiteswarm Hive (40)
TERRAIN
1 x Awakened Wyldwood (0)
CORE BATTALIONS
*Expert Conquerors
**Bounty Hunters
***Command Entourage
- Magnificent

TOTAL POINTS: 1985/2000
Created with Warhammer Age of Sigmar: The App"""

battlescribe_list = """++ **Pitched Battle GHB 2022** 2,000 (Chaos - Slaves to Darkness) [2,000pts] ++

+ Leader +

Archaon the Everchosen [860pts]

Centurion Marshall [145pts]: Death Dealer, General, Hellfire Sword

Chaos Lord [115pts]: Daemonbound War-Flail, Mark of Nurgle

+ Battleline +

Chaos Chosen [240pts]: 5 Chaos Chosen, Mark of Nurgle, The Eroding Icon

Varanguard [290pts]: 3 Varanguard, 3x Ensorcelled Weapon, Mark of Khorne

Varanguard [290pts]: 3 Varanguard, 3x Ensorcelled Weapon, Mark of Khorne

+ Allegiance +

Allegiance
. Allegiance: Slaves to Darkness: Host of the Everchosen

+ Game Options +

Game Type: 2000 Points - Battlehost

Grand Strategy: Dominating Presence

+ Malign Sorcery +

Endless Spell: Emerald Lifeswarm [60pts]

++ Total: [2,000pts] ++

Created with BattleScribe (https://battlescribe.net)"""

print( 'strings loaded')

#STEP 1 - detection of format, tweak to be more resiliant later 
result1 = detect_list_type( warscroll_builder_list )
print( "should be warscroll builder " , result1 )
result2 = detect_list_type( battlescribe_list )
print( "should be battlescribe " , result2 )
result3 = detect_list_type( aos_app_list )
print( "should be aos app " , result3 )

parseListString( warscroll_builder_list )