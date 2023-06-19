export const siteVariables = {
  // version-specific
  cliVersion: '1.16.1',
  runtimeVersion: '8.5.0',
  jenkinsenv: '${env.GIT_BRANCH}',
  jenkinsenv1: '${files[*]}',
  jenkinsenv2: '${#files[@]}',
  jenkinsenv3: '$(date +%Y%m%d%H%M%S)',
  jenkinsenv4: '$astro_id',
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
};
