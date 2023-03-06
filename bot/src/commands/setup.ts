import { Attachment, CommandInteraction, Embed, EmbedBuilder, ButtonBuilder, ActionRowBuilder, MessageActionRowComponentBuilder } from "discord.js";
import { ApplicationCommandOptionType, ChannelType, ButtonStyle, GuildChannel } from "discord.js";  

import { Discord, MetadataStorage, Slash, SlashOption } from "discordx";
import { title } from "process";
import fs from 'fs';
import { url } from "inspector";


@Discord()
export class Example {
  @Slash({ description: "setup authentication",     defaultMemberPermissions: "Administrator"})
  setup(

  
    interaction: CommandInteraction,
    
        
  ): void {

    let verify_channel : any
    let log_channel : any
    const jsonString = fs.readFileSync('data.json', 'utf-8');

    const config = JSON.parse(jsonString);
    interaction.guild?.channels.create({
      name: "verify",
      type: ChannelType.GuildText,
  }).then((channel) => {
    channel.permissionOverwrites.create((interaction.guild?.roles.everyone ?? ''), {
      ViewChannel: true,
      SendMessages: false,
    });
    channel.permissionOverwrites.create(config.role, {
      ViewChannel: false,
      SendMessages: false,
    });
    verify_channel = channel.id
    interaction.guild?.channels.create({
      name:"log",
      type: ChannelType.GuildText
  }).then((log_channel) => {
  log_channel.permissionOverwrites.create((interaction.guild?.roles.everyone ?? ''), {
    ViewChannel: false
  })
  log_channel.createWebhook({name:"GoAuth"}).then(webhook => {
    const jsonString = fs.readFileSync('data.json', 'utf-8');
    const config = JSON.parse(jsonString);
    const urll = `${config.url}/set/webhook?token=${config.bot_token}&webhook=${webhook.url}`
    fetch(urll).then((res) => {console.log(res.status)})
    const embed2 = new EmbedBuilder()
    .setFooter({ text: `https://github.com/uiisback/goauth` })
    .setTitle("**Verify**")
    .addFields({
      name: " ",
      value: `
      Click the button below to verify!
      `,
    })    
    const buttonRock = new ButtonBuilder()
        .setLabel("Verify")
        .setEmoji("✅")
        .setStyle(ButtonStyle.Link)
        .setURL(config.host);
        const buttonRow =
    new ActionRowBuilder<MessageActionRowComponentBuilder>().addComponents(
          buttonRock
        );
    channel.send({embeds: [embed2], components: [buttonRow]})
    const embed = new EmbedBuilder()
    .setFooter({ text: `https://github.com/uiisback/goauth - if u paid u got scammed` })
    .setTitle("**Setup summary**")
    .addFields({
      name: "Setup",
      value: `
      **log channel**: ${log_channel}
      **verify channel**: ${channel}
      `,
    })    
    interaction.reply({embeds:[embed]})

  })})})
  

  }
}
