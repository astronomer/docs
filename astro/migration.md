### Step 8: Configure Additional Components
- Add CICD if already being used in Source environment
- Add Secrets Backend if already being used in Source environment
- Add Trust Policies between Astro and Cloud Roles, as needed.

### Step 9: Test locally and check for import errors
Test the environment locally with the CLI using `astro dev parse`  and `astro dev start` - inspect errors in the CLI and/or the localhost webserver

### Step 10: Deploy
Deploy with astro deploy 

## Test and Cutover Process
### Test and Cutover
- Confirm successful migration of connections & variables in Target environment
- Validate and test DAGs in Target environment
- Utilize Starship in Source Environment to pause DAGs in Source and unpause DAGs in Target
### **Tune instance**
- Monitor analytics as DAGs turn on
- Add new instance types to match worker size from source
- Add any intentionally set Airflow Configuration settings
    - Note: not all configurations are [configurable on Astro](https://docs.astronomer.io/astro/platform-variables)
- Add `DAGs-only Deployment` , if desired
### Continue and repeat
- Customer continues to **Test and Cutover DAGs** on Astro with support from Astro Data Engineers via Slack, engaging in additional calls, as needed.
- Repeat Migration for all Environments after initial airflow environment is fully migrated