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
 --fee 0.001266 \
 --gas-limit 10600 \
 --storage-limit 496
```

### Admin update leader

```
octez-client transfer 0 from archive-baking-node-0 to contract --entrypoint "admin_update_leader" --arg "Pair \"tz1iyd1dExPGVuS7JvueGXF13LZaENVcaPya\" \"Shard-2\""
```