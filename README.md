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
[ACC_CREDENTIALS]
t2maccount = account
t2musername = user
t2mpassword = pass
t2mdeveloperid = devid

[INS_CREDENTIALS]
t2mdeviceusername = user
t2mdevicepassword = pass

[ELASTIC]
esnodes = esnode1:port,esnode2:port
user = user
pass = pass

[LOGGING]
level = DEBUG
```
> `user` and `pass` only if required for the connection to Elasticsearch

## Running the ingestion of ewons tags

```bash
python3.6 pipeline.py
```
> We must to install requirements.txt


## What's next

- [ ] Use corrutines with asyncio
- [x] Index tags to elasticsearch
- [x] Include shell scripts for running
- [x] Logging with a timed rotating log file
- [ ] Create a DockerFile
