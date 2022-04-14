export const siteVariables = {
  cliVersion: '1.4.0',
  runtimeVersion: '4.2.4',
  // Hacky variable so that we can use env var fromatting in CI/CD templates
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
  keyid: '${ASTRONOMER_KEY_ID}',
  keysecret: '${ASTRONOMER_KEY_SECRET}',
  // Hacky variable for droneci
  deploymentiddrone: '$ASTRONOMER_DEPLOYMENT_ID',
};
