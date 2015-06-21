# Introduction #

In order to add more data into the program database first one need to crawl into the game manuals and write down the data into a computer-friendly format. In this section I'll describe this format.

# Clan data format #
To describe a Clan you need to provide a lot of data, that is divided
in several files. In this guide we will follow one by one the steps needed to import the Scorpion clan into the program.

## The Family file ##
First open a text editor and create a new file called Scorpion\_Families.txt,
in this file we will put the data that represents the Scorpion Clan families in this format:

```
#
FamilyName
FamilyAttributeBonus
1
#
```

and repeat for each family, that will results in:

```
#
Bayushi
agility
1
#
Shosuro
awareness
1
#
Soshi
intelligence
1
#
Yogo
willpower
1
```

Save the file.

## The School bonuses file ##
Next we need a file called Schools\_Scorpion.txt, each record will contain the information about a Clan School and its starting bonuses in this format:

```
#
School Name
tag
trait bonus
honor startingvalue
ElementAffinity or -
ElementDeficiency or -
#
```

for the Scorpions clan this results in:

```
#
Bayushi Bushi School
bushi
intelligence 1
honor 2.5
-
-
#
Soshi Shugenja School
shugenja
awareness 1
honor 2.5
air
earth
#
Bayushi Courtier School
courtier
awareness 1
honor 2.5
-
-
#
Shosuro Infiltrator School
ninja
reflexes 1
honor 1.5
-
-
```

## The School Skills file ##
Next we need a file called Skills\_Scorpion.txt, each record will contain the information about a Clan School and its starting skills in this format:

```
#
SchoolName
SkillName (Emphasis), OtherSkill ?2, *wildcard
#
```

The second line has each skill separed by a comma, and any emphases is placed between parentesis. Also if you need the starting rank to be higher than 1, add ?2 or ?3, etc.. at the end.

When the manual don't specify a named skill but a category you can add a wildcard. Some wildcards are:

```
*any    = Any Skills
*bugey  = Any Bugei skills
*high   = Any High skills
*weapon = Any Weapon skills
```

and so on...

The result is:

```
#
Bayushi Bushi School
Courtier (Manipulation), Defense, Etiquette, Iaijutsu, Kenjutsu, Sincerity, *any
#
Soshi Shugenja School
Calligraphy (Cipher), Courtier, Etiquette, Lore_(Theology), Spellcraft, Stealth, *any
#
Bayushi Courtier School
Calligraphy, Courtier (Gossip), Etiquette, Investigation, Sincerity (Deceit), Temptation, *high
#
Shosuro Infiltrator School
Acting, Athletics, Ninjutsu, Sincerity, Stealth (Sneaking) ?2, *any
```

## The School Techniques file ##

Next we need a file called Techs\_Scorpion.txt, each record will contain the information about a Clan School and its techniques in this format:

```
#
SchoolName
unique_name_1; Technique Name 1
unique_name_2; Technique Name 2
unique_name_3; Technique Name 3
unique_name_4; Technique Name 4
unique_name_5; Technique Name 5
#
```

and for the Scorpion clan this results in:

```
#
Bayushi Bushi School
bayushi_bushi_1; The Way Of The Scorpion
bayushi_bushi_2; Pincers And Tail
bayushi_bushi_3; Strike At The Tail
bayushi_bushi_4; Strike From Above, Strike From Below
bayushi_bushi_5; The Pincers Hold, The Tail Strikes
#
Soshi Shugenja School
soshi_shugenja_1; The Kami's Whisper
#
Bayushi Courtier School
bayushi_courtier_1; Weakness Is My Strength
bayushi_courtier_2; Shallow Waters
bayushi_courtier_3; Secrets Are Birthmarks
bayushi_courtier_4; Scrutiny'S Sweet Sting
bayushi_courtier_5; No More Masks
#
Shosuro Infiltrator School
shosuro_ninja_1; The Path Of Shadows
shosuro_ninja_2; Strike From Darkness
shosuro_ninja_3; Steel Within Silk
shosuro_ninja_4; Whisper Of Steel
shosuro_ninja_5; The Final Silence
#
```

## The School Spells file ##
Next we need a file called Spells\_Scorpion.txt, each record will contain the information about a Clan School and its starting spells in this format:

```
#
ShugenjaSchoolName
ListOfSpellsOrWildCards
#
```

as skills we can use Spell names or wildcard to specify the spells.
Wildcards available are:

```
*any  = Any Ring
*fire = Fire Ring
*air  = Air Ring
... and so on
```

For the Scorpion clan ( only one Shugenja school ) here the result:

```
#
Soshi Shugenja School
Sense, Commune, Summon, *air (3), *fire (2), *water (1)
#
```