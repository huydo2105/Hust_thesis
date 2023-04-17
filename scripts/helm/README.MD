# Deploy a Tezos Chain using Helm

This script deploys a Tezos chain using Helm.

## Prerequisites

You must have the following tools installed:

- Helm: https://helm.sh/docs/intro/install/
- Tezos Chain Helm chart: https://github.com/oxheadalpha/helm-charts/tree/main/charts/tezos-chain

## Usage
### Install
/install.sh <chain_name>

Where `<chain_name>` is the name of your Tezos chain. If the name is not provided, it will default to `default-chain`.

The script creates a Helm release for the Tezos chain with the specified name and deploys it using the `oxheadalpha/tezos-chain` chart. The values for the release are loaded from a YAML file with the name `<chain_name>_values.yaml`. The namespace for the release is also set to `<chain_name>`.

Example usage:
./install.sh my-tezos-chain
his will create a Helm release for a Tezos chain named `my-tezos-chain` using the values in the `my-tezos-chain_values.yaml` file.

### Upgrade
/upgrade.sh <chain_name>

Where `<chain_name>` is the name of your Tezos chain. If the name is not provided, it will default to `default-chain`.

The script upgrade a Helm release for the Tezos chain with the specified name and deploys it using the `oxheadalpha/tezos-chain` chart. The values for the release are loaded from a YAML file with the name `<chain_name>_values.yaml`. The namespace for the release is also set to `<chain_name>`.

Example usage:
./upgrade.sh my-tezos-chain
his will create a Helm release for a Tezos chain named `my-tezos-chain` using the values in the `my-tezos-chain_values.yaml` file.

