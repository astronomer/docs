export const siteVariables = {
  // version-specific
  cliVersion: '1.8.1',
  runtimeVersion: '6.0.4',
  // Hacky variable so that we can use env var formatting in CI/CD templates
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
  keyid: '${ASTRONOMER_KEY_ID}',
  keysecret: '${ASTRONOMER_KEY_SECRET}',
  devkeyid: '${DEV_ASTRONOMER_KEY_ID}',
  devkeysecret: '${DEV_ASTRONOMER_KEY_SECRET}',
  prodkeyid: '${PROD_ASTRONOMER_KEY_ID}',
  prodkeysecret: '${PROD_ASTRONOMER_KEY_SECRET}',
  // Hacky variable for droneci
  deploymentiddrone: '$ASTRONOMER_DEPLOYMENT_ID',
};
