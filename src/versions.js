export const siteVariables = {
  // version-specific
  cliVersion: '1.13.0',
  runtimeVersion: '7.4.1',
  jenkinsenv: '${env.GIT_BRANCH}',
  jenkinsenv1: '${files[*]}',
  jenkinsenv2: '${#files[@]}',
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
};
