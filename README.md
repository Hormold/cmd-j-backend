## Custom server for cmdj.app
**Disclaimer: This is research code and not intended for production use. Use at your own risk.**

This is the backend for the cmdj.app extension to use GPT-3 directly from the browser.
It uses stream api to send the request to the GPT-3 api and then stream the response back to the browser.

You need just a OPENAI_API_KEY in .env file to run this server.
All package dependencies should be installed with poetry.

*P.S. And of course, you need to modify Chrome extension to use your own server (replace cmdj original server with your own server url)*
*P.S.2 Add license_key=randomstr cookie (to use the custom server, instead ChatGPT) on extension website https://cmdj.app*