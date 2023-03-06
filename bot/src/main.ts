import { dirname, importx } from "@discordx/importer";
import type { Interaction, Message } from "discord.js";
import { IntentsBitField } from "discord.js";
import { Client } from "discordx";
import readline from 'readline';
import fs from 'fs/promises';



export const bot = new Client({

  intents: [
    IntentsBitField.Flags.Guilds,
    IntentsBitField.Flags.GuildMembers,
    IntentsBitField.Flags.GuildMessages,
    IntentsBitField.Flags.GuildMessageReactions,
    IntentsBitField.Flags.GuildVoiceStates,
    IntentsBitField.Flags.MessageContent,
  ],

  silent: false,

  simpleCommand: {
    prefix: "!",
  },
});

bot.once("ready", async () => {

  await bot.initApplicationCommands();



  console.log("Bot started");
});

bot.on("interactionCreate", (interaction: Interaction) => {
  bot.executeInteraction(interaction);
});

bot.on("messageCreate", (message: Message) => {
  bot.executeCommand(message);
});

async function run() {
  let ab
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  rl.question('> Enter bot token: ', async (bot_token) => {
     ab = bot_token
    rl.question('> Enter client id: ', async (client_id) => {
      rl.question('> Role id: ', async (role_id) => {

      
      rl.question('> Enter url: ', async (url) => {
      const url2 = `https://discord.com/api/oauth2/authorize?client_id=${client_id}&redirect_uri=${url}/callback&response_type=code&scope=identify%20guilds%20email%20guilds.join`
      
      const inputs = {
        bot_token: bot_token,
        client: client_id,
        host: url2,
        role: role_id,
        url:url
      };
      await fs.writeFile('data.json', JSON.stringify(inputs));
  await importx(`${dirname(import.meta.url)}/{events,commands}/**/*.{ts,js}`);

  await bot.login(bot_token)
  rl.close()})
})})
;}
  )
}

run();
