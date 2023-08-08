- [Adaptive Sharding-based Blockchain on Tezos Simulator](#asb)
  - [Prerequisites](#prerequisites)
  - [Installing prerequisites](#installing-prerequisites)
  - [Starting Minikube](#starting-minikube)
  - [Tezos k8s Helm Chart](#tezos-k8s-helm-chart)
- [Creating a Sharding-based Private Blockchain](#creating-a-private-blockchain)
- [Notes](#notes)
- [Tezos k8s](#tezos-k8s)

# Adaptive Sharding-based Blockchain on Tezos

This README walks you through:

- creating your own sharding-based Tezos private blockchain.

Using `minikube`, your nodes will be running in a peer-to-peer network inside of a Kubernetes cluster.

Follow the prerequisites step first. Then you can jump to [creating a private chain](#creating-a-private-blockchain).


## Prerequisites

- python3 (>=3.7)
- [docker](https://docs.docker.com/get-docker/)
- [kubectl](https://kubernetes.io/docs/reference/kubectl/kubectl/)
- [minikube](https://minikube.sigs.k8s.io/docs/)
- [helm](https://helm.sh/)
- [stable-baselines](https://stable-baselines.readthedocs.io/en/master/guide/install.html)
- [tensorboard](https://www.tensorflow.org/tensorboard/get_started?hl=vi)

## Installing prerequisites

This section depends on running Arch Linux system.

```shell
pacman -Syu && pacman -S docker python3 minikube kubectl kubectx helm
pip install 'stable-baselines3==1.7.0' --force-reinstall
pip install tensorboard
pip install wheel && pip install mkchain
```

Then change mode for user
```shell
sudo usermod -a -G docker huydq
```

## Starting Minikube

```shell
minikube start
```

Configure your shell environment to use minikube’s Docker daemon:

```shell
eval $(minikube docker-env)
```

This allows you to run Docker commands inside of minikube. For example: `docker images` to view the images that minikube has.

If you want to unset your shell from using minikube's docker daemon:

```shell
eval $(minikube docker-env -u)
```

## Tezos k8s Helm Chart

To add the Tezos k8s Helm chart to your local Helm chart repo, run:

```shell
helm repo add oxheadalpha https://oxheadalpha.github.io/tezos-helm-charts/
```

# Creating a Sharding-based Private Blockchain

Set as an environment variable the number of shard you would like to give to your chain:

```shell
export NUM_SHARD=num-shard
```

Then run following commands to start your Adaptive Sharding-based Blockchain:

```shell
python3 NUM_SHARD CHAIN_NAME
```

For example with NUM_SHARD = 2, run following command
```shell
python3 chain-1 8732
```

The command will do following tasks:

1. This will a file to create your chain:

`./${CHAIN_NAME}_values.yaml`

2. Then create a Helm release that will start your chain:

Your kubernetes cluster will now be running a series of jobs to
perform the following tasks:

- generate a node identity
- create a baker account
- generate a genesis block for your chain
- start the bootstrap-node baker to bake/validate the chain
- activate the protocol
- bake the first block

3. Exec to each node in each shard to do following jobs:

a. Port forwarding the shard so we can track the shard level

b. Deploy smart contract

c. Reveal node identity

d. Update leader to each shard

e. Listen to the level of each shard to run DDPG algorithm to get suitable sharding policy.

Here are a few more useful commands.
    
a. To pause your network, you can do `minikube stop` and resume it whenever you want with `minikube start`.

b. To stop and delete your network, you can `kubectl delete ns [NAMESPACE]`.

c. To see the overall status of your network and list the pods you have, you can `kubectl -n oxheadalpha get pods`

d. To watch the logs of the node of a pod, you can `kubectl -n oxheadalpha logs [POD] tezos-node -f`.

e. To have a direct access to the node container and execute manual commands, you can also do `kubectl -n CHAIN_NAME exec -it archive-baking-node-0 -- /bin/sh`

Congratulations! You now have an operational adaptive sharding-based Tezos 
chain.

# Notes

- We recommend using a very nice GUI for your k8s Tezos chain infrastructure called [Lens](https://k8slens.dev/). This allows you to easily see all of the k8s resources that have been spun up as well as to view the logs for your Tezos nodes. Checkout a similar tool called [k9s](https://k9scli.io/) that works in the CLI.

# Tezos k8s

Please see  [TEZOSK8S.md](./TEZOSK8S.md)
