# LiveTweeter

[![development status | 6 - mature](https://img.shields.io/badge/development_status-6_--_mature-green)](https://pypi.org/classifiers/)
[![license: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![release](https://img.shields.io/github/v/release/PatchaIT/LiveTweeter)
<!--[![next](https://img.shields.io/badge/next-v1.4.2-orange)](https://github.com/PatchaIT/LiveTweeter/tree/LiveTweeter_v1.4.2)-->
<!--[![code style: pep-0008](https://img.shields.io/badge/code_style-pep--0008-FFF8FF)](https://peps.python.org/pep-0008/)-->

(On your Streamlabs Chatbot) Tweets when you are going live!.

## Table of Contents

* [About the Project](#about-the-project)
  * [Warning Notes](#warning-notes)
* [In Shorts](#in-shorts)
* [Changelog](#changelog)
  * [Versions by Wellbrained BurnySc2](#versions-by-wellbrained-burnysc2)
  * [Versions by Patcha](#versions-by-patcha)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Settings](#settings)
* [Optional Workarounds](#optional-workarounds)
* [Credits](#credits)

## About The Project

Hi all,
  due to new free API versions and restricting rules on X platform
  (formely Twitter), most auto-tweeting bots stopped supporting such kind of
  feature, so it's necessary to adopt a personal solution, working with
  personal account's limits.

For that purpose, a configurable script like LiveTweeter was perfect to face
  this necessity, but it was too dated and needed updating.

You can find the original there:
  [2018 wellbrained and BurnySc2 LiveTweeter script for Streamlabs Chatbot
    (formely Ankhbot)](https://github.com/BurnySc2/Ankhbot-Scripts-DevBranch/tree/master/LiveTweeter).

In here you'll find my edited version, implementing the necessary to make
  this script be usable again.

Enjoy.

### Warning Notes

Note:
  Youtube support without variables and OnGameChange detection.

## In Shorts

* Script: LiveTweeter
* Version: 1.4.2
* Description: Automatically Tweets when going Live
* Change: Twitter API 2.0 + "periodical" and "on game change" tweets fixes
* Services: Twitch, Youtube
* Overlays: None
* Made by: @BuRny, @Brain
* Updated by: @Patcha_it
* Tested by: @Mackdanny

## Changelog

### Versions by Wellbrained BurnySc2

(Some dates are estimates)

* 2018/01/06 v1.0.0
  * First Release version
* 2018/02/06 v1.0.1
  * Fixed the usage of paths with spaces in it  
  * Trimming user informations now to prevent errors with spaces
* 2018/02/16 v1.0.2
  * Disabled send-tweet button when the script is not enabled
  * Attempt to fix unicode characters
* 2018/03/06 v1.1.0
  * Changed methods to support Chatbot .29+ versions
* 2018/03/16 v1.1.1
  * Emojis are now supported
* 2018/07/10 v1.2.0
  * Way better error logging
      (detection if python path or keys were incorrectly entered)
  * Added logs when $game and $title could not be replaced
  * Chatbot Logs entry: User information on whose timeline was posted
  * "Install pip requests" command window stays open after the installation
      finished (so errors can be tracked down if any occured)
  * Saves script status to file in case of Streamlabs Chatbot restart during
      the stream to prevent a new automatic tweet
  * Added a $preview variable for twitch users - contains a link to a preview
      image to the stream
  * Emojis are now supported
  * (optional) sends a new tweet when the streamer started playing a different
      game (tweet on game change), added a new text file for this feature
      (Tweet_OnGameChange.txt)
  * (optional) sends new tweet when some time (30-300 minutes) has passed
      since the stream went live, added a new text file for this feature
      (Tweet_Periodic.txt)

### Versions by Patcha

* 2024/04/20 v1.3.5
  * Supports Twitter API v2.0 Free Endpoints, with API v1.1 login
  * (optional) enter your Streaming Channel Name, as workaround for BOT issue
      on retrieving Channel Name by itself sometimes
  * (optional) enter your Twitter Channel Name, as workaround for
      Twitter Free API v2.0 limits or errors
* 2024/04/28 v1.4.0
  * Channels name options moved in a dedicated options section
  * (optional) option to force using the Streaming Channel Name setted into
      options, without trying to get it at runtime
  * (optional) option to force using the Twitter Channel Name setted into
      options, without trying to get it via API
  * Added a button which allows to reset current saved Twitter Channel Name
    (in case you changed it or if you prefer to use the one you just
      setted into options)
  * Added current time to info logs
  * Added an option to make script wait a certain amount of second before
      actually sending a new tweet.
    If stream goes offline during countdown, the counter will reset.
      Unless the setted amount of time to result offline will pass meantime.
* 2024/05/04 v1.4.1
  * Current time in info logs now have always two digits even for unities.
* 2024/06/04 v1.4.2
  * Resolved an issued with periodical tweet sent even while there was already
      another tweet triggered
  * Resolved an issue from 1.2.0 where "periodical" tweet text could be
      replaced by "on game change" tweet text and vice versa
  * Renamed "Channel names" section into "Optional workarounds",
      to host more workaround solutions
  * Optional workarounds are better explained into a dedicated section
      at the bottom of this ReadMe file
  * Added an optional text to use in case obtaining the actual current
      livestream's title fails
  * Added an optional text to use in case obtaining the actual current
      game's name fails
  * Added an optional visa to enable/disable `Quick Message for Tweet File`
      field text to be used
      (i.e.: in case you use `Quick Message` only for test purposes)

## Getting Started

### Prerequisites

Have an installation of Streamlabs Chatbot, already logged in to your accounts.

* [Download Streamlabs Chatbot](https://streamlabs.com/desktop-chatbot)

Follow this tutorial to prepare your Streamlabs Chatbot installation to accept scripts.

* [[Streamlabs Chatbot] Scripts Explained by Castorr91](https://www.youtube.com/watch?v=l3FBpY-0880)

### Installation

1. Download the latest version of the script.
2. If you haven't already, open your Streamlabs Chatbot and log in to your
  Streamer and Bot accounts.
3. On the left side, wait for the `Scripts` tab to pop up and click it.
4. On the top right corner of the window, next to the reload button is an
  import script button (Arrow pointing right to a box) and select the script
  downloaded before.
5. You will receive a message box confirming the import, accept it.
6. The window will update and show the `LiveTweeter` script.
7. Click on the `LiveTweeter` name to see the configuration pane.

## Settings

1. Into script's settings, expand `User information (keep it hidden)`
      section and enter the path to your default Python27 directory
      with python.exe (per default: `C:/Python27/python.exe`)
      into `Python Path` field.

    Click the `Install PIP Requests` button to install necessary libraries.

    Note:  
      In case you didn't install PIP with the Python installation
        follow this guide:
        [PIP Installation Doc](https://pip.pypa.io/en/stable/installation/)

      Or just install the Python27 again with the function enabled.

2. Click the `Register Twitter App` button.
    Create a Project and an App linked to it, you can fill in whatever
      you want.

    An example:

      `Name: SL Chatbot - LiveTweet`  
      `Description: SL Chatbot - LiveTweet`  
      `Website: https://www.twitch.tv/<yourTwitchName>`  
      `Callback URL: https://www.twitch.tv/<yourTwitchName>`

3. After creation go to the `Keys and Access Tokens` tab and press the button
      to create the Access information.
    Copy paste the necessary four tokens into Chatbot:

    `Consumer Key + Secret`  
    `Access Token + Secret`

    With this you'll give Chatbot the permission to send out Tweets
      in your stead.

## Optional Workarounds

I'm making this section, to better explain some of the workaround options
  I added to the script.

Seeing that they could appear a bit confusing at first look.

Just remember that if you hold your mouse over an option into chatbot script
  settings, it will popup an explaining tooltip for your help.

> ### Streaming Channel Name [textbox]

  This text field, lets you directly declare your Streaming channel name,
    Twich or Youtube.

  Usually the script is able to obtain by itself the channel name by using
    some chatbot libraries.
  Unluckily there's a bug where as soon as the chatbot is started, its
    libraries fail to obtain the channel name correctly.
  
  You can workaround this manually, by going into the Scripts section
    of the chatbot and refresh scripts (using the circle arrouw icon button
    on the top left).
  And this would resolve the issue for ALL those scripts which try to obtain
    the channel name from the chatbot.

  Otherwise you can fill this field with your Streaming Channel Name,
    and the script will use this name every time it seems that the chatbot
    failed to obtain the name by itself.

> ### Force Streaming Channel Name [checkbox]

  As mentioned talking about Streaming Channel Name, that option is supposed
    to be adopted only if the chatbot fails to obtain the channel name
    by itself on runtime.

  Anyway, if you flag this checkbox, it will stop trying to achieve it
    by itself on runtime, and instead it will start to always adopt the
    channel name you wrote into Streaming Channel Name field.
  If you do so, please remember to update your channel name in case
    you'd change it on your streaming platform.

> ### Generic livestream title [textbox]

  If you didn't use `Streaming Channel Name` optinal field (and/or
   `Force Streaming Channel Name` option), sometimes the script could
    fail trying to get the Streaming channel name from chabot libraries.
  But if it fails, if would also fail to obtain the current livestream's title
    of your streaming, from Twich API.
  Because to do this, it needs your correct Twitch channel name.
  
  This could make a text like `A channel name has to be specified.`
    appear instead of the livestream title into your Tweets.
  If you want to prevent this by applying another text,
    you can specify that text here.

> ### Generic game name [textbox]

  If you didn't use `Streaming Channel Name` optinal field (and/or
    `Force Streaming Channel Name` option), the script will try to get
    the name from chabot libraries.
  But if it fails, if would also fail to obtain the current game's name
    you're streaming, from Twich API.
  Because to do this, it need your correct Twitch channel name.

  This could make a text like `A channel name has to be specified.`
    appear instead of the game name into your Tweets.
  If you want to prevent this by applying another text,
    you can specify that text here.

> ### Twitter Channel Name [textbox]

  This text field, lets you directly declare your Twitter channel name.
  Usually the script would obtain it by itself contacting Twitter API.
  This uses to work fine, unless you consumed all API call your account
    can perform.

  In case the script fails to obtain your Twitter channel name via API,
    if you filled this optional field, it will automatically use the name
    you wrote in there.

> ### Force Twitter Channel Name [checkbox]

  As mentioned talking about Twitter Channel Name, that option is supposed
    to be adopted only if the chatbot fails to obtain the channel name
    by itself with a Twitter API call.
  But if you have a free Twitter API account, this would consume a call
    to those API.
  
  It's also important to undeline, that the script will do this only once,
  then save the name into a file, also for next sessions.
  So potentially it's not a great issue.
  
  Anyway, if you flag this check, it will stop trying to achieve it
    by API call, and instead it will start to always adopt the channel name
    you wrote into Twitter Channel Name field.
  If you do so, please remember to update your channel name in case
    you'd change it on your streaming platform, after doing so, you'll surely
    need to use the button I'll describe now.

> ### Reset Twitch Channel Name [button]

  As mentioned before, to not abuse Free Twitter API calls countdown,
    as soon as the script succeed to achieve a Twitter channel name, it
    will be stored into a text file and reused each time the chatbot restart.
  This could became an issue in case you'll need to change your
    Twitter channel name.

  It is actually important to underline that a link with the corret Tweet ID
    will always work even if the channel could result wrong.
  But probably you'll not want the wrong/old channel name to be used
    in your chat links.

  That's where this button find its utility: it will clean the old
    Twitter channel name from script's memory and store text file,
    and force it to try to get the new name.
  If you activated the `Force Twitter Channel Name` check, the new name
    will be obtained from the dedicated text option we explained before:
    `Twitter Channel Name`.
  Otherwise the script will send a new Twitter API call to get current name.

## Credits

[Brain - Twitch](www.twitch.tv/wellbrained)  
[Burny - Twitch](www.twitch.tv/burnysc2)
