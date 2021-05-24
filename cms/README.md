# Content Management System

## Development

Assuming the Sanity project is already set up:
1. `npm install`
2. `npx sanity login`, and login to the account that has the project.
3. `npm start`

Most errors with the Sanity CLI can be fixed by logging out and logging back in.

After making any changes to the schema, run `npm run deploy-dev-gql` so that the
GraphQL API gets updated with the latest changes.

## Deployment

After making any changes to the schema which you want to deploy, run `npm run
deploy-prod-gql` to deploy a new GraphQL API with the changes.

## Sanity Project Setup

1. `npm install -D @sanity/cli`
2. `npx sanity login`
3. `npx sanity init`
