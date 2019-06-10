# CloudVault



## Brew Setup

1. TBD

## Envchain Setup

1. Install envchain.
```
brew install envchain
```
  - __Note__: [brew](#Brew-Setup) is required for installation.
2. Save a ```CloudVault-GitLab-Token``` as an envchain object.
```
envchain --set --noecho --require-passphrase Vault VAULT_LAB_API_TOKEN
```
  - __Note__: A [GitLab Access Key](#Brew-Setup) is required for setup.



```
envchain CloudVault python3 -m CloudVault
```