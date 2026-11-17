# ABC University SMS (CT142-3-3-DevOps)

Flask + SQLite prototype deployed through the initial pipeline (Figure 1):
push/PR to GitHub -> GitHub Actions (lint + pytest) -> Docker image -> Docker Hub -> AWS Elastic Beanstalk.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
flask --app wsgi run --debug      # http://127.0.0.1:5000
pytest -v
flake8 .
```

## Team workflow (GitHub flow)

1. `git checkout main && git pull`
2. `git checkout -b feature/<your-fr>` (e.g. `feature/attendance`)
3. Build your FR under `app/` plus at least 2 tests in `tests/`
4. Push and open a PR into `main`. Actions runs lint + tests on the PR.
5. One teammate reviews, then merge. Merging to `main` builds, pushes and deploys.

Your own commits, PR and the Actions run your merge triggers are your contribution evidence for the video.
**Merge your own PR** after it is approved. The deploy run is credited to whoever clicks Merge, so if a
teammate merges it, the run shows their name instead of yours.

## One-time setup (pipeline owner)

### 1. Docker Hub
- Create a **public** repository `group1-sms-repo`.
- Account Settings -> Personal access tokens -> new token (Read & Write).

### 2. AWS Learner Lab: Elastic Beanstalk
Start the lab, open the console (region **us-east-1**), then Elastic Beanstalk -> Create application:
- Application name: `abc-sms`, environment name: `abc-sms-env`
- Platform: **Docker** (Amazon Linux 2023), application code: Sample application
- Presets: **Single instance** (no load balancer)
- Service role: **LabRole**; EC2 instance profile: **LabInstanceProfile**; key pair: `vockey`
- Instance type: **t3.micro**; no database
- Wait until Health = Ok

### 3. GitHub repo settings
Settings -> Secrets and variables -> Actions:

| Type | Name | Value |
|------|------|-------|
| Secret | `DOCKERHUB_USERNAME` | Docker Hub username |
| Secret | `DOCKERHUB_TOKEN` | token from step 1 |
| Secret | `AWS_ACCESS_KEY_ID` | Learner Lab -> AWS Details -> AWS CLI |
| Secret | `AWS_SECRET_ACCESS_KEY` | same |
| Secret | `AWS_SESSION_TOKEN` | same |
| Variable | `EB_APP_NAME` | `abc-sms` |
| Variable | `EB_ENV_NAME` | `abc-sms-env` |
| Variable | `AWS_REGION` | `us-east-1` |
| Variable | `DEPLOY_ENABLED` | `false` normally; `true` only while the Beanstalk environment is running |

With `DEPLOY_ENABLED=false`, merges still run lint, tests, build and push to Docker Hub; only the deploy job is
skipped. When the environment is up again, set it to `true` and re-run the workflow: the latest `main`
(every merged feature) deploys at once.

Settings -> Branches -> add rule for `main`: require a pull request, 1 approval, and status check **Lint and test**.

## Before every deploy or video recording

The Beanstalk environment lives in the **pipeline owner's** Learner Lab account, so only they can refresh the
credentials, and the live URL only works while their lab session is running (sessions last about 4 hours;
instances stop when it ends). So:

- Book a slot with the pipeline owner before you merge or record.
- They start the lab, copy the three AWS values from AWS Details into the GitHub secrets, and confirm the URL works.
- Merge (or re-run: Actions -> CI/CD - SMS -> Run workflow) and record within that session.
- You show EB through the deploy job logs and the live URL. The EB console is only visible to the owner,
  so they take the EB console screenshots for everyone.

## Known limitations of this initial pipeline (feed into Part 2)

- No staging environment or production approval gate: every merge goes straight to the live environment.
- No code-quality/security scanning (SonarCloud, Trivy, Dependabot).
- SQLite lives inside the container, so data resets on every redeploy. Production would use RDS.
- No monitoring beyond EB basic health and a single smoke test; no automated rollback.
- Short-lived Learner Lab credentials stored as static secrets instead of OIDC role federation.