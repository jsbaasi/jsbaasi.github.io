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
# Abbreviations
ESO - external secrets operator
# Past Issues
- backstage was appearing down from the vpn, looking at the ingress resources and the backstage pod it was healthy. The problem was that the cnpg auth was configured incorrectly and wouldn't let backstage connect. 
