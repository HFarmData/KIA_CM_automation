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
- **create_conversations**: this is one of the most important functions. In this step I am going to "unpack" the conversations creating a dataframe where every row is a message, ordered by date. After that I keep only the messages between start_date and end_date to be sure to not to have unnecessary messages. This is the result:
    ![image](https://github.com/user-attachments/assets/144e90a3-d346-4639-9457-bf2b92a1b8e9)
- **create_final_df**: here we have a simple functions that copies the previous dataframe in a new one, adding the other necessary columns.
      ![image](https://github.com/user-attachments/assets/3f5bb409-5ed8-4360-a8e4-cf14bbc29efd)
- **before_deadline**: a very challengin problem was the column BEFORE DEADLINE. The request was to track all the messages that recevied an answer in a time frame of two hours. Using this function I addressed the problem

After all these passages It comes another interesting part. Another request from the team was to automatically find: License Plate, Car Dealer, Chassis Number and Sentiment for every message. To solve this, I exploited **OpenAI API**.
THe process is quite simple: I analyze every comment and through a refined prompt I let GPT-4o find the information I need. 

Last part of the project was generating an automatic answer for every comment. To solve this issue I took advantage of OpenAI assistants: through a file that I put in knowledge containing the FAQ.

To sum up everything the final result will be:
![image](https://github.com/user-attachments/assets/ebb2dec3-e5e4-4b39-8382-359858afe0c2)


