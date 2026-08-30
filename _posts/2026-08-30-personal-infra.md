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
# what i want
- redis, postgres db, prometheus, grafana configured for you through annotations

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


Good — that clears things up. fuservice is fulb: Phoenix 1.8.3, Ecto + Postgrex, Redix, and Phoenix.CodeReloader in listeners:. And you already have Ecto.Adapters.SQL.Sandbox and a precommit alias. The testing infrastructure is in decent shape.

The thing that unlocks this: Tilt speaks Compose natively

You don't give up Tilt. docker_compose() is a first-class Tilt primitive — docker_build, live_update, the UI, log multiplexing, resource deps all work against Compose services. So "move to Compose" and "keep Tilt" aren't in tension at all.

Opinion 1: don't containerize the thing you're currently editing

This is the big one. For a Phoenix app, live_update file-syncing into a container is strictly worse than the BEAM's own code reloader. You'd be adding a sync hop to beat a system that already recompiles a changed module in milliseconds inside a live VM that keeps your state.

The right split is: dependencies in Compose, the app you're working on native, Tilt supervising both. Tilt's local_resource(serve_cmd=...) runs and supervises
non-containerized processes, sle thing.

# Tiltfile
docker_compose(['platform/compose.yaml', 'apps/fulb/compose.yaml'])

dc_resource('postgres', labels=['deps'])
dc_resource('redis',    labels=['deps'])

# the real image — off by default, flip it on to test what ships
dc_resource('fulb', auto_init=False, labels=['containerized'])
docker_build('registry.gitlab.com/jsbaasi/engineering/fulb', '.')

local_resource(
    'fulb',
    serve_cmd='mix phx.server',
    serve_env={
        'DATABASE_URL': 'ecto::5432/fulb_dev',
        'REDIS_HOST': 'localho
        'PHX_HOST': 'localhost',
        'PORT': '4000',
    },
    resource_deps=['postgres',
app'],
)

local_resource('test', 'mix test', auto_init=False,
               trigger_mode=TRIGGER_MODE_MANUAL,
               resource_deps=['postgres'], labels=['checks'])
local_resource('precommit', 'mix precommit', auto_init=False,
               trigger_mode=TRIGGER_MODE_MANUAL, labels=['checks'])

tilt up → Postgres and Redis in Docker, Phoenix native with hot reload, mix test and mix precommit as one-click buttons in the UI. That's a better loop than you've ever had on k3s, and it's ~30 lines.

Note this Tiltfile actually woate one — that's still the stock tilt init scaffold pointing at a ./app directory and a codegen.sh that don't exist, plus it installs external-secrets via Helm locally. Whatever you build, don't port that.

Opinion 2: compose.override.yanches
st valuable Compose idiom, and it directly kills a pattern I'd call a bug in your current setup — you have dev and prod branches that your own docs say "are not in sync with each other." Divergent branches as an environment mechanism means dev drift is invisible until you promote.

apps/fulb/
├── compose.yaml            # base — the truth, shared
├── compose.override.yaml   # dev — auto-loaded locally, NEVER in prod
└── secrets.env

# compose.override.yaml
services:
  fulb:
    build: .
    ports: ["4000:4000"]
    environment:
      MIX_ENV: dev
      PHX_HOST: localhost
e up locally picks up the override automatically. Production runs docker compose -f compose.yaml up, which doesn't. Same file, same commit, one branch. Dev/prod difference becomes a diff you can read in one screen instead of a branch comparison.

Opinion 3: per-app, be honest about what each one needs

fulb — native, as above. Phoenix already ships phoenix_live_dashboard; at /dev/dashboard you get request timings, Ecto query logs, BEAM memory and process counts for free. Don't run Prometheus/Grafana locally by default. Put the obs stack behind --profile obs and only start it when you're specifically working on dashboards or alert rules. LiveDashboard beats Grafana for the inner loop.

fudbot — C++/DPP is the opposiis the problem: it git clones
and compiles DPP from source onutes. Two fixes, do both:

- Split DPP into a base image you build once and push (fudbot-base:dpp-10.1.4), so app builds are seconds.
- Locally, don't containerize on the host with a warm cache'] gives you rebuild-on-save in the Tilt UI.

continuwuity — third-party image. docker compose up. Nothing to develop.

Opinion 4: your testing gap is tests, not tooling

Being blunt because you asked for opinions: you have one test file, error_json_test.exs, which is the one mix phx.new generated. Everything around it is set up correctly — Sandbox in manual mode, test: ["ecto.create --quiet", "ecto.migrate --quiet", "test"], a precommit alias that compiles with --warnings-as-errors. You have a well-built harness with nothing in it.

So: skip Testcontainers. Peoplation, and
Ecto.Adapters.SQL.Sandbox alresolation per test — that's thesame problem, solved better, already installed. Point MIX_ENV=test at the same Compose Postgres on a fulb_test database and you're done. Add Testcontainers only if you later need parallel CI runs against separate engines.
against real Postgres and Redis. You have conn_case.ex and data_case.ex sitting there unused.

Opinion 5: small things that punch above their weight

*.localhost needs no config. Linux, macOS and Chrome all resolve anything.localhost to 127.0.0.1. Run Traefik locally with the same routing labels as prod, just Host(\fulb.localhost`)and no TLS resolver. You test your actual routing config without/etc/hosts` edits or certs.

direnv. A committed .envrc with fake-but-valid dev values means cd into the repo and your shell is configured. This is what replaces Vault locally — dev secrets should be fake and
committed, not fetched.

Make the DB reset trivial. You already have mix ecto.reset wired to
drop/create/migrate/seed. Makeduces a genuinely usabledataset, not an empty schema. A fast path back to known-good state is most of what "great local testing" feels like day to day.

One command, top of the README

git clone && direnv allow && tilt up

If that isn't the whole onboarding, something in the chain is wrong.

Why this is better than what you have

Your current local story requires rendering the Helm chart with vault.enabled=false, serviceMonitor.enabled=false, pullPolicy=IfNotPresent — local runs a materially different artifact than prod, because you can't reasonably run k3s + ArgoCD + Vault + cert-manager + ESO on a laptop. That divergence is inherent to the platform, not a thing you configured
badly.

With Compose, local is prod minus an override file and a couple of profiles. The dev
environment isn't a simulatione definition with the expensiveparts switched off.

Want me to write the actual Tiltfile, compose.yaml + compose.override.yaml for fulb, and the DPP base-image split for fudbot? That's the concrete starting point and I can have it diffable against what's running.

✻ Worked for 2m 12s · done 8:50

❯ what is direnv? tell me more about secrets, how are they managed then? more opinions, on local and prod, whats easiest for me and i dont need some usa governemtn area 51 security, no one is ever getting into my vps probbly

Let me check one thing that's directly relevant to the Vault argument.

  Read 1 file, ran 1 shell command

Working directory drifted to fuservice. Let me re-read with absolute paths.

  Ran 1 shell command

direnv, quickly

It's a shell hook. You drop a .envrc in a directory; when you cd in, direnv exports those variables into your shell, and when you cd out it unloads them. That's the whole product.

sudo apt install direnv
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc   # or zsh

Then in the repo:

# .envrc — committed, fake values only
export DATABASE_URL=ecto://postgres:postgres@localhost:5432/fulb_dev
export REDIS_HOST=localhost
export PORT=4000
export PHX_HOST=localhost

dotenv_if_exists .envrc.local   # gitignored, real tokens if you need them

First time you enter, direnv refuses and tells you to run direnv allow — it won't execute a
.envrc you haven't explicitly silently run something in your
for you: mix phx.server just works, with no wrapper script and no remembering to export things. That committed-defaults + gitignored-overrides pattern is the whole local secrets story.

Your Vault isn't doing what you think it is

Not a lecture, just what's in your repo. podstates/infra/vault/:

- standalone, file storage, tls_disable = 1
- unseal keys sit in a plain Kubernetes Secret called vault-unseal-keys
- a CronJob runs every 10 minutes, reads those keys, and unseals it

So the lock is opened automatit to it holding all three keys,in the same cluster, over plain HTTP. Whatever Vault is providing, it isn't confidentiality-at-rest — it's an encrypted-on-disk KV store whose decryption key lives beside it. For that you're paying Vault 94Mi + ESO's three pods at 93Mi + an unseal CronJob
+ a ClusterSecretStore + a perchart.tgres, apps/fulb/prod, apps/fudbot/prod. Delete Backstage and ArgoCD and it's about six.

Your instinct is right. This one's easy.

What I'd do: SOPS + age

And here's my actual reasoning, which is not security — you're correct that nobody's coming for your VPS.

The reason is that encryption is what makes a secret safe to put in git, and git is what
gives you versioning, backup, eploys. The alternative —
plaintext .env on the server, an unversioned, unbacked-up file that is one rm or one dead VPS away from a bad weekend. Given that losing data to a single unbacked-up VPS is already the running theme of this whole conversation, I'd rather the secrets not be in that category.


Setup, once, about ten minutes:

age-keygen -o ~/.config/sops/age/keys.txt      # prints your public key, age1...

# .sops.yaml at the repo root
creation_rules:
  - path_regex: \.enc\.env$
    age: age1qz...your-public-key

Daily use is two commands:

sops apps/fulb/secrets.enc.envs encrypted
sops -d --input-type dotenv --output-type dotenv apps/fulb/secrets.enc.env

Copy keys.txt to the VPS and to your password manager. That one file is now the thing that
must not be lost — but it's 20ich is a much easier backup
rick

Make leaking structurally impossible rather than a matter of discipline:

gitignore
*.env
!*.enc.env

Now a plaintext secrets file physically cannot be committed, and the encrypted one always can. This is worth more than any scanning tool, because it fails closed.

Local

Never real secrets. Committed .envrc with fake values, and docker compose bringing up a Postgres whose password is literally postgres. It's on loopback on your laptop; a strong password there is pure ceremony.
stration — a dev bot in a private dev server, its own token, in gitignored .envrc.local. If it leaks, you delete a bot nobody uses. Same idea for any third-party API: dev credentials, separate account, blast radius zero.

Prod

deploy:
      git pull --ff-only
      @for d in apps/*/; do \
        [ -f "$$d/secrets.enc.env" ] && \
          sops -d --input-type dotenv --output-type dotenv "$$d/secrets.enc.env" > "$$d/.en
      done      docker compose up -d --r
      docker image prune -af --filter until=168h

chmod 600 the outputs if you like, but be clear-eyed that it buys little: anything in a container's environment is vis anything that can reach the
e on that 1Gi PVC is the only copy of several of those values. Get them out before you tear anything down:

for p in infra/registry gitlab-oauth gandi alerting monitoring postgres \
         apps/fulb/prod apps/fudbot/prod; do
  vault kv get -format=json "secret/$p" | jq -r '.data.data'
done

Dump to plaintext first, verif the values you extracted, thenSOPS-encrypt and then delete Vault. Don't do it in one step. And check the Gandi token and Discord webhook specifically — those two aren't recoverable from anywhere else without re-issuing.


The two failure modes that are actually likely for you are pasting a token into a public commit (the risk there is a scraper bot abusing your Discord token within minutes — not a targeted attack) and losing the only copy of something. The gitignore rule handles the first. SOPS-in-git handles the second. That's proportionate, and it's less machinery than you're running today.