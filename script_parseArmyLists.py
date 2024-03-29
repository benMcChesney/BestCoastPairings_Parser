

import enum
import pandas as pd 
import copy


class ArmyListFormatType(enum.Enum):
    WARSCROLL_BUILDER = 1
    BATTLESCRIBE = 2
    AOS_MOBILE_APP = 3
    UNKNOWN = 4
    WARSCROLL_BUILDER_PARTIAL = 5

class UnitGroup(enum.Enum):
    UNKNOWN = "UNKOWN"
    LEADER = "Leaders"
    BATTLELINE = "Battleline"
    UNIT = "Units"
    OTHER = "Other"
    BEHEMOTH = "Behemoth"
    ARTILLERY = "Artillery"
    ENDLESS_SPELLS = "EndlessSpell"
    META = "Army"

def detect_list_type( armyList ):
    #if "list" in url :
    if 1 == 2:
        print('pass')
    elif "Created with BattleScribe" in armyList :
        format = ArmyListFormatType.BATTLESCRIBE
    #elif "Warhammer Age of Sigmar: The App" in armyList or "Army Faction:" in armyList :
    elif any( h in armyList for h in [ "Warhammer Age of Sigmar: The App" , "Army Faction:" ] ):
        format = ArmyListFormatType.AOS_MOBILE_APP
    elif "Allegiance: " in armyList:
        format = ArmyListFormatType.WARSCROLL_BUILDER
        if ( "battleline" not in armyList.lower() ): 
            format = ArmyListFormatType.WARSCROLL_BUILDER_PARTIAL
    else:
        format = ArmyListFormatType.UNKNOWN

    return format 

def parseKeyValue( lineString, obj , renameKey = None ) : 
    # - Lore of the Deeps: Steed of Tides
    # print("@ start ")
    lineString = lineString.replace( "- " , "").strip() 
    colon_firstIndex = lineString.find( ":" )
    if colon_firstIndex < 0 : 
        colon_firstIndex = lineString.find( " x ")
    if colon_firstIndex > 0 : 
        extracted_key = lineString[ 0 : colon_firstIndex ]
        if renameKey != None : 
            extracted_key = renameKey 
        if len( extracted_key ) < 2 :
            extracted_key = "option"
        extracted_value = lineString[ colon_firstIndex+1 : ].strip()
    
        copyIndex = 1 
        doesExist = 1
        objKeys = obj.keys() 
        path = extracted_key 
        # what if key already exists ? 
        if extracted_key in objKeys : 
            while doesExist == 1 : 
                path = f"{extracted_key}_{copyIndex}"
                if path in objKeys : 
                    doesExist = 1
                else :
                    doesExist = 0 
                copyIndex+= 1

        #print(f"[{path}] = {extracted_value}")
        obj[ path ] = extracted_value 
        return path 

def parseGetKey( lineString ) : 
    # - Lore of the Deeps: Steed of Tides
    # print("@ start ")
    lineString = lineString.replace( "- " , "").strip() 
    lineString = lineString.replace( '.' , '' ).strip()
    colon_firstIndex = lineString.find( ":" )
  
    if colon_firstIndex > 0 : 
        extracted_key = lineString[ 0 : colon_firstIndex ]
        return extracted_key 

def resetObj( oObj , label ): 
    obj = copy.deepcopy( oObj )
    obj[ "type" ] = label
    return obj


def parseListString( armyList , listId ):


    formatType = detect_list_type( armyList )
    print("format is ", formatType )
    lineNum = 0 
    faction_obj = {}
    faction_obj[ "listId"] = listId 
    units = [] 
    keep = [] 
    leaderHeaders = [ "Leaders" , "LEADERS" ]
    unit = { } 
    headingType = UnitGroup.META
    prevLine = ""
    armyList = armyList.replace( '```' , '' ).strip() 

    i = 0 
    factionLine = -1 
    for line in armyList.splitlines() :
        if len( line ) > 0 and "Created with BattleScribe" not in line : 
            #if "Leaders" in line or "LEADERS" :
            #print(  f"@ {lineNum} : {line}" )
            oldHeading = headingType 
            if any( h in line for h in [ "Leaders" , "LEADERS" , "+ Leader +" , "LEADER" ] ):
                headingType = UnitGroup.LEADER
                unit["type"] = headingType.value
            
            if any( h in line for h in [ "+ Allegiance +" , "Allegiance" ] ):
                headingType = UnitGroup.META

            #if "Battleline" in line or "BATTLELINE" in line :    
            if any( h in line for h in [ "Battleline" , "BATTLELINE" , "+ Battleline +"] ):           
                headingType = UnitGroup.BATTLELINE
                unit = resetObj(faction_obj, headingType.value)
                #print('BATTLELINE start at line ', lineNum )

            #if "Units" in line or "OTHER" in line :
            if any( h in line for h in [ "Units" , "OTHER" ] ):
                headingType = UnitGroup.UNIT
                unit = resetObj(faction_obj, headingType.value)
                #print('Units start at line ', lineNum )
            
            #if "Endless Spells" in line or "ENDLESS SPELL" in line:
            if any( h in line for h in [ "Endless Spells" , "ENDLESS SPELL" ] ):
                headingType = UnitGroup.ENDLESS_SPELLS
                unit = resetObj(faction_obj, headingType.value)
                #print('Endless start at line ', lineNum )

            #if "Behemoth" in line or "BEHEMOTH" in line : 
            if any( h in line for h in [ "Behemoth" , "BEHEMOTH", "Behemoths" ] ):
                headingType = UnitGroup.BEHEMOTH
                unit = resetObj(faction_obj, headingType.value)

            if headingType == UnitGroup.META : 
                if formatType == ArmyListFormatType.WARSCROLL_BUILDER_PARTIAL : 
                    dashIndex = line.find( '-' )
                    if lineNum > 1 and dashIndex == -1 :
                        headingType = UnitGroup.UNIT  
                        unit = {} 
                        #print('resetting obj')

            # change!
            if oldHeading != headingType : 
                #print( f" change in heading from {oldHeading} -> {headingType} ")
                if formatType in [ ArmyListFormatType.AOS_MOBILE_APP 
                , ArmyListFormatType.WARSCROLL_BUILDER  ] : 
                    if unit != {} :  
                        units.append( unit )
                if formatType in [ ArmyListFormatType.BATTLESCRIBE ]:
                    unit = {}
            
                
            # started parsing leaders
            if headingType == UnitGroup.LEADER :
                # not a subability / enhancement to leader 
                if len(line) > 1 and line[0] != "-" : 
                    if line != headingType.value:
                        if formatType in [ ArmyListFormatType.AOS_MOBILE_APP 
                            , ArmyListFormatType.WARSCROLL_BUILDER ]:
                            
                            units.append( unit )
                            unit = {}
                            unit["type"] = headingType.value
                            l_paren = line.find( "(" )
                            r_paren = line.find( ")" )
                            if r_paren > l_paren : 
                                unitCount = 1 
                                name  = line[ 0 : ].strip()
                                unit['unitsCount'] = unitCount
                                unit["points"] = line[ l_paren+1: r_paren ].replace( "pts" , "")
                                unit["name"] = line[ : l_paren-1 ].strip() 
                        if formatType in [ ArmyListFormatType.BATTLESCRIBE ]:
                            unitCount = 1 
                            lbracket = line.find( "[" )
                            rbracket = line.find( "]" )
                            if lbracket > 0 : 
                                unit[ "name" ] = line [ : lbracket - 1 ]
                                unit[ "points" ] = line [ lbracket + 1 : rbracket - 1 ]
                                unit['unitsCount'] = 1
                                colon_firstIndex = line.find( ":" )
                                options = line[ colon_firstIndex + 1 : ]
                                splitList = options.split( ',')
                                # print ( line )
                                #for o in splitList : 
                                #    print( o )
                                #    toSend = f"Option:{o}"
                                #    print(toSend)
                                #    parseKeyValue( toSend , unit , "Option" )
    
                # is sub ability of assumed leader

                else :
                    if formatType in [ ArmyListFormatType.AOS_MOBILE_APP
                    , ArmyListFormatType.WARSCROLL_BUILDER ]:
                    # only run once for general check 
                        if "general" in line.lower() :
                            unit["isGeneral"] = 1 
                        if "Lore: " in line : 
                            parseKeyValue( line , unit , "Spell" )
                            colon_firstIndex = line.find( ":" )

                            to_pass =  "lore: " + line[  : colon_firstIndex  ]
                            parseKeyValue( to_pass , unit , "Spell Lore")
                        
                        elif "Spells:" in line : 
                            #- Spells: Regrowth, Verdant Blessing
                            colon_firstIndex = line.find( ":" )
                            splitSpells = line[  colon_firstIndex+1 : ].split( "," )
                            for s in splitSpells : 
                                toSend = f"Spell:{s}"
                                parseKeyValue( toSend, unit )
                        else : 
                            parseKeyValue( line , unit )
                    elif formatType == ArmyListFormatType.BATTLESCRIBE : 

                        lbracket = line.find( "[" )
                        rbracket = line.find( "]" )
                        if lbracket > 1 : 
                            unit = {}
                            unit[ "name" ] = line [ : lbracket - 1 ]
                            unit[ "points" ] = line [ lbracket + 1 : rbracket - 3 ]

                            colon_firstIndex = line.find( ":" )
                            options = line[  colon_firstIndex+1 : ]
                            commaIndex = options.find( ",")
                            
                            if commaIndex > 0 :
                                optionsList = options.split( ",")
                                for x in range( 0 , len( optionsList ) ) : 
                                    unit[ f"option_{x}"] = optionsList[x]
                            #    for slo in optionsList : 
                            #        feedIn = f"Option:{slo}"
                            #        parseKeyValue( feedIn , leader )
                            
                            units.append( unit )
            #battlelineLineNum = lineNum
            # started parsing battleline

            elif headingType == UnitGroup.META:
                
                if formatType in [ ArmyListFormatType.AOS_MOBILE_APP , ArmyListFormatType.WARSCROLL_BUILDER ]:
                
                    if lineNum == 0 :
                    #line_lower = line.lower()
                    #if "faction" in line_lower and "subfaction" not in line_lower : 
                    #if ":" in line_lower : 
                        parseKeyValue( line , faction_obj , "faction")
                        #factionLine = lineNum 
                    #if (factionLine + 1 ) == lineNum :
                    #    parseKeyValue( line , faction_obj ,  "subfaction")  
                    #"subfaction" in line_lower :     
                    elif lineNum == 1 and "grand strategy:" not in line.lower() : 
                        parseKeyValue( line , faction_obj ,  "subfaction")  
                    else: 
                        #print("debugger")
                        parseKeyValue( line , faction_obj )
                if formatType == ArmyListFormatType.BATTLESCRIBE : 
                    #if lineNum == 0 : 
                    
                    if "Allegiance:" in line : 
                        #++ **Pitched Battle GHB 2022** 2,000 (Chaos - Slaves to Darkness) [2,000pts] ++
                        factionLine = lineNum
                        
                        parseKeyValue( line , faction_obj , "faction")
                        
                        #rParen = line.find( ")" )
                        #lParen = line.find( "- " )
                        #if rParen > 0 :
                        #    faction_obj[ "faction" ] = line[ lParen + 1 :  rParen - 1].strip()    
                    elif factionLine > 0 and lineNum == factionLine+1 : 
                        subfactionKey = parseGetKey( line )
                        faction_obj[ "subfaction" ] = subfactionKey ; 
                        parseKeyValue( line , faction_obj , "subfaction_option")
                    else : 
                        parseKeyValue( line , faction_obj )
                                    
                if formatType == ArmyListFormatType.WARSCROLL_BUILDER_PARTIAL :
                    if lineNum == 0 :
                        parseKeyValue( line , faction_obj , "faction")
                    elif lineNum == 1 : 
                        parseKeyValue( line , faction_obj ,  "subfaction")
            
            elif headingType in [ UnitGroup.BATTLELINE 
                , UnitGroup.ARTILLERY 
                , UnitGroup.BATTLELINE
                , UnitGroup.BEHEMOTH 
                , UnitGroup.ENDLESS_SPELLS
                , UnitGroup.UNIT ]:
                # print( headingType.value )
                # not a subability / enhancement to leader 
                if formatType in [ ArmyListFormatType.AOS_MOBILE_APP 
                    , ArmyListFormatType.WARSCROLL_BUILDER 
                    , ArmyListFormatType.WARSCROLL_BUILDER_PARTIAL ]:
                    if len(line) > 1 and line[0] != "-" : 
                        # what if an existing leader ?
                        #if "isGeneral" in unit.keys() :  
                        if ( unit != {} ):
                            units.append( unit )
                            # print('adding unit')
                            unit = {}
                            unit["type"] = headingType.value
                            
                        # first run 
                        #print('setting value run')
                        x_firstIndex = line.find( "x" )
                        l_paren = line.find( "(" )
                        r_paren = line.find( ")" )
                        if r_paren > l_paren : 
                            unitCount = 1 
                            if x_firstIndex > 1 :
                                unitCount = line[:x_firstIndex-1].strip()
                            name  = line[x_firstIndex+1 : ].strip()
                            unit['unitsCount'] = unitCount
                            unit["points"] = line[ l_paren + 1 : r_paren ]
                            unit["name"] = line[x_firstIndex+1 : l_paren-1 ].strip() 
                        
                    # is sub ability of assumed leader
                    else : 
                        # only run once for general check 
                        parseKeyValue( line , unit )
                elif formatType in [ ArmyListFormatType.BATTLESCRIBE ]:
                    
                    unit = {}
                    unit["type"] = headingType.value
                    # print('resetting battleline OBJ')
                    lbracket = line.find( "[" )
                    rbracket = line.find( "]" )
                    if lbracket > 0 : 
                        unit[ "name" ] = line [ : lbracket - 1 ]
                        unit[ "points" ] = line [ lbracket + 1 : rbracket - 3 ]
                        colon_firstIndex = line.find( ":" )
                        options = line[  colon_firstIndex+1 : ]

                        commaIndex = options.find( ",")
                        if commaIndex > 0 :
                            optionsList = options.split( ",")
                            for x in range( 0 , len( optionsList ) ) : 
                                unit[ f"option_{x}"] = optionsList[x]
                        units.append( unit )   
                
                    # is sub ability of assumed leader
                    else : 
                        # only run once for general check 
                        parseKeyValue( line , unit )
                else:
                    print('implementing later....')
        else:
            skipThisIndex = 45 
            # skipping...
        # count "valid lines"
        #if ":" in line : 
        lineNum += 1 
        prevLine = line 

    for u in units : 
        if "name" in u.keys():
            u[ "listId"] = listId 
            keep.append( u ) 

    return keep , faction_obj 

#units_df = [] 
#factions_df = [] 

units_df = pd.DataFrame({})
factions_df = pd.DataFrame({})
#units, faction = parseListString( lrl_list , 'asdas' )
#units_df.to_csv('listParse_units.csv')
#factions_df.to_csv('listParse_factions.csv')


event_df = pd.read_csv( "_DONE_event_army_lists_progress.csv" )
#event_df = pd.read_csv( "Dv3LDfBRAU_event_data_badParsing.csv") 
event_df.reset_index() 

for index, row in event_df.iterrows():
                
    listUrl = row["list_url"] 
    slashIndex = listUrl.rfind( "/")
    listId = listUrl[ slashIndex + 1 : ]
    #print( 'loading list ', listId )
    #https://www.bestcoastpairings.com/list/DWPNWKX8CK

    army_list = row [ "full_list_text" ] 
    if isinstance(army_list, str) :
        units, faction = parseListString( army_list , listId )
        units_df = pd.concat( [ units_df , pd.json_normalize( units ) ] )
        factions_df = pd.concat( [ factions_df , pd.json_normalize( faction ) ] )

        units_df.to_csv('listParse_units.csv')
        factions_df.to_csv('listParse_factions.csv')
         
   
