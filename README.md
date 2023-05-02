# Helm chart for Home Assistant
Home Assistant is an open-source home automation platform running on Python 3.
It is able to track and control all devices at home and offer a platform for automating control.

## Introduction

This chart bootstraps a [Home Assistant](https://home-assistant.io) deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

## Prerequisites

- Kubernetes 1.4+ with Beta APIs enabled
- PV provisioner support in the underlying infrastructure
- Helm 3
  
## Installing the Chart

To install the chart with the release name `my-release`:

```console
$ helm install my-release stable/home-assistant
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

| Parameter                        | Description                                                                                                        | Default                                  |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------|------------------------------------------|
| `replicaCount`                   | Number of replicas for the deployment                                                                              | `1`                                      |
| `image.repository`               | Repository for the Home Assistant image                                                                            | `ghcr.io/home-assistant/home-assistant`  |
| `image.pullPolicy`               | Image pull policy                                                                                                  | `IfNotPresent`                           |
| `image.tag`                      | Overrides the image tag whose default is the chart appVersion                                                      | `""`                                     |
| `imagePullSecrets`               | List of imagePullSecrets for private image repositories                                                            | `[]`                                     |
| `nameOverride`                   | Override the default name of the Helm chart                                                                        | `""`                                     |
| `fullnameOverride`               | Override the default full name of the Helm chart                                                                   | `""`                                     |
| `serviceAccount.create`          | Specifies whether a service account should be created                                                              | `true`                                   |
| `serviceAccount.annotations`     | Annotations to add to the service account                                                                          | `{}`                                     |
| `serviceAccount.name`            | The name of the service account to use                                                                             | `""`                                     |
| `podAnnotations`                 | Annotations to add to the pod                                                                                      | `{}`                                     |
| `podSecurityContext`             | Pod security context settings                                                                                      | `{}`                                     |
| `env`                             | Environment variables                                                                                              | `[]`                                     |
| `envFrom`                         | Use environment variables from ConfigMaps or Secrets                                                               | `[]`                                     |
| `securityContext`                | Container security context settings                                                                                | `{}`                                     |
| `service.type`                   | Service type (ClusterIP, NodePort, LoadBalancer, or ExternalName)                                                 | `ClusterIP`                              |
| `service.port`                   | Service port
| `ingress.enabled`                     | Enable or disable ingress                                                                  | `false`                      |
| `ingress.className`                   | Ingress class name                                                                         | `""`                         |
| `ingress.annotations`                 | Ingress annotations                                                                        | `{}`                         |
| `ingress.hosts`                       | Ingress hosts configuration                                                                | `[chart-example.local]`      |
| `ingress.paths`                       | Ingress paths configuration                                                                | `[{"path": "/", "pathType": "ImplementationSpecific"}]` |
| `ingress.tls`                         | Ingress TLS configuration                                                                  | `[]`                         |
| `resources`                           | Resource settings for the container                                                        | `{}`                         |
| `nodeSelector`                        | Node selector settings for scheduling the pod on specific nodes                            | `{}`                         |
| `tolerations`                         | Tolerations settings for scheduling the pod based on node taints                           | `[]`                         |
| `affinity`                            | Affinity settings for controlling pod scheduling                                           | `{}`                         |
| `persistence.enabled`                 | Enable or disable persistence                                                              | `true`                       |
| `persistence.accessMode`              | Access mode for the persistent volume claim                                                | `ReadWriteOnce`              |
| `persistence.size`                    | Size of the persistent volume claim                                                        | `5Gi`                        |
| `persistence.storageClass`            | Storage class for the persistent volume claim                                              | `""`                         |
| `addons.codeserver.enabled`           | Enable or disable the code-server addon                                                    | `false`                      |
| `addons.codeserver.resources`         | Resource settings for the code-server container                                            | `{}`                         |
| `addons.codeserver.image.repository`  | Repository for the code-server image                                                       | `ghcr.io/coder/code-server`  |
| `addons.codeserver.image.pullPolicy`  | Image pull policy for the code-server image                                                | `IfNotPresent`               |
| `addons.codeserver.image.tag`         | Tag for the code-server image                                                              | `"4.7.1"`                    |
| `addons.codeserver.ingress.enabled`   | Enable or disable the ingress for the code-server addon                                    | `false`                      |
| `addons.codeserver.ingress.className` | Ingress class name for the code-server addon                                               | `""`                         |
| `addons.codeserver.ingress.annotations` | Ingress annotations for the code-server addon                                            | `{}`                         |
| `addons.codeserver.ingress.hosts`     | Ingress hosts configuration for the code-server addon                                      | `[chart-example.local]`      |
| `addons.codeserver.ingress.paths`     | Ingress paths configuration for the code-server addon                                      | `[{"path": "/", "pathType": "ImplementationSpecific"}]` |
| `addons.codeserver.ingress.tls`       | Ingress TLS configuration for the code-server addon                                        | `[]`                         |
