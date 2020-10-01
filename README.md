# Shipping :ship: 

Cli utility for deploying packages.

## Idea

To simplify the process of deploying packages on different servers and in different ways. Currently there is support for deploying packages in conda environments, however it is being built with other methods such as containers, poetry etc in mind.

There are two configs in use, one is to describe the host environment and the other will hold specific instructions for a package.

All suggestions are welcome.

## Example usage

```
$cat configs/server1/prod.yaml
---
hostname: computer1
log_file: /logs/production_deploy_log.txt


$cat configs/server1/scout_production.yaml
---
tool: scout
env_name: P_scout
deploy_method: pip

$shipping --host-info configs/server1/prod.yaml deploy --config configs/server1/scout_production.yaml
```

This command will deploy the tool `scout` into the conda environment `P_scout` on the server `computer1` and log who deployed what version and when.

There will be different use cases where the deployment process involves restarting a server or installing dependencies with [yarn][yarn] etc that we will support.


[yarn]: https://yarnpkg.com