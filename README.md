# Shipping :ship: 

![Shipping tests][github-url] [![Coverage Status][coveralls-image]][coveralls-url] [![CodeFactor][codefactor-image]][codefactor-url] [![Code style: black][black-image]][black-url]


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
[pypi]: https://pypi.python.org/pypi/shipping/
[coveralls-url]: https://coveralls.io/r/Clinical-Genomics/shipping
[coveralls-image]: https://img.shields.io/coveralls/Clinical-Genomics/shipping.svg?style=flat-square
[github-url]: https://github.com/Clinical-Genomics/shipping/workflows/Tests/badge.svg
[codefactor-image]: https://www.codefactor.io/repository/github/clinical-genomics/shipping/badge
[codefactor-url]: https://www.codefactor.io/repository/github/clinical-genomics/shipping
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black