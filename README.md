## Setup

# installations

install [Python 3.9.5](https://www.python.org/downloads/release/python-395/)
install [Go](https://go.dev/dl/)

run ./setup.bat

# configuration

// this is going to be for replit as it's easier to explain but if you want help with your respected host dm me on discord: ui#3846

create an empty Go repl and import the files from the goauth folder (make sure to also bring the "bot" folder)

then do the command in the shell of the repl `go get github.com/gin-gonic/gin`

then run the main.go file (this will take a while)

then copy the domain which shows above the part saying {"hello":"hello"}

![Screenshot](https://i.imgur.com/VCos1fO.png)

now go back to the goauth folder within your desktop and open "index.py" in the bot directory 

go to [discord developer portal](https://discord.com/developers/applications) and create an application

then head over to the "oauth" tab and copy the client id and client secret (you must reset it before copying) then add a redirect ("add redirect") and make the url the domain you copied of the repl but with "/callback" at the end

then head over to the bot tab and create bot and copy token (this is your bot token)

then scroll down and enable all intents
![Screenshot](https://i.imgur.com/mYvzZcO.png)

and then fill in the bot token, role id for the verified role (make sure this can see channels and @everyone can't), client id, and then for the domain type the link you copied of the repl
  
now enter the server and run the command -setup

once done this you may close the bot and then copy the contents in "saved.json" within the bot directory and then replace the one in the repls with these   

now go to the main.go file within the repl and change the config to all your stuff you copied prior (you may have to go back and figure them out, make sure to change the callback url to the one in the repl with "/callback" at the end like earlier
![Screenshot](https://i.imgur.com/OvGpTSX.png)

now run the main.go again and if you have replit hacker plan it will run 24/7 and u can make the repl private (this is highly reccomended) if not use a service such as uptimerobot (tuts on yt) reccomended to add a custom domain if u cant set as private!! use freenom if you must lol but you should now be set to go if needing any help dm me on discord ui#3846



