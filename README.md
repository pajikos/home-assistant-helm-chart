# Helm chart for Home Assistant

![Latest Released Version](https://img.shields.io/github/v/tag/pajikos/home-assistant-helm-chart?sort=semver)
![Helm Chart Release](https://github.com/pajikos/home-assistant-helm-chart/actions/workflows/build-helm-chart-release.yaml/badge.svg)
![Auto-update latest HA version](https://github.com/pajikos/home-assistant-helm-chart/actions/workflows/check_ha_release.yml/badge.svg)

Home Assistant is an open-source home automation platform running on Python 3.
It is able to track and control all devices at home and offer a platform for automating control.

## Introduction

This chart bootstraps a [Home Assistant](https://home-assistant.io) deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

## Prerequisites

- Kubernetes 1.4+ with Beta APIs enabled
- PV provisioner support in the underlying infrastructure
- Helm 3
  
## Installing the Chart

To install the chart with the release name `home-assistant`:

```console
$ helm repo add pajikos http://pajikos.github.io/home-assistant-helm-chart/
$ helm repo update
$ helm install home-assistant pajikos/home-assistant
```

The command deploys Home Assistant on the Kubernetes cluster in the default configuration. The [configuration](#configuration) section lists the parameters that can be configured during installation.

> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```console
$ helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

The following table lists the configurable parameters of the Home Assistant chart and their default values.

# Home Assistant Helm Chart

This document provides detailed configuration options for the Home Assistant Helm chart.

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `replicaCount` | Number of replicas for the deployment | `1` |
| `image.repository` | Repository for the Home Assistant image | `ghcr.io/home-assistant/home-assistant` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `image.tag` | Overrides the image tag (default is the chart appVersion) | `""` |
| `image.imagePullSecrets` | List of imagePullSecrets for private image repositories | `[]` |
| `nameOverride` | Override the default name of the Helm chart | `""` |
| `fullnameOverride` | Override the default full name of the Helm chart | `""` |
| `serviceAccount.create` | Specifies whether a service account should be created | `true` |
| `serviceAccount.annotations` | Annotations to add to the service account | `{}` |
| `serviceAccount.name` | The name of the service account to use | `""` |
| `podAnnotations` | Annotations to add to the pod | `{}` |
| `podSecurityContext` | Pod security context settings | `{}` |
| `env` | Environment variables | `[]` |
| `envFrom` | Use environment variables from ConfigMaps or Secrets | `[]` |
| `hostNetwork` | Specifies if the containers should be started in `hostNetwork` mode. | `false` |
| `hostPort.enabled` | Enable 'hostPort' or not | `false` |
| `hostPort.port` | Port number | `8123` |
| `service.type` | Service type (ClusterIP, NodePort, LoadBalancer, or ExternalName) | `ClusterIP` |
| `service.port` | Service port | `8080` |
| `ingress.enabled` | Enable ingress for Home Assistant | `false` |
| `resources` | Resource settings for the container | `{}` |
| `nodeSelector` | Node selector settings for scheduling the pod on specific nodes | `{}` |
| `tolerations` | Tolerations settings for scheduling the pod based on node taints | `[]` |
| `affinity` | Affinity settings for controlling pod scheduling | `{}` |
| `persistence.enabled` | Enable or disable persistence | `true` |
| `persistence.accessMode` | Access mode for the persistent volume claim | `ReadWriteOnce` |
| `persistence.size` | Size of the persistent volume claim | `5Gi` |
| `persistence.storageClass` | Storage class for the persistent volume claim | `""` |
| `addons.codeserver.enabled` | Enable or disable the code-server addon | `false` |
| `addons.codeserver.resources` | Resource settings for the code-server container | `{}` |
| `addons.codeserver.image.repository` | Repository for the code-server image | `ghcr.io/coder/code-server` |
| `addons.codeserver.image.pullPolicy` | Image pull policy for the code-server image | `IfNotPresent` |
| `addons.codeserver.image.tag` | Tag for the code-server image | `"4.12.0"` |
| `addons.codeserver.ingress.enabled` | Enable or disable the ingress for the code-server addon | `false` |
