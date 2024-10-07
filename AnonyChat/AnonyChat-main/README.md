# AnonyChat 🔒

AnonyChat is a fully decentralised chat program using RSA Encryption for secure communication. It allows for unlimited clients and has ban/kick functionality.

## Features 🚀

- RSA Encrypted Chatroom
- Unlimited Clients
- Ban/Kick Functionality
- Disclaimer: The server will be able to log messages if configured to do so.

## How to setup (Client)

1. Clone the repository (`git clone github.com/SaintsConnor/AnonyChat`)
2. install rsa (`pip install rsa`)
3. Run the following command: `python3 [Path/To/AnonyChat]/Client/main.py`
4. Follow on screen prompts

## How to setup (Server)

1. Clone the repository (`git clone github.com/SaintsConnor/AnonyChat`)
2. install rsa (`pip install rsa`)
3. Edit server/main.py for custom password/admin nickname
4. Run the following command: `python3 [Path/To/AnonyChat]/Server/main.py`
5. Ensure firewall allows the port!
6. Share IP/Port with Clients
7. Please note that you will to connect to the server yourself. If it is hosted on the pc you are connecting to, please use localhost as server name. Otherwise use the public IP address and port

## Upcoming Features 📈

- Direct Messaging
- Server Channels
- File Transfers
- Voice Chat
- Update Detection

## How to contribute 🤝

If you would like to contribute, please submit a pull request and an developer will check it is suitable for the program and works. Upon approval you will be added to CONTRIBUTORS.txt

Alternatively, contact the lead developer if you would like to be a main developer on: ssgconnor@proton.me

## Security 🔒

Any vulnerabilities are taken seriously and regular updates will be given to fix them. If discovered please email Connor on: ssgconnor@proton.me

## Known Issues 🐛

- The chat program may experience connection issues on certain network configurations.
- The ban/kick functionality may not work properly in some cases.
- Characters may not display properly in the chatroom due to encoding issues (Fix In Progress).

## Version Control 🚀

AnonyChat uses Git for version control. Each release is tagged with a version number and a codename.

### Release History 📜

- v0.1 (Alpha) - "First Steps" 🐣
- v0.2 (Alpha) - "Encryption Update" 🔒
- v0.3 (Alpha) - "Networking Update" 🌐
- v0.4 (Alpha) - "The Bug Bust" 🚀 (IN PROGRESS)

To see the full list of changes for each release, please refer to the [CHANGELOG.md](./CHANGELOG.md) file.

## LICENSE 📜

This software is under the: "GNU GENERAL PUBLIC LICENSE v3.0". Below is a TLDR of this.

- Anyone can copy, modify and distribute this software.
- You have to include the license and copyright notice with each and every distribution.
- You can use this software privately.
- You can use this software for commercial purposes.
- If you dare build your business solely from this code, you risk open-sourcing the whole code base.
- If you modify it, you have to indicate changes made to the code.
- Any modifications of this code base MUST be distributed with the same license, GPLv3.
- This software is provided without warranty.
- The software author or license can not be held liable for any damages inflicted by the software.
