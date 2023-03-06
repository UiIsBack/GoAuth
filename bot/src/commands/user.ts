import { Attachment, CommandInteraction, Embed, EmbedBuilder } from "discord.js";
import { ApplicationCommandOptionType, } from "discord.js";

import { Discord, MetadataStorage, Slash, SlashOption } from "discordx";
@Discord()
export class Example {
  @Slash({ description: "user info" })
 async  user(

    @SlashOption({
      description: "token",
      name: "access_token",
      required: true,
      type: ApplicationCommandOptionType.String,
    })



    access_token: string,
    interaction: CommandInteraction,
    
        
  ): Promise<void> {
    const headers = {
        Authorization: `Bearer ${access_token}`,
      };
    
      const req = await fetch('https://discord.com/api/v8/users/@me', {
        headers,
      })
      const res = await req.json(

      )
      const embed = new EmbedBuilder()
      .setFooter({text: `https://github.com/uiisback/goauth - if u paid u got scammed`})
      .setTitle("**User info**")
      .setFields({
        name:res['username'],
        value:`
        **id**: *${res['id']}*
        **verified**: *${res['verified']}*
        **2fa**: *${res['mfa_enabled']}*
        `
      })
        
    
          interaction.reply({embeds: [embed]});
        }}
