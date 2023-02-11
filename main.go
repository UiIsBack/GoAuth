package main

import (
	"bytes"
	"fmt"
	"encoding/json"
		"net/http"
		"io/ioutil"
	"github.com/gin-gonic/gin"
	"os"
)


const guild_id = "1071829849766895677"
const bot_token = "MTA3MzkxMzgxMTUwNzA5MzU2Ng.GXJHc7.g2sZ3W0-s7xVBE7Ewa_9kkIiqzsVlAvSmZ4Ngw"
const api_endpoint = "https://discord.com/api/v8";
const sec = "Rqpq5LCFDdQW5SR1sOiGGn9xHuSkgH5o";
const client_id = "1073913811507093566";
const redirect = "http://localhost:8080/callback"
const role_id = "1073978795549274254"
const grant = "authorization_code"
type DiscordToken struct {
	AccessToken string `json:"access_token"`
}




func assignRole(userID string, roleID string, botToken string) error {
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

	if resp.StatusCode != http.StatusNoContent {
		body, _ := ioutil.ReadAll(resp.Body)
		return fmt.Errorf("Assigning role failed with status code %d: %s", resp.StatusCode, string(body))
	}

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

	ff[data["id"].(string)] = data

	file.Truncate(0)
	file.Seek(0, 0)

	err = json.NewEncoder(file).Encode(ff)
	if err != nil {
		return err
	}

	return nil
}
func main() {
	
	var url = "https://discord.com/api/oauth2/authorize?client_id=" + client_id + "&redirect_uri=" + redirect + "&response_type=code&scope=identify%20guilds%20email%20guilds.join"

	r := gin.Default()
	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"url": url,
		})
	})
	r.GET("/callback", func(c *gin.Context) {

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

		data1, err1 := getUserData(token)
		if err1 != nil {
			fmt.Println(err1)
			return
		}
		var mn = data1["id"]
		fmt.Println(data1["id"])
		err = saveData("saved.json", data1)
		if err != nil {
			fmt.Println(err)
			return
		}
		mn, ok := mn.(string)
if !ok {
    // handle error
}		
fmt.Println(mn)
		err2 := assignRole(mn.(string), role_id, bot_token)
		if err1 != nil {
			fmt.Println(err2)
			return
		}
		c.JSON(200, gin.H{
			"status": "verified",
		})
	})

	r.Run()
}