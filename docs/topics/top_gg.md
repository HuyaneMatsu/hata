# Introduction

[Top.gg](https://top.gg) is a Discord Bot and Server discovery site, for spicing up your Discord experience.

Discord bot listings, like [top.gg](https://top.gg) help your bot grow, but before putting your bot on one, I recommend
reading [this article](https://github.com/KusaDaDev/Organic-Growth) as a guidance.

# Setup

Since there are no hata compatible top.gg api wrappers, Mama provides one for you.

The extension can be setupped on your client either by passing `top_gg` as an extension, or by calling the
`setup_ext_top_gg` with it.

```py3
from hata import Client

Sakuya = Client(
    TOKEN,
    extensions = 'top_gg',
    top_gg_token = TOP_GG_TOKEN,
)
```
or
```py3
from hata import Client
from hata.ext.top_gg import setup_ext_top_gg

Sakuya = Client(TOKEN)
top_gg_client = setup_ext_top_gg(Sakuya, top_gg_token = TOP_GG_TOKEN)
```

## Parameters

The extension has one required parameter called `top_gg_token`. This is your authorization token used towards top.gg's
API. You can get your top.gg API token by going to `https://top.gg/bot/{your_bot_id}/webhooks`
(Replace `your_bot_id` with your bot's ID!).

### auto_post_bot_stats

By default the extension will auto post your bot stats each half hour. To disable it, use the `auto_post_bot_stats`
optional parameter.

```py3
from hata import Client

Sakuya = Client(
    TOKEN,
    extensions = 'top_gg',
    top_gg_token = TOP_GG_TOKEN,
    auto_post_bot_stats = False,
)
```

### raise_on_top_gg_global_rate_limit

Since `top.gg` has long global rate limits, you can turn off waiting for it (if hit for some weird reason). To do it,
pass the `raise_on_top_gg_global_rate_limit` parameter as `True`.

```py3
from hata import Client

Sakuya = Client(
    TOKEN,
    extensions = 'top_gg',
    top_gg_token = TOP_GG_TOKEN,
    raise_on_top_gg_global_rate_limit = True,
)
```

After passing it, you will get a ``TopGGGloballyRateLimited`` whenever the client is globally rate limited.
```py3
from hata.ext.top_gg import TopGGGloballyRateLimited

try:
    bot_info = await client.top_gg.get_bot_info()
except TopGGGloballyRateLimited:
    # global limit hit
    pass
```

# API methods

Here is a quick rundown of the api methods provided by the extension. For more details, check out the
[library's reference documentation](https://www.astil.dev/project/hata/docs/hata/ext/top_gg/client/TopGGClient).

## get_weekend_status

Returns whether the weekend multiplier is on.

```py3
is_weekend = await Sakuya.top_gg.get_weekend_status()
```

## get_bot_voters

Returns the last 1000 voters.

```py3
voters = await Sakuya.top_gg.get_bot_voters()
```

## get_bot_info

Returns your bot's information.

```py3
bot_info = await Sakuya.top_gg.get_bot_info()
```

## get_bots

Returns bot information based on the given query.

```py3
bots = await Sakuya.top_gg.get_bots(limit=50, offset=0, sort_by=None, search=None)
```

`sort_by` fields and `search` field's keys might be the following:

- banner_url
- certified_at
- discriminator
- donate_bot_guild_id
- featured_guild_ids
- github_url
- id
- invite_url
- is_certified
- long_description
- name
- owner_id
- owner_ids
- prefix
- short_description
- support_server_invite_url
- tags
- upvotes
- upvotes_monthly
- vanity_url
- website_url

## get_user_info

Returns the information about the user.

```py3
user_info = await Sakuya.top_gg.get_user_info(user_id)
```

## get_user_vote

Returns whether the user voted in the last 12 hours.

```py3
voted = await Sakuya.top_gg.get_user_vote(user_id)
```

# Webhook

You might configure your bot on `top.gg` to send a webhooks to your web server. After setting your url and
authorization, you are ready to define your vote route.

Here is a minimal [flask](https://flask.palletsprojects.com/en/2.0.x/) example, showing how to:

```py3
from flask import Flask, Response, abort, request
from hata.ext.top_gg import BotVote

AUTHORIZATION = ''

app = Flask(__name__)

@app.route('/vote', methods=['POST'])
def vote():
    authorization = request.headers.get('Authorization', '')
    if authorization != AUTHORIZATION:
        abort(401)
    
    bot_vote = BotVote.from_data(request.json)
    # Do things
    
    return Response(status=200)

app.run()
```
