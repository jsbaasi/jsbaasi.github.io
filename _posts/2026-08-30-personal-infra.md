---
layout: post
title: Personal Infra
date: 2026-08-30 21:45:02 +0000
categories: development
permalink: /personal-infra/
---
Going to be moving to docker compose for my vps infra. Kubernetes is a bit too expensive for my 8gb box and at the moment I don't really need anything bigger. Mostly focusing on stuff other than wan-accessible services.
# Getting rid of
- kubernetes
- backstage
- argocd

In Compose that boilerplate doesn't exist, because Traefik, Prometheus and Alloy all discover things from container labels and the Docker socket. A whole service becomes:

```
services:
  fulb:
    image: registry.gitlab.com/jsbaasi/engineering/fulb:${FULB_TAG:-latest}
    env_file: [secrets.env]
    networks: [edge, backend]
    labels:
      traefik.enable: "true"
      traefik.http.routers.fulb.rule: "Host(`fulb.stormblessed.fr`)"
      traefik.http.routers.fulb.tls.certresolver: le
      prometheus.scrape: "true"
```

```
stack/
├── compose.yaml              # include: the rest
├── platform/
│   ├── compose.yaml          # traefik, prometheus, grafana, loki, alloy, postgres, redis
│   ├── fragments.yaml        # shared service definitions
│   ├── prometheus.yml
│   ├── provision-db.sh
│   └── grafana/provisioning/{datasources,dashboards}/
├── apps/
│   ├── fulb/{compose.yaml,secrets.env}
│   ├── fudbot/…
│   └── continuwuity/…
└── Makefile
```

```
# compose.yaml
include:
  - platform/compose.yaml
  - apps/fulb/compose.yaml
  - apps/fudbot/compose.yaml
  - apps/continuwuity/compose.yaml
```

service = new directory, one line

Metrics — write the config once

```
# platform/prometheus.yml
scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 15s
    relabel_configs:
      - source_labels: [__meta_docker_container_label_prometheus_scrape]
        regex: "true"
        action: keep
      # only the backend network, or you get one target per attached network
      - source_labels: [__meta_docker_network_name]
        regex: "stack_backend"
        action: keep
      - source_labels: [__address__, __meta_docker_container_label_prometheus_port]
        regex: '([^:]+)(?::\d+)
        replacement: "$1:$2"
        target_label: __address__
      - source_labels: [__meta_docker_container_label_prometheus_path]
        regex: "(.+)"
        target_label: __metrics_path__
      - source_labels: [__meta_docker_container_name]
        regex: "/(.*)"
        target_label: job
```

Per app after that: the two labels above. Same ergonomics as serviceMonitor.enabled: true.

Two gotchas that will bite you: filter by network (without it every multi-network container produces duplicate targets), and don't hand Prometheus a raw Docker socket — put tecnativa/docker-socket-proxy in front with CONTAINERS=1 and everything else off.

DB — a fragment plus six lines
# platform/fragments.yaml
services:
  db-init:
    image: postgres:17-alpine
    entrypoint: ["/provision-db.sh"]
    volumes:
      - ./platform/provision-db.sh:/provision-db.sh:ro
    environment:
      PGHOST: postgres
      PGUSER: provisioner
      PGPASSWORD: ${PROVISIONER
    networks: [backend]
    restart: "no"

# apps/fulb/compose.yaml
services:
  fulb-db:
    extends: {file: ../../platform/fragments.yaml, service: db-init}
    environment:
      APP_DB: fulb
      APP_USER: fulb
      APP_PASS: ${FULB_DB_PASSWORD}
    depends_on:
      postgres: {condition: service_healthy}

  fulb:
    depends_on:
      fulb-db: {condition: service_completed_successfully}

provision-db.sh is the idempotent SQL from before. Six lines per app, and it's more automation than you have on Kubernetes today.

Watch out: extends deliberatelyor volumes_from). Declare itlocally, as above. That trips everyone once.

Opinions on the rest

Secrets: drop Vault, use SOPS + age. Vault costs you 94Mi, a pod, an unseal CronJob, ESO's three pods, and a ClusterSecretStore — to serve static strings to four apps. SOPS-encrypted secrets.env files committed next to each app is strictly better here: the secret lives in the same commit as the thing that uses it, which is what actually makes GitOps work. sops -d at deploy time. You lose dynamic credentials, which you weren't using.

GitOps: a systemd timer, not a platform.

deploy:
      git pull --ff-only
      sops -d secrets.enc.env >
      docker compose up -d --remove-orphans
      docker image prune -af --filter until=168h

Timer every 5 minutes. That las8GB problem — make image GC part of deploy instead of hoping k3s notices at 85% disk. If you want a UI later, Komodo is the reasonable pick; don't start there.

Grafana: provisioning directorio dashboard/datasource sidecarsare 150Mi of Python to watch for ConfigMaps. Mount grafana/provisioning/dashboards/*.json and it's a volume mount. Dashboards still live in git next to the app.

Logs: move to Alloy. Promtail is deprecated in favour of Grafana Alloy and is at or past end of life — worth checking your support window regardless of this migration. Alloy's discovery.docker gives you the same auto-discovery you get from Promtail's k8s SD, so logging stays zero-config per app.

Drop the dev environment from tv and prod branches on one 8GBbox. Dev should be docker compose up on your laptop — same files, no --profile prod. That's both cheaper and a better loop than pushing to a branch and waiting for a sync.

Backstage: delete, don't replace. A make new-service NAME=foo that copies a template directory is the honest version at four services.

Keep: Traefik (you know the label syntax, and its gandiv5 DNS provider does your DNS-01 natively), Postgres, Redis, Loki, Prometheus, Grafana.

The bill

┌──────────────────┬────────────────────┬───────────────────────────┐
│                  │        now         │           after           │
├──────────────────┼────────────────────┼───────────────────────────┤
│ orchestrator     │ k3s 1443Mi         │ dockerd+containerd ~250Mi │
├──────────────────┼────────────────────┼───────────────────────────┤
│ GitOps           │ ArgoCD 633Mi       │ systemd timer, 0          │
├──────────────────┼────────────────────┼───────────────────────────┤
│ portal           │ Backstage 323Mi    │ 0                         │
├──────────────────┼────────────────────┼───────────────────────────┤
│ secrets          │ Vault+ESO 203Mi    │ SOPS, 0                   │
├──────────────────┼────────────────────┼───────────────────────────┤
│ DB operators     │ CNPG 58Mi          │ 0                         │
├──────────────────┼────────────────────┼───────────────────────────┤
│ LB               │ MetalLB 118Mi      │ 0                         │
├──────────────────┼────────────────────┼───────────────────────────┤
│ TLS              │ cert-manager 128Mi │ in Traefik                │
├──────────────────┼────────────────────┼───────────────────────────┤
│ ingress          │ 2× Traefik 100Mi   │ 1× ~50Mi                  │
├──────────────────┼────────────────────┼───────────────────────────┤
│ Prometheus       │ 614Mi              │ ~200Mi                    │
├──────────────────┼────────────────────┼───────────────────────────┤
│ Grafana          │ 302Mi              │ ~150Mi                    │
├──────────────────┼────────────────────┼───────────────────────────┤
│ Loki + logs      │ 239Mi              │ ~250Mi                    │
├──────────────────┼────────────────────┼───────────────────────────┤
│ Postgres + Redis │ 188Mi              │ ~190Mi                    │
├──────────────────┼────────────────────┼───────────────────────────┤
│ your apps        │ 223Mi              │ 223Mi                     │
├──────────────────┼────────────────────┼───────────────────────────┤
│ total            │ ~5.9Gi             │ ~1.3Gi                    │
└──────────────────┴────────────────────┴───────────────────────────┘

Roughly 4.5Gi back on a 7.75Gi box, and the per-service surface goes from a values.yaml against a schema to about fifteen lines of Compose.
re the risk is. The risk is that you have 721M of Postgres on a single local-path volume with no backups, and that's true today and would be true after. Fix that first, before or during — a pg_dump to object storage on a nightly timer is the highest-value hour in this whole plan.

Want me to build the stack/ skeleton — platform compose, prometheus config, provision script, and the three apps ported — so you can diff it against what's running?