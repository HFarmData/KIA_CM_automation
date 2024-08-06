# KIA_CM_automation

## Repository's Purpose
The purpose of this repository is to download and manage the community of a given Social Media profile. By community I mean all the messages (both private and public) that a page receives during the day. Private messages involve all the direct messages, while by public I included all the post tags and comments.

By now the only social media channels I manage are Facebbok and Instagram, but it is (probably) possible to apply this code to every social.

## How does the Repository work?
In order to run the repository you simply need to run the file **CM_Automation.py**, the code will do all the processing. 

The repositoty contains two files:
- CM_Automation: in this file rests only the execution of the various functions. In few lines I will explain the different parts;
- utils: here rests the real "brain" of the project

First of all I declared the **start date** and **end date** range for the download. For a sake of robustness every day I set the day before from 00:00 to 23:59. These are the steps:
- **get_data**: download data from emplifi (fields: "author", "community_type", "content_type", "created_time", "id", "message", "messages", "origin", "parent_post", "profileId", "response_first", "post_labels", "url");
- replace NA's with the word "VUOTO" (not the best choice, improvable) and filter out posts;
- **create_conversations**: this is one of the most important functions. In this step I am going to "unpack" the conversations creating a dataframe where every row is a message, ordered by the send date. This is the result:
    ![image](https://github.com/user-attachments/assets/144e90a3-d346-4639-9457-bf2b92a1b8e9)[h!]

