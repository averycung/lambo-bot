<p align="center">
  <img src="assets/icon3.png" alt="Lambo Bot Icon" width="120"/>
</p>
<h1 align="center">Lambo Bot</h1>

**Lambo Bot** is a Telegram bot built to help users automatically promote their **BullX** and **Axiom** crypto trading platform referral links. It detects Solana token addresses in group chats and responds with the referring user’s custom referral link.

<p align="center">
  <img src="assets/banner.jpeg" alt="Lambo Bot Icon" width="800"/>
</p>

## Features 
- 🔍 Detects Solana contract addresses in Telegram messages
- 💭 Replies to all addresses with a customized referral link set by the user
- 💻 Tracks chat owners for consistent promotion between chats
- 🛢️ MySQL-backed database for storing referral data

## Tech Stack
- **Python**  
- **TeleBot (pyTelegramBotAPI)**  
- **MySQL**  
- Hosted on: `Railway`

## Demo
The bot has 7 commands:
* /start
* /instructions
* /help
* /setcode
* /viewcode
* /deletecode
* /claim

**/start**
starts the bot, returns a mesage containing preliminary instructions

![image](https://github.com/user-attachments/assets/07ae470a-4716-4938-9b51-0dec74f0696c)
-------

**/instructions**
returns a message containing bot usage instructions

![image](https://github.com/user-attachments/assets/5bbd2eaa-26e6-48fd-a7d6-98cc61acd73c)
-------
**/help**
returns a message containing a list of commands

![image](https://github.com/user-attachments/assets/134c7a7e-ac7f-49d2-a38a-ea91364d258e)
-------
**/setcode**
allows user to choose a platform to set a code for. referral code is processed and stored in MySQL with the user's unique Telegram ID as the key

![image](https://github.com/user-attachments/assets/1fc2b4b1-fb5c-4b0b-811c-ba5b16ed7a85)
![image](https://github.com/user-attachments/assets/ffed676e-953b-4abb-8b4a-5c2c45ddaca8)
-------
**/viewcode**
returns a message containing the user's referral codes. returns None if no code is set

![image](https://github.com/user-attachments/assets/93fc7842-3a0f-4af2-9001-060889f6b2c2)
-------
**/deletecode**
asks the user which platform to delete a referral code for. deletes the chosen code

![image](https://github.com/user-attachments/assets/f13ae279-eea6-4ecc-a69d-1cc4246277df)
![image](https://github.com/user-attachments/assets/94fbee9b-c6e6-43bc-890d-b41f698b3b8d)

![image](https://github.com/user-attachments/assets/c7e682d2-9931-4611-8255-e10a4dd38e42)
-------
**/claim**
allows the user to 'claim' ownership of a group chat/channel. Once a group chat is claimed, Lambo only promotes the referral code of the chat's owner. any time a Solana CA is detected, the owner's referral codes will be returned in a message.
chat owners are stored in a MySQL table with the unique chat id and telegram id as parameters. for user experience, **only admins** of a chat can use /claim. this ensures that usage of the bot stays intentional and controlled.

![image](https://github.com/user-attachments/assets/e7a94072-2bda-4717-ad33-3598c645290c)

## Main Function
**CA Detection**
Solana uses Base58Check encoding; each CA is a 32-byte public key. Lambo Bot detects for CAs in a message and returns ref links

![image](https://github.com/user-attachments/assets/0e1380a2-28fd-4b4a-ab43-4311830c365e)

![image](https://github.com/user-attachments/assets/d9e52597-8fc2-4d66-bcad-b64a02617d73)

![image](https://github.com/user-attachments/assets/679e6588-0593-4822-b8a1-72103d71fc8f)

## Contact
@natu102 on telegram


