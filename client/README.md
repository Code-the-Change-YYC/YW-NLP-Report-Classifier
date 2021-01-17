# NLP CIR Webform

This folder holds the front-end webform for CIR input written in React.

In this folder, you can run `npm i` to install the necessary dependencies, then `npm start` to run the development server. Node.js needs to be installed.

## Sanity API

Must create a read token and make it available as the `REACT_APP_SANITY_READ_TOKEN`
environment variable. Tokens can be created in the project dashboard (`npx
sanity manage`).

Also add the `REACT_APP_SANITY_GRAPHQL_ENDPOINT` environment variable. The
endpoint is printed after `npx sanity graphql deploy`.

In the project dashboard the development URL (http://localhost:3000) must be
added under CORS Origins.