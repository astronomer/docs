export const siteVariables = {
  // version-specific
  runtimeVersion: '9.1.0',
  cliVersion: '1.19.1',
  jenkinsenv: '${env.GIT_BRANCH}',
  jenkinsenv1: '${files[*]}',
  jenkinsenv2: '${#files[@]}',
  jenkinsenv3: '$(date +%Y%m%d%H%M%S)',
  jenkinsenv4: '$astro_id',
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
};
