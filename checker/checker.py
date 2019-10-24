import time
import logging
import sys
import asyncio
import random
import json

from string import ascii_letters, digits
from enochecker_async import BaseChecker, BrokenServiceException, create_app, OfflineException, ELKFormatter, CheckerTaskMessage
from logging import LoggerAdapter
from motor import MotorCollection


songs = """
Shell Shock
And I'm Like (DJ Edit)
Forbidden (DJ Edit)
Space Inavder (Wulfx Remix)
The Mega Bundle 2
When I'm There (DJ Edit)
Hardcore Addiction 6
Hard Dance Bangers, Vol. 02
Hard Dance Anthems, Vol. 15
Earth Bb (DJ Edit)
Candy (DJ Edit)
Old Skool Masters - S3RL
Remix EP 18
The Future Of Hardcore Finale
Inspiration (DJ Edit)
Hard Dance Anthems, Vol. 10
Never Let You Go
S3RL Remix EP 14
My Girlfriend is a Raver
S3RL Remix EP 9
Warehouse Anthems: Hardcore, Vol. 6
Hentai
Hardcore Addiction 3
The Future Of Hardcore Album (Bestsellers)
All That I Need (DJ Edit)
Hard Dance Anthems, Vol. 09
Remix EP 11
Warehouse Anthems: Hardcore Vol. 3
MTC Saga (DJ Edit)
S3RL Remix EP 17
Warehouse Anthems: Hardcore Vol. 2
Bring It 2
Remix EP 7
Hypnotoad (DJ Edit)
Music Is My Saviour
Now That I've Found You (DJ Edit)
Escape (DJ Edit)
Next Time (DJ Edit)
Warehouse Anthems: Hardcore, Vol. 9
Hard Dance Bangers, Vol. 03
Click Bait (DJ Edit)
You're My Superhero (DJ Edit)
Hardcore x YIR
MTC2 (DJ Edit)
Warehouse Anthems: Hardcore, Vol. 14
Casual N00b (DJ Edit)
Essential Guide: Hard House, Vol. 5
Remix 15
Warehouse Anthems: Hardcore, Vol. 5
The Fix (S3RL Remix)
Jaded AF (DJ Edit)
Stamina Summer Slammers, Vol. 4
Bass Slut (Sash Dee & Hardside Remix)
Warehouse Anthems: Hardcore, Vol. 13
Silicon XX (DJ Edit)
Hard Dance Bangers, Vol. 04
Beat All The Odds (DJ Edit)
Eh!?
Cherry Pop
Through the Years
It's This Again (DJ Edit)
Hard Dance Anthems, Vol. 03
Who's Got The Stamina?!, Vol. 2
The Future Of Hardcore Summer Bundle
Well, That Was Awkward (Ambiguous DJ Edit)
Xtreme Warfare EP
Nightcore This (DJ Edit)
Hard Dance, Vol. 12
Hard Dance Anthems, Vol. 06
Where Did You Go
Mc Offside- Breaking Boundaries (Re Release)
Kniteforce Radio All Stars, Vol. 1
Avaline
Berserk (DJ Edit)
Fire (DJ Edit)
Hard Dance Anthems, Vol. 01
Blow The House
The Mega Bundle 3.1
Starlight Starbright (DJ Edit)
S3RL Remix EP 13
Like This (DJ Edit)
Public Service Announcement (DJ Edit)
Future Hardcore Classics Vol. 15
Who's Got The Stamina?!, Vol. 1
It's This Again (The Watchmen Radio Mix)
Hard Dance Anthems, Vol. 08
Hardcore Addiction 4
Hard Dance Anthems, Vol. 02
Bass Slut (Alex BassJunkie & Riche Remix)
The Perfect Rave (DJ Edit)
Scary Movie
Mr Vain
Intensify (DJ Edit)
Chillcore (DJ Edit)
It's This Again (The Watchmen Remix)
The Archives, Vol. 1
Fan Service (DJ Edit)
Breaking Boundaries 2019 Revamped Release
Whirlwind (DJ Edit)
Nostalgic (DJ Edit)
Space-Time
Warehouse Anthems: Hardstyle Vol. 7
Trillium
What Is A DJ? (DJ Edit)
The Thank You Bundle Pack
Catchit (DJ Edit)
Hard Dance Anthems, Vol. 14
Projections Of A Fractured Mind
Planet Rave
S3RL Remix EP 12
The Future Of Hardcore Album Bundle
Self Titled (DJ Edit)
Genre Police (DJ Edit)
Hard Dance Bangers, Vol. 01
Calls To Heaven (S3RL Remix)
Dealer (NeoQor Remix)
Sek-C Raver (Maxi Malone Remix)
The July Selection
Hard Dance Anthems, Vol. 13
The Future Of Hardcore Album (Exclusive Tracks)
Warehouse Anthems: Hardcore, Vol. 8
Speechless (DJ Edit)
Over The Rainbow (DJ Edit)
Put Your Phones Up (DJ Edit)
Keep On Ravin' Baby (Archari Remix)
Stamina Summer Slammers, Vol. 2
Old Stuff (DJ Edit)
Misleading Title
The Best Of KFA, Vol. 1
Bass Slut (Karlston Khaos & Djay D Remix)
Remastered
Crazy Ass Bitch (Alex BassJunkie & Riche Remix)
The Mello EP
Hard Dance Anthems, Vol. 07
The Legend of Link (DJ Edit)
S3RL Remix EP 10
The Power of Love of Power (DJ Edit)
When I Die (DJ Edit)
Yeah Science (DJ Edit)
S3RL Remix EP 8
Nothing But... Bass, Vol.12
R4V3 B0Y (DJ Edit)
Spoiler Alert
Superhero
Relentless Bundle
Tell Me What You Want (DJ Edit)
I Wanna Stay (DJ Edit)
Hard Dance Anthems, Vol. 05
Warehouse Anthems: Hardcore, Vol. 12
Unforgettable
Metropolis of Massacre
New World Order
Scream
St8ment
Resolute Power
Temper
Out Of The Frame
Up In Smoke
Gotta Be You
Earthquake
Start A Fire
Dance 2 Music (Audiophetamine Edit)
Better Off
Shady People
Desire (Audiophetamine Edit)
Dreams
Parallel Universe
Wild Love
Supercharged
Ain't No Better Life
4AM
Crash & Burn
Angels & Demons (Darren Styles Edit)
Down With The E
Headbanger
Ready 4 The Tweekend
The Dragon
Infinite
Switch
Partystarter
Necronomicon
Just Like That
My Critic Fetish
The Law
MF
Repercussion
The Promqueen's Finest Drugs
Day of Reckoning
Blaze
Rally Of Retribution (Official Dominator 2019 Anthem)
The Driller Killer
Black Hole
HOAX
Crusader
Right Through Your Head
Burn This MF Down
Send Me to Hell
Wiseguy
Nocturnolz
Still a Full Gentle Racket (Angerfist 2019 Refix)
Gates Of Oblivion
From the Blackness
Bare Knuckle Fist
Impact
Commandments
Criminally Insane
Still A Full Gentle Racket
Street Fighter (Audiofreq Remix)
Bogota
Brainfail
The Desecrated
The Heartless
Creed Of Chaos feat. Nolz
Pennywise
Off The Grid
Hustlers
Rally of Retribution (Official Dominator 2019 Anthem)
I Like It Loud (feat. The Ultimate MC)
The Approach
Hoax
Send Me To Hell
From The Ashes
F@cking Wit Yo Head
Gates of Oblivion feat. Nolz
Critter
Bassline Abuser feat. Syco
Primal Instinct
Get It Lit
Number 1
Criminally Insane (Radical Redemption Remix)
Nothing Is Real
Streetfighter
Creed of Chaos (Official Anthem) feat. Nolz
Taking Charge
Krash The Party
Gangsterizm
Overdose Music
Tournament of Tyrants (Official Masters of Hardcore 2018 Anthem) feat. Tha Watcher
Creature
Street Fighter
Coco's Revenge
Acid Bomb
Survive The Street
Shambala
Reckoning
Pussy Lounge 2019
Hardcore Festival Top 100, Vol. 2
Beyond The Lights
Masters In The Mix Vol V - Mixed By Angerfist and F. Noize
This Life Is Lost
Nothing Like The Oldschool
The Qontinent 2018
Vive la Frenchcore Anthem 2017
Defqon.1 2018
Hardcore Vibes, Vol. 1
Trip To Bangladesh
Frenchcore Worldwide 02
10 Years of Gearbox
Reverze 2019 Edge Of Existence
Get It Crackin - The Remixes
Thunderdome Die Hard III
Vengeance
Creme de la Core Album
Frenchcore Worldwide 01
Bad Dreams
Approach To Midnight
Toxicator 2018
Defqon.1 2019
Regeneration
Q-BASE 2018
Leven Is Lijden
Famous In Vegas
Mayday 2019 - When Music Matters
Trip Around The World
Approach To Midnight Sampler 4 - Extended Mixes
Sincere Hate EP
Frenchcore Compilation, Pt. 01
Q-BASE 2017
Harmony of Hardcore 2017
LSD Problem
Thunderdome 25 Years Of Hardcore
Payback time
Call of fury
Laughing Loud E.P.
Hardcore Thunder Megamix, Vol. 3
Fight the power
Clockwork
Project Hardcore 2015
Harmony Of Hardcore 2016
Invincible
The Qontinent 2017
Thunderdome The Golden Series
Legacy of Noize
Syndicate 2017 - Ambassadors in Harder Styles
Rewind
RUDENESS - Hardcore beyond rules
Tales of jealousy
Dogfighter
The future
Game over
Dangerous
Let's get it on
Decibel Outdoor 2015
Out thing e.p. Part 2
A real voice
A night of madness
Where The Sun Never Shines
The Hardest Records In The World (Mixed By Kutski)
Badass
Boom and shake up
Harmony of Hardcore 2013
Thunderdome 25 Years Of Hardcore
Q-BASE 2017
The Qontinent 2016
Decibel outdoor 2017
Nothing else matters
Exterminate - Extended DJ Versions
Good old times
Pussy Lounge 2016
Defqon.1 2016
Decibel 2014
Harmony of Hardcore 2019
Hardcore machine
Hardcore Vibes, Vol. 1
INSANE
Decibel Outdoor 2016
Nasty
Hardcore Festival Top 100, Vol. 1
Hardcore Festival Top 100, Vol. 2
Dedicated to your project
Q-BASE 2014
Q-BASE 2016
Approach To Midnight Sampler 1 - Extended Mixes
Hardcore Thunder Megamix, Vol. 1
Intents Festival 2011 - Hardcore Edition
Thrillogy 2014
Dogfight Hardcore Vol. 1
Revolt 2019
Dogfight
Pussy lounge 2014
Anarchy ep
Project Hardcore #ph14
Harmony of Hardcore 2014
Bass Fusion (100%% Hardcore)
Remixing Project 2 - Thrillseeka
Ama shishi
Thunder-like
Thunderdome Die Hard
Masters In The Mix Vol V - Mixed By Angerfist and F. Noize
Disorder
Bassdrum music
Here comes the madness
New World Order
De Beukplaat 9 - Compiled by Mental Theo
The Qontinent 2019
Approach To Midnight
Embrace The Fire
Till I Die Vol.2
Come Get Some
Agony
Grand Theft Album Pt. 1
#MFFYF
Thrillogy 2012 mixed by Zatox, Crypsis and Mad Dog
Fire
911
Hardcore Thunder Megamix, Vol. 2
Babylon Dead
Syndicate 2019 (Ambassadors in Harder Styles)
Disconnected EP
Maze of Martyr (Official Dominator 2017 anthem)
Defqon.1 2014
Harderz 2013 (Super Hard Bass Mixed By Ronald-V)
Decibel Outdoor 2018
Sick And Twisted
Thunderdome - The Final Exam - 20 Years Of Hardcore
Hardcore World, Vol. 1
Reset
Inner side
Till I Die Vol.1
Dogfight Hardcore Vol.II - Ruthless & Wild
Not my tempo
I love hardcore
Qlimax 2013 Immortal Essence Mixed By Code Black
The apocalypse (Official Unity Anthem 2015)
Hardcore Italia - The propaganda
Rock The Part-E - Dj Mad Dog Extended Remix
The Hardest Records In The World, Vol. 2 (Mixed by Kutski)
Thunderdome Die Hard III
Priests
Pussy Lounge 2017
Keeping The Rave Alive: The Ravers Revolution
Reverze 2014
Maschen-Drat-Zaun
""".split("\n")


class DJBoothChecker(BaseChecker):
    def __init__(self):
        self.port = 7556
        super(DJBoothChecker, self).__init__("DJBooth", 8080, 1, 0, 0)

    async def create_user(self, user, password, addr):
        try:
            reader, writer = await asyncio.open_connection(addr, self.port)
            ret = await reader.readuntil(b": ")
            writer.write(b"r\n")
            await reader.readuntil(b": ")
            writer.write(user.encode() + b"\n")
            await reader.readuntil(b": ")
            writer.write(password.encode() + b"\n")
            writer.close()
        except Exception as e:
            raise BrokenServiceException("Couldn't create the user {}, {}".format(user, e))

    async def login_user(self, user, password, addr):
        try:
            reader, writer = await asyncio.open_connection(addr, self.port)
            ret = await reader.readuntil(b": ")
            writer.write(b"l\n")
            await reader.readuntil(b": ")
            writer.write(user.encode() + b"\n")
            await reader.readuntil(b": ")
            writer.write(password.encode() + b"\n")
            ret = await reader.readline()
            if b"Sorry" in ret:
                raise Exception("Unable to log in as the user {} doesn't exist!".format(user))
            await reader.readuntil(b"? ")

            return reader, writer
        except Exception as e:
            raise BrokenServiceException("Couldn't log in as the user {}, {}".format(user, e))

    async def submit_song(self, reader, writer, song):
        try:
            writer.write(b"a\n")
            await reader.readuntil(b"> ")
            writer.write(song.encode() + b"\n")
            await reader.readuntil(b"? ")
        except Exception as e:
            raise BrokenServiceException("Couldn't submit Song {}, {}".format(song, e))

    async def get_song_list(self, reader, writer):
        try:
            writer.write(b"l\n")
            l = await reader.readuntil(b"\n\n")
            await reader.readuntil(b"? ")
            l = [x.decode().split(") ")[1] for x in l.split(b"\n")]
            return l
        except Exception as e:
            raise BrokenServiceException("Couldn't get the full songlist, {}".format(e))

    async def putflag(self, logger, task, collection):
        try:
            logger.debug("Putting flag {}".format(task.flag))
            self.address = task.address
            tag = ''.join(random.choice(ascii_letters + digits) for _ in range(20))
            user = ''.join(random.choice(ascii_letters + digits) for _ in range(20))
            passw = ''.join(random.choice(ascii_letters + digits) for _ in range(20))

            await collection.insert_one({ 'flag' : task.flag, 'tag': tag , 'user': user, 'password': passw })

            logger.debug("Registering User: {} with Password: {}".format(user, passw))
            await self.create_user(user, passw, task.address)
            logger.debug("Registered User: {}".format(user))

            logger.debug("Putting Flag: {}".format(task.flag))

            logger.debug("Logging in User: {}".format(user))
            reader, writer = await self.login_user(user, passw, task.address)
            logger.debug("Logged in as User: {}".format(user))

            logger.debug("Submitting all the songs")
            selected_songs = [random.choice(songs) for x in range(random.randrange(3, 5))]
            rand_idx = random.randint(0,len(selected_songs)-1)
            selected_songs = selected_songs[:rand_idx] + [task.flag] + selected_songs[rand_idx:]
            for song in selected_songs:
                logger.debug("Submitting song: {} for user {}".format(song, user))
                await self.submit_song(reader, writer, song)
            logger.debug("Done submitting all the songs. Quitting!")

            writer.write(b"q\n")
        except Exception as e:
            raise BrokenServiceException("Failed to put flag: {}, {}".format(task.flag, e))

    async def getflag(self, logger, task, collection):
        try:
            logger.debug("Getting flag {}".format(task.flag))
            data = await collection.find_one({ "flag": task.flag })
            if data is None:
                raise BrokenServiceException("Couldn't retrieve the db for {}".format(task.flag))
            user = data["user"]
            passw = data["password"]

            logger.debug("Logging is as User: {}".format(user))
            reader, writer = await self.login_user(user, passw, task.address)
            logger.debug("Logged is as User: {}".format(user))

            logger.debug("Querying the songs")
            song_list = await self.get_song_list(reader, writer)
            if task.flag not in song_list:
                raise BrokenServiceException("Flag {} not in songlist {}".format(task.flag, song_list))

            writer.write(b"q\n")
        except Exception as e:
            raise BrokenServiceException("Failed to get flag: {}, {}".format(task.flag, e))

    async def putnoise(self, logger, task, collection):
        pass

    async def getnoise(self, logger, task, collection):
        pass

    async def havoc(self, logger, task, collection):
        pass

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ELKFormatter("%(message)s")) #ELK-ready output
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

app = create_app(DJBoothChecker()) # mongodb://mongodb:27017
