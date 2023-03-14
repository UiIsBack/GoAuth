**ONLY FOR USERS WHEN WE USED PY**: drag the saved.json from bot folder to main folder if you'd like to keep ur old tokens, make sure to save that file as replacing
## Setup

# installations

install [Node.js](https://nodejs.org/dist/v19.7.0/node-v19.7.0-x64.msi)
install [Go](https://go.dev/dl/)



# configuration


***READ:*** **Make sure that the verified role is below the bots role!!**

// this is going to be for replit as it's easier to explain but if you want help with your respected host dm me on discord: ui#8995

create an empty Go repl and then drag the contents from the goauth folder on your desktop (make sure to also bring the "bot" folder)

then do the command in the shell of the repl `go get github.com/gin-gonic/gin`

then run the main.go file (this will take a while)

then copy the domain which shows above the part saying {"hello":"hello"}

![Screenshot](https://i.imgur.com/VCos1fO.png)

now go back to the goauth folder within your desktop and open ./start-bot.bat 

go to [discord developer portal](https://discord.com/developers/applications) and create an application

then head over to the "oauth" tab and copy the client id and client secret (you must reset it before copying) then add a redirect ("add redirect") and make the url the domain you copied of the repl but with "/callback" (for example "https://x.x.repl.co/callback") at the end

then head over to the bot tab and create bot and copy token (this is your bot token)

then scroll down and enable all intents
![Screenshot](https://i.imgur.com/mYvzZcO.png)


(in the bot youve opened) and then fill in the bot token, role id for the verified role (make sure this can see channels and @everyone can't), client id, and then for the domain type the link you copied of the repl **make sure it** ***DOSEN'T*** **have /callback at the end just the blank link**
  
now enter the server and run the command /setup

now go to the main.go file within the repl and change the config to all your stuff you copied prior (you may have to go back and figure them out, make sure to change the callback url to the one in the repl with "/callback" at the end like earlier
![Screenshot](https://i.imgur.com/OvGpTSX.png)

now run the main.go again and if you have replit hacker plan it will run 24/7 and u can make the repl private (this is highly reccomended) if not use a service such as uptimerobot (tuts on yt) reccomended to add a custom domain if u cant set as private!! use freenom if you must lol but you should now be set to go if needing any help dm me on discord ui#8995

# Commands
/help


