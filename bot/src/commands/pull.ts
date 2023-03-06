import { Attachment, CommandInteraction, Embed, EmbedBuilder } from "discord.js";
import { ApplicationCommandOptionType, } from "discord.js";
import fs from 'fs';
import { Discord, MetadataStorage, Slash, SlashOption } from "discordx";
import { title } from "process";
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
  @Slash({ description: "pull" })
  pull(
    

    @SlashOption({
      description: "access token",
      name: "oauth_token",
      required: true,
      type: ApplicationCommandOptionType.String,
    })
    @SlashOption({
      description: "guild id",
      name: "guild_id",
      required: true,
      type: ApplicationCommandOptionType.String,
    })

    @SlashOption({
      description: "user id",
      name: "user_id",
      required: true,
      type: ApplicationCommandOptionType.String,
    })
    
    oauth_token: string,
    guild_id: string, 
    user_id: string,
    interaction: CommandInteraction,
    
        
  ): void {
    const jsonString = fs.readFileSync('data.json', 'utf-8');

    const embed = new EmbedBuilder()
    .setFooter({ text: `https://github.com/uiisback/goauth - if u paid u got scammed` })
    .setTitle("**Pull info**")
    .addFields({
      name: "Starting pull",
      value: `
      **user**: <@${user_id}>
      **guild**: ${guild_id}
      **status**: starting...
      **time taken**: null
      `,
    })

    interaction.reply({ embeds: [embed] }).then(rr => {
      const config = JSON.parse(jsonString);

    let r = pull_to_guild(config.bot_token, oauth_token, guild_id, user_id)
    console.log(r)
    const embed2 = new EmbedBuilder()
    .setFooter({ text: `https://github.com/uiisback/goauth - if u paid u got scammed` })
    .setFields({
      name:"Pull finished",
      value: `
      **user**: <@${user_id}>
      **guild**: ${guild_id}
      **status**: done
      **time taken**: null
      `,
    })

    interaction.editReply({embeds: [embed2]})})
  }
}