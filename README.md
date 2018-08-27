# helm-secrets-py

python rewrite of the [bash version](https://github.com/futuresimple/helm-secrets)

## Installation

Dependencies:
- python3
- [mozilla/sops](https://github.com/mozilla/sops)

Install the plugin using
```
helm plugin install https://github.com/hensur/helm-secrets-py.git
```

## Usage

Overview of available modes:
```
> helm secrets
usage: secrets.py [-h] {enc,dec,view,clean,deploy,install,upgrade} ...

GnuPG secrets encryption in Helm Charts This plugin provides ability to
encrypt/decrypt secrets files to store in less secure places, before they are
installed using Helm. To decrypt/encrypt/edit you need to initialize/first
encrypt secrets with sops - https://github.com/mozilla/sops

optional arguments:
  -h, --help            show this help message and exit

commands:
  {enc,dec,view,clean,deploy,install,upgrade}
    enc                 encrypt a given file
    dec                 decrypt a given file
    view                view a given file (decrypted)
    clean               clean a given dir (decrypted)
    deploy              wrapper for helm, builds the value file list based on
                        a leaf directory
    install             wrapper for helm install that decrypts secret files
                        before execution
    upgrade             wrapper for helm upgrade that decrypts secret files
                        before execution
```

## features

the core functionality is the decryption and encryption of secrets.yaml files

either manually by using `helm secrets enc` or `helm secrets dec`
or by using the helm wrappers `helm secrets install` or `helm secrets upgrade`

the helm wrappers will decrypt the secrets, run the helm install command and encrypt
the secrets afterwards.

the deploy command will collect all values or secrets files from the helm_vars
directory.

## deploy
deploy is a special command that will automatically deploy a chart configuration
(there can be different configs for dev and prod)

this whole command is based on a expected directory structure with a helm_vars directory
that contains all values.yaml and secrets.yaml files.

```
> cd manifests/example-chart
example-chart > tree .
.
├── Chart.yaml
├── helm_vars
│   ├── dev
│   │   ├── secrets.yaml
│   │   └── values.yaml
│   ├── prod
│   │   └── values.yaml
│   └── values.yaml
├── requirements.lock
├── requirements.yaml
└── templates
    ├── clusterrolebinding.yaml
    ├── clusterrole.yaml
    ├── _helpers.tpl
    ├── NOTES.txt
    └── service-account.yaml
```

### examples

to deploy the dev environment for this chart, run from the charts parent directory
```
manifests > helm secrets deploy install example-chart/helm_vars/dev
```

the deploy mode will the generate a helm_cmd that includes all values and decrypted secrets files
in the dev and parent directories

```
helm install -f /manifests/example-chart/helm_vars/dev/values.yaml -f /manifests/example-chart/helm_vars/dev/secrets.dec.yaml -f /manifests/example-chart/helm_vars/values.yaml -n example-chart /manifests/example-chart
```
