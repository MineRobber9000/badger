# badger

The Twitch Plays Pokemon badge system, ported to tildeverse IRC!

## How it works

Every 20 to 50 messages, the person talking will recieve a random badge. These badges have a distribution like so:

|Badge Name |Chance of pull|
|-----------|--------------|
|Berrybadge |65.00%        |
|Firebadge  |15.00%        |
|Rockbadge  |10.00%        |
|Waterbadge |5.00%         |
|Shadybadge |2.00%         |
|Musicbadge |1.90%         |
|Sportsbadge|1.00%         |
|Tildebadge |0.10%         |

You can transmute 3 or more badges. When you do this, it will create one, hopefully rarer badge and take the badges you put in away.

For technical documentation on how transmutation works, refer to TPP docs [here](https://twitchplayspokemon.tv/transmutation_calculations).
