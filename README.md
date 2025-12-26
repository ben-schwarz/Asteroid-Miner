The core gameplay loop is complete, although there's still room to add different power-ups
and I haven't implemented the ammunition and air systems that I came up with in the power
point. Right now, all of the available upgrades are simple numerical improvements. The game will
also need proper visuals and ideally some sound effects if I can find any. I would've added some
sprite animation this delivery for the gold pick-ups but I couldn't log into Adobe with my
school account, so I couldn't use Photoshop. I also plan to add a spaceship-style enemy that
appears when there are very few asteroids remaining. I also plan to add more asteroid shapes.

Features in this build:
Window size increased
Asteroids now move more slowly. Diagonal asteroids still move twice as fast as horizontal ones.
Lasers last longer to compensate for the larger window
Asteroids drop gold pickups that increase the score when the player touches them. These pickups
are intended to decay eventually to prevent soft-locking, but I never checked if this actually works. It should occur after being updated 300 times.
The gameplay stage ends when the player runs out of hits from crashing into asteroids
After being hit by an asteroid, the player becomes invulnerable for 1.5 seconds, causing their
sprite to appear partially transparent for this period.
When all asteroids are destroyed, the round will increase by 1, and four more asteroids will
spawn. Later rounds do not currently increase score gained or difficulty in any way. Rounds will
also not progress if there are any pick-ups still onscreen.
Once the gameplay stage ends, the player is moved to the upgrade stage, where they can spend
their score to improve their ship by increasing the mercy period after getting hit, increasing
the speed of their ship, and increasing the number of hits before the game stage ends.
Increasing speed kind of makes the game harder.
All of these values have a maximum, and once this maximum is reached, the button to upgrade them
will stop being drawn.
When the player presses the continue button, they will be placed back in the gameplay stage.
The escape key can be pressed at any time to end the game.

Once, I experienced a bug where the round did not progress despite all of the asteroids being
destroyed. Presumably, this was because a score-pickup was offscreen, and although this would've
resolved itself through the pickups decaying, an alternative solution would be to make the
pickups move very slowly and wrap around the screen like all other sprites.
