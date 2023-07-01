cd /home/fetia/IdeaProjects/mkchain/agents
/home/fetia/IdeaProjects/mkchain/agents
cd /home/fetia/IdeaProjects/mkchain/src
minikube start
eval $(minikube docker-env)
cd /home/fetia/IdeaProjects/mkchain/src
. .venv/bin/activate
helm repo add oxheadalpha https://oxheadalpha.github.io/tezos-helm-charts/

