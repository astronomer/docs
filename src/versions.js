export const siteVariables = {
  // version-specific
  cliVersion: '1.14.0',
  runtimeVersion: '7.4.2',
  jenkinsenv: '${env.GIT_BRANCH}',
  jenkinsenv1: '${files[*]}',
  jenkinsenv2: '${#files[@]}',
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
};
