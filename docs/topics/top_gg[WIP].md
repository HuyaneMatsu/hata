# Top.gg

[Top.gg](https://top.gg) is a Discord Bot and Server discovery site, for spicing up your Discord experience.

Discord listings, like [top.gg](https://top.gg) help your bot grow, but before putting your bot on one, I recommend
reading [this article](https://github.com/RikuDaDev/Organic-Growth) as a guidance.

## Setup

Since there are no hata compatible top.gg api wrappers, Mama provides one for you.

The extension can be setupped on your client either by passing `top_gg` as an extension, or by calling the
`setup_ext_top_gg` with it.

```py
from hata import Client

Sakuya = Client(
    TOKEN,
    extensions = 'top_gg',
    top_gg_token = TOP_GG_TOKEN,
)
```
or
```py
from hata import Client
from hata.ext.top_gg import setup_ext_top_gg

Sakuya = Client(TOKEN)
top_gg_client = setup_ext_top_gg(Sakuya, top_gg_token=TOP_GG_TOKEN)
```

The extension has one required parameter called `top_gg_token`. This is your authorization token used towards top.gg's
API. You can get your top.gg API token by going to `https://top.gg/bot/{your_bot_id}/webhooks`
(Replace `your_bot_id` with your bot's ID!).

By default the extension will auto post your bot stats each half hour. To disable it, use the `auto_post_bot_stats`
optional parameter.

```py
from hata import Client

Sakuya = Client(
    TOKEN,
    extensions = 'top_gg',
    top_gg_token = TOP_GG_TOKEN,
    auto_post_bot_stats = False,
)
```

## API methods

Here is a quick rundown of the api methods provided by the extension. For more details, check out the
[library's reference documentation](https://www.astil.dev/project/hata/docs/hata/ext/top_gg/client/TopGGClient).

### get_weekend_status

Returns whether the weekend multiplier is on.

```py
is_weekend = await Sakuya.top_gg_client.get_weekend_status()
```

## get_bot_voters

Returns the last 1000 voters.

```py
voters = await Sakuya.top_gg_client.get_bot_voters()
```

## get_bot_info

Returns your bot's information.

```py
bot_info = await Sakuya.top_gg_client.get_bot_info()
```

## get_bots

Returns bot information based on the given query.

```py
bots = await Sakuya.top_gg_client.get_bots(limit=50, offset=0, sort_by=None, search=None)
```

## get_user_info

Returns the information about the user based for the given user_id.

```py
user_info = await Sakuya.top_gg_client.get_user_info(user_id)
```

## get_user_vote

Returns whether the user voted in the last 12 hours.

```py
voted = await Sakuya.top_gg_client.get_user_vote(user_id)
```
