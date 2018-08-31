# Nexo Efipress EWons

1. [What's the point?](#whats-the-point)
2. [Credentials](#credentials-configini)
3. [Running the ingestion of ewons tags](#running-the-ingestion-of-ewons-tags)
4. [What's next](#whats-next)


## What's the point?

Simple project to ingest a Ewons tags with Json API REST.


## Credentials `config.ini`

We must to rename the `config.ini.template` file to `config.ini` 
in the project's root directory, and fill it with the credentials

```ini
[CREDENTIALS]
t2maccount = account
t2musername = user
t2mpassword = pass
t2mdeveloperid = devid
```

## Running the ingestion of ewons tags

```bash
#!/usr/bin/env bash
PIDFILE=/tmp/ewons_app.pid
trap "{ rm -f $PIDFILE; }" EXIT

if [[ -f $PIDFILE ]]; then
  echo "Process is taking more than schedule interval..."
  exit 0
else
  echo $$ > ${PIDFILE}
  source ~/venvs/myenv/bin/activate
  python ~/pipeline.py
fi
```

## What's next

- [ ] Use corrutines with asyncio
- [ ] Index tags to elasticsearch
- [ ] Include shell scripts for running
- [x] Logging with a timed rotating log file
- [ ] Create a DockerFile
