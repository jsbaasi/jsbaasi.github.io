---
layout: post
title: Kubernetes Notes
date: 2026-05-01 20:30:22 +0000
categories: development kubernetes infrastructure
permalink: /kubernetes-notes/
---
[Vault Notes]
`kubectl get pods -A` get pods running in the all the namespaces

`kubectl describe ingress backstage -n infra-backstage` kubectl can you describe what the backstage ingress resource looks like in the infra-backstage namespace
`kubectl rollout status <resource> <namespace> -o wide`
if i want to check when my new backstage application state will be synced to my cluster i can do `kubectl rollout status deployment/backstage -n infra-backstage -o wide`

`kubectl exec postgres-1 -n infra-postgres -- psql -c "\l+"`
to see what databases there are in my postgres instance

`kubectl run --image=<image_tag> --dry-run=client -o=yaml`
to see the deployment

```bash
kubectl run -i --tty busybox --image=busybox:1.28 -- sh  # Run pod as interactive shell
```

```bash
kubectl run <name> --image=<image_tag> --dry-run=client -o=yaml
```
for dry run
```bash
kubectl get all,cm,secret,ing -A
```
for getting all resources in the cluster
```bash
kubectl -n infra-vault get $(kubectl api-resources --namespaced=true --no-headers -o name | egrep -v 'events|nodes' | paste -s -d, - ) --no-headers
```
to get all resources in the namespace `infra-vault`
```bash
kubectl exec --stdin --tty bot -- sh
```
get a shell to pod named `bot`, i tried to do `/bin/bash` command on the alpine image, but not recognised, sh is tho
```bash
kubectl describe ss vault
```
describe secret store kind of resource named vault
```bash
kubectl api-versions
```
annoying command
```bash
kubectl get secret <secret-name> -n <namespace> jsonpath='{.data}' | base64 -d
```
after you do jsut plain .data then see what key you want, then key into it with jsonpath and then pipe it to base64
# helm
`helm list`
# Abbreviations
ESO - external secrets operator
# k3d notes

starts with `k3d cluster`, and tbh you can figure it out from the help command
`k3d cluster list` to ... list clusters
`k3d cluster create --config ~/.kube/cluster_config.yaml` to start a cluster with the config file given as a flag
# Past Issues
- backstage was appearing down from the vpn, looking at the ingress resources and the backstage pod it was healthy. The problem was that the cnpg auth was configured incorrectly and wouldn't let backstage connect. 
- `kubectl rollout restart deployment/backstage -n infra-backstage` had to do this because backstage was running with old secrets, apparently the 'env' secrets are copied into the container at start time, and are not read from the 'environment' anymore
