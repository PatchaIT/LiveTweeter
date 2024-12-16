# TheRenewTTS

[![development status | 7 - inactive](https://img.shields.io/badge/development_status-7_--_inactive-orange)](https://pypi.org/classifiers/)
[![license: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![release](https://img.shields.io/github/v/release/PatchaIT/LiveTweeter)
[![next](https://img.shields.io/badge/next-v1.3.5-orange)](https://github.com/PatchaIT/LiveTweeter/tree/LiveTweeter_v1.3.5)
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
* [Credits](#credits)

## About The Project

Hi all,
  due to new free API versions and restricting rules on X platform
  (formely Twitter), most auto-tweeting bots stopped supporting such kind of
  feature, so it's necessary to adopt a personal solution, working with
  personal account's limits.

For that purpose, a configurable script like LiveTweeter was perfect to face
  this necessity, but it was too dated and needed updating.

You can find the original here:
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
* Version: 1.3.5
* Description: Automatically Tweets when going Live
* Change: Supports Twitter API v2.0 Free Endpoints, with API v1.1 login
* Services: Twitch, Youtube
* Overlays: None
* Made by: @BuRny, @Brain
* Edited by: @Patcha_it (from 1.3.5)

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
  * Way better error logging (detection if python path or keys were incorrectly entered)
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
  * (optional) enter your Streaming Channel Name, as workaround for BOT issue on retrieving Channel Name by itself sometimes
  * (optional) enter your Twitter Channel Name, as workaround for Twitter Free API v2.0 limits or errors

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

## Credits

[Brain - Twitch](www.twitch.tv/wellbrained)  
[Burny - Twitch](www.twitch.tv/burnysc2)
