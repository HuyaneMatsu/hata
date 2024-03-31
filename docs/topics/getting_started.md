# Getting started

To get started with Discord bots, first you need a discord application and add a bot to it. This tutorial will show to
how to do it.

First go to [Discord developer portal](https://discord.com/developers/applications).

![](assets/getting_started_0000.png)

If you have any applications, or teams, they will show up here.

To create one application click on `New Application`, name it and `Create`.

![](assets/getting_started_0001.png)

When the application is created, click on the `Bot`.

![](assets/getting_started_0012.png)

To authorize the bot with Discord you will need its token. To get the token, we have to `reset` it.

![](assets/getting_started_0015.png)

> The token is like your password, do not give it away. Anyone with it can log into your bot.

Turn on `Public bot` check. Even tho it enables others too to add the bot, it also allows you for easier installation.

![](assets/getting_started_0021.png)

Before moving forward, I also recommend checking out privilege intents. Since they limit what bots can access.

You can find them on the bot tab a little bit down.

![](assets/getting_started_0007.gif)

# Inviting your bot

To invite to a guild, first you need a bot invite.

To generate one for your bot, go to the `Installation` tab.

![](assets/getting_started_0013.png)

![](assets/getting_started_0017.png)

First turn on `user install`, this enables the bot to not only be invited to a guild, but will allow its command
to be integrated with users.

Now select `Discord provided Link` in the `Install Link` section. This allows us to configure how the bot is verified.

![](assets/getting_started_0019.png)

Add extra `bot` scope in `Guild Install` section.

![](assets/getting_started_0020.png)

Copy the url and paste it into your browser.

![](assets/getting_started_0022.png)

Click on `Add to Server`.

![](assets/getting_started_0011.png)

Select a guild to add the bot into and click `Authorize`.

> Your account needs `Manage Server` permission in order to add a bot to it.

Now that you have your bot, you can start writing your bot.

# Writing your bot

There are many libraries interacting with the Discord API. Most bot developers stick with the same library for their
whole career, so checking out multiple ones and making a choice, which satisfies needs is highly recommended.

Or if you are enough hardcore to make your own, or you are just curious, check out
[Discord's official documentation](https://discord.com/developers/docs/intro).

----

<p align="right">
    <a href="./introduction_to_python.md">Next up: Introduction to Python</a>
</p>
