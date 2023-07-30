## Overview
SmartPy is a comprehensive solution for developing, testing, and deploying smart contracts on the Tezos blockchain. With its easy-to-use Python syntax, developers can create contracts in a familiar and intuitive way, while SmartPy's type inference provides added safety.

Before deployment, contracts can be tested in simulated scenarios, including complex cases with multiple interacting contracts. Once ready, SmartPy contracts are compiled to Michelson, the Tezos blockchain's native language, for deployment.

With SmartPy, the possibilities for creating and deploying smart contracts on the Tezos blockchain are endless!

## Installation
The preferred way of running SmartPy is via the smartpy wrapper. This requires Docker and works on both Linux and macOS. It can be obtained as follows:

```
wget smartpy.io/smartpy
chmod a+x smartpy
```


## To test it, you can run the smartpy command:

```
./smartpy test main.py main/
```

## To have a direct access to the node container and execute manual commands, you can also do 

```
kubectl -n chain-2 exec -it archive-baking-node-0 -- /bin/sh
```

Now that the Michelson source code of your contract is in a file, you can run a command to originate it on the Tezos test network your client is connected to.

## Using smart contract
### Input the following command (in a single line):
```
octez-client originate contract contract \
 transferring 0 \
 from archive-baking-node-0 running contract.tz \
 --init '(Pair
    "tz1iyd1dExPGVuS7JvueGXF13LZaENVcaPya"
    (Pair
        {
        }
        (Pair
            {
            }
            (Pair
                {
                    Elt "" 0x68747470733a2f2f6578616d706c652e636f6d
                }
                (Pair
                    {
                    }
                    (Pair
                        {
                        }
                        (Pair
                            {
                            }
                            {
                            })))))))' \
 --fee 0.004671 \
 --gas-limit 10600 \
 --storage-limit 10000
```


### Get contract storage
```

octez-client get contract storage for contract
curl http://localhost:8733/chains/main/blocks/head/context/contracts/KT1Ksp8YL7qMput43naXv45rfQ8u8pRTCj5t/storage
``` 
### Admin update leader

```
octez-client transfer 0 from archive-baking-node-0 to contract --entrypoint "admin_update_leader" --arg "Pair \"tz1iyd1dExPGVuS7JvueGXF13LZaENVcaPya\" \"Shard-2\"" --burn-cap 1
```

### Leader update endpoint

```
octez-client transfer 0 from archive-baking-node-0 to contract --entrypoint "update_endpoint" --arg "Pair \"127.0.0.1:8733\" \"Shard-2\"" --burn-cap 1
```

### Leader update sharding policies

```
octez-client transfer 0 from archive-baking-node-0 to contract --entrypoint "update_sharding_policy" --arg "Pair \"Requirement: safety Hard gas limit per operation: 1040000 Hard gas limit per block: 3839999.8903274536 Hard storage limit per operation: 60000 Endorsing reward per slot: 0.9999999701976776 Minimal block delay: 5 Double baking punishment: 64.00002464652061 Consensus threshold: 4667 Balances of each node: archive-baking-node-0: key: edsk4QFGng4J8mQhcAz8pL9TQdZvSXD6a5oVnn7UMvJaKhRoiiftoH is_bootstrap_baker_account: true bootstrap_balance: 4000000000000 Nodes: archive-baking-node: Storage size: 15Gi Instances: 1 rolling-node: Storage size: 15Gi Instances: 5\" \"Shard-2\"" --burn-cap 1
```

### Self election
```
octez-client transfer 6000  from nodeA to contract --entrypoint "self_elected" --arg "\"Shard-2\"" --burn-cap 1
```