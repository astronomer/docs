export const siteVariables = {
  cli- 1.5.0
cliVersion: '1.5.0',
  runtimeVersion: '5.0.0',
    // Hacky variable so that we can use env var formatting in CI/CD templates
    deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
      keyid: '${ASTRONOMER_KEY_ID}',
        keysecret: '${ASTRONOMER_KEY_SECRET}',
          // Hacky variable for droneci
          deploymentiddrone: '$ASTRONOMER_DEPLOYMENT_ID',
};
