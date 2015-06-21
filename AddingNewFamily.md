# Adding a Family #

As usual I assume you're familiar with adding values to a given database table, so without further ado opens the `families` table and proceed with adding a new record.

## How do I fill all those fields ? ##

Diffidently from the `clans` table here you get a lot of fields to fill, so let's start from the beginning:

  * `uuid` : add 1 to the last `uuid` you specified ( e.g. 5002 ). Remember to never add 2 items with the same uuid.
  * `name` : the family name
  * `clan_id` : browse the `clans` table and fill this value with the corresponding `uuid` field of the wanted clan. ( e.g. If you want to add a Family to the Crab clan write **1** on the `clan_id` field.
  * `perk` : This is the bonus trait, **use ALL lowercase letters**
  * `perkval` : Usually **1** you can specify how many grades the family bonus add to the Trait.

## Done ##

Click ok and we've added our first custom family! :)

## Sidenote ##

One might want to edit an existing family ( or whatever else ).
The procedure is the same but you don't need to create a new record; just double-click on an existing item and edit its value.

DO NOT CHANGE THE `uuid` FIELDS in this case.