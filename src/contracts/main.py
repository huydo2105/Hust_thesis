import smartpy as sp

        
policy = """Requirement: safety

    Hard gas limit per operation: 1040000
    Hard gas limit per block: 3839999.8903274536
    Hard storage limit per operation: 60000
    Endorsing reward per slot: 0.9999999701976776
    Minimal block delay: 5
    Double baking punishment: 64.00002464652061
    Consensus threshold: 4667
    
    Balances of each node:
    archive-baking-node-0:
      key: edsk4QFGng4J8mQhcAz8pL9TQdZvSXD6a5oVnn7UMvJaKhRoiiftoH
      is_bootstrap_baker_account: true
      bootstrap_balance: 4000000000000
    
    Nodes:
    archive-baking-node:
      Storage size: 15Gi
      Instances: 1
    rolling-node:
      Storage size: 15Gi
      Instances: 5"""
false_policy = """Requirement: safety

    Hard gas limit per operation: 1040000
    Hard gas limit per block: 3839999.8903274536
    Hard storage limit per operation: 60000
    Endorsing reward per slot: 0.9999999701976776
    Minimal block delay: 5
    Double baking punishment: 64.00002464652061
    Consensus threshold: 4667
    
    Balances of each node:
    archive-baking-node-0:
      key: edsk4QFGng4J8mQhcAz8pL9TQdZvSXD6a5oVnn7UMvJaKhRoiiftoH
      is_bootstrap_baker_account: true
      bootstrap_balance: 4000000000000
    
    Nodes:
    archive-baking-node:
      Storage size: 15Gi
      Instances: 1
    rolling-node:
      Storage size: 15Gi
      Instances: 5"""

@sp.module
def main():
    class ShardingBlockchain(sp.Contract):
        def __init__(self, admin, metadata):
            self.data.endpoints = {}
            self.data.admin = admin
            self.data.metadata = metadata
            self.data.leaders = {}
            self.data.proposed_leaders = {}
            self.data.sharding_policies = {}
            self.data.num_nodes = {}
            self.data.voting = {}

        @sp.entry_point
        def admin_update_leader(self, params):
            assert sp.sender == self.data.admin, "NotAdmin"
            self.data.leaders = sp.update_map(params.shard, sp.Some(params.leader), self.data.leaders)
            self.data.proposed_leaders = sp.update_map(params.shard, sp.Some(sp.set(params.leader)), self.data.proposed_leaders)
            assert self.data.leaders[params.shard] == params.leader
            assert self.data.proposed_leaders[params.shard].contains(params.leader)
            
        @sp.entry_point
        def update_endpoint(self, params):
            assert sp.sender == self.data.admin or sp.sender == self.data.leaders[params.shard], "NotAdminNorLeaders"
            self.data.endpoints = sp.update_map(params.shard, sp.Some(params.endpoint), self.data.endpoints)
            assert self.data.endpoints[params.shard] == params.endpoint

        @sp.entry_point
        def update_num_nodes(self, params):
            assert sp.sender == self.data.admin or sp.sender == self.data.leaders[params.shard], "NotAdminNorLeaders"
            self.data.num_nodes = sp.update_map(params.shard, sp.Some(params.num_nodes), self.data.num_nodes)
            assert self.data.num_nodes[params.shard] == params.num_nodes
            
        @sp.entry_point
        def update_sharding_policy(self, params):
            assert sp.sender == self.data.admin or sp.sender == self.data.leaders[params.shard], "NotAdminNorLeaders"
            self.data.sharding_policies = sp.update_map(params.shard, sp.Some(params.policy), self.data.sharding_policies)
            assert self.data.sharding_policies[params.shard] == params.policy

        @sp.entry_point
        def self_elected(self, params):
            assert sp.amount == sp.tez(6000), "InsufficientStake"
            self.data.proposed_leaders[params.shard].add(sp.sender)
            assert self.data.proposed_leaders[params.shard].contains(sp.sender)
            
        @sp.entry_point
        def select_leaders(self, params):
            assert sp.sender == self.data.admin, "NotAdmin"
            x = 0
            # for shard in self.data.proposed_leaders.items():
            proposed_leaders = self.data.proposed_leaders[params.shard].elements()
            for leader in proposed_leaders:
                if x == 0:
                    selected_leader = leader
                    self.data.leaders = sp.update_map(params.shard, sp.Some(selected_leader), self.data.leaders)
                    x += 1
                else:
                    sp.send(leader, sp.tez(6000))

        @sp.entry_point
        def propose_new_leader(self, params):
            assert sp.amount == sp.tez(6000), "InsufficientStake"
            proposal = sp.record(
                proposer= sp.sender,
                votes= sp.set(sp.sender),
                new_leader= params.new_leader,
            )
            self.data.voting = sp.update_map(params.shard, sp.Some(proposal), self.data.voting)
            
            
        @sp.entry_point
        def vote_new_leader(self, params):
            shard_votes = self.data.voting[params.shard]
            assert self.data.voting.contains(params.shard) , "NoProposal"
            assert not shard_votes.votes.contains(sp.sender), "AlreadyVoted"
            shard_votes.votes.add(sp.sender)

        @sp.entry_point
        def update_leader(self, params):
            shard_votes = self.data.voting[params.shard]
            malicious_leader = self.data.leaders[params.shard]
            new_leader = shard_votes.new_leader
            
            assert sp.sender == shard_votes.proposer or sp.sender == self.data.admin, "NotProposerNorAdmin"
            assert self.data.voting.contains(params.shard) , "NoProposal"
            if len(shard_votes.votes) > (2 * self.data.num_nodes[params.shard]) / 3:
                sp.send(malicious_leader, sp.tez(3000))
                sp.send(new_leader, sp.tez(3000))
                self.data.leaders = sp.update_map(params.shard, sp.Some(new_leader), self.data.leaders)
                del self.data.voting[params.shard]
            else:
                sp.send(new_leader, sp.tez(3000))
                
                
    
if "templates" not in __name__:

    @sp.add_test(name="Adaptive Sharding")
    def test():
        # sp.test_account generates ED25519 key-pairs deterministically:
        admin = sp.test_account("Administrator")
        nodeA_shard1 = sp.test_account("nodeA_shard1")
        nodeB_shard1 = sp.test_account("nodeB_shard1")
        nodeC_shard1 = sp.test_account("nodeC_shard1")
        nodeD_shard1 = sp.test_account("nodeD_shard1")
        
        nodeE_shard2 = sp.test_account("nodeA_shard2")
        nodeF_shard2 = sp.test_account("nodeB_shard2")
        nodeG_shard2 = sp.test_account("nodeC_shard2")
        nodeH_shard2 = sp.test_account("nodeD_shard2")

        # Instantiate a contract
        c1 = main.ShardingBlockchain(
            admin=admin.address,
            metadata=sp.utils.metadata_of_url("https://example.com"))
        
        # Create a scenario
        scenario = sp.test_scenario(main)
        # Add the contract to the scenario
        scenario += c1
        scenario.h1("Transparent Leader Selection Smart Contract")
        # Let's display the accounts:
        scenario.h2("Accounts")
        scenario.show([admin, nodeA_shard1, nodeB_shard1, nodeC_shard1, nodeD_shard1, 
                        nodeE_shard2, nodeF_shard2, nodeG_shard2, nodeH_shard2])
  
        
    
        scenario.h2("Healthy epoch simulation")
        scenario.h3("Admin Update leaders for shard-1")
        c1.admin_update_leader(shard="Shard-1", leader = nodeA_shard1.address).run(valid=True, sender=admin)
        scenario.verify(c1.data.leaders["Shard-1"] == nodeA_shard1.address)
        scenario.verify(c1.data.proposed_leaders["Shard-1"].contains(nodeA_shard1.address))
        
        scenario.h3("Admin update number of nodes for shard-1")
        c1.update_num_nodes(shard="Shard-1", num_nodes = 4).run(valid=True, sender=admin)
        scenario.verify(c1.data.num_nodes["Shard-1"] == 4)
        
        scenario.h3("Leader Update endpoints")
        c1.update_endpoint(shard="Shard-1", endpoint = "127.0.0.1:8732").run(valid=True, sender=nodeA_shard1)
        scenario.verify(c1.data.endpoints["Shard-1"] == "127.0.0.1:8732")
        
        scenario.h3("Leader Update policy")
        c1.update_sharding_policy(shard="Shard-1", policy = policy).run(valid=True, sender=nodeA_shard1)
        scenario.verify(c1.data.sharding_policies["Shard-1"] == policy)
        
        scenario.h3("Nodes Self election")
        c1.self_elected(shard="Shard-1").run(valid=True, sender=nodeB_shard1, amount = sp.tez(6000))
        c1.self_elected(shard="Shard-1").run(valid=True, sender=nodeC_shard1, amount = sp.tez(6000))
        scenario.verify(c1.data.sharding_policies["Shard-1"] == policy)
        scenario.verify(c1.balance == sp.tez(12000))
        
        scenario.h3("Select leader")
        c1.select_leaders(shard = "Shard-1").run(valid=True, sender=admin)

        scenario.h2("Bad epoch simulation")
        scenario.h3("Admin Update leaders")
        c1.admin_update_leader(shard="Shard-2", leader = nodeE_shard2.address).run(valid=True, sender=admin)
        scenario.verify(c1.data.leaders["Shard-2"] == nodeE_shard2.address)
        scenario.verify(c1.data.proposed_leaders["Shard-2"].contains(nodeE_shard2.address))
        
        scenario.h3("Leader Update endpoints")
        c1.update_endpoint(shard="Shard-2", endpoint = "127.0.0.1:8733").run(valid=True, sender=nodeE_shard2)

        scenario.h3("Admin update number of nodes for shard-2")
        c1.update_num_nodes(shard="Shard-2", num_nodes = 4).run(valid=True, sender=admin)
        scenario.verify(c1.data.num_nodes["Shard-1"] == 4)
        
        scenario.h3("Leader Update policy")
        c1.update_sharding_policy(shard="Shard-2", policy = policy).run(valid=True, sender=nodeE_shard2)
        
        scenario.h3("Node find out malicious leader by comparing policy")
        scenario.h3("NodeF propose to change leader to nodeF")
        c1.propose_new_leader(shard="Shard-2", new_leader = nodeF_shard2.address).run(valid=True, sender=nodeF_shard2, amount=sp.tez(6000))

        scenario.h3("Other nodes agree the proposal")
        c1.vote_new_leader(shard="Shard-2").run(valid=True, sender=nodeG_shard2)
        c1.vote_new_leader(shard="Shard-2").run(valid=True, sender=nodeH_shard2)

        scenario.h3("Admin update leader")
        c1.update_leader(shard="Shard-2").run(valid=True, sender=admin)

        
        

    

        
        
