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

| Parameter                            | Description                                                                 | Default                                                 |
| ------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------- |
| `image.repository`                   | Home Assistant image repository                                             | `homeassistant/home-assistant`                          |
| `image.tag`                          | Home Assistant image tag (immutable tags are recommended)                   | `0.118.5`                                               |
| `image.pullPolicy`                   | Home Assistant image pull policy                                            | `IfNotPresent`                                          |
| `image.pullSecrets`                  | Specify docker-registry secret names as an array                            | `[]` (does not add image pull secrets to deployed pods) |
| `nameOverride`                       | String to partially override home-assistant.fullname template with a string | `nil`                                                   |
| `fullnameOverride`                   | String to fully override home-assistant.fullname template with a string     | `nil`                                                   |
| `service.type`                       | Kubernetes Service type                                                     | `ClusterIP`                                             |
| `service.port`                       | Home Assistant port                                                         | `8123`                                                  |
| `service.nodePort`                   | Kubernetes Service nodePort                                                 | `nil`                                                   |
| `service.annotations`                | Service annotations                                                         | `{}`                                                    |
| `service.loadBalancerIP`             | LoadBalancerIP if service type is `LoadBalancer`                            | `nil`                                                   |
| `service.loadBalancerSourceRanges`   | Address that are allowed when service is LoadBalancer                       | `[]`                                                    |
| `service.externalTrafficPolicy`      | Enable client source IP preservation                                        | `Cluster`                                               |
| `service.clusterIP`                  | Kubernetes Service clusterIP                                                | `nil`                                                   |
| `service.externalIPs`                | Kubernetes Service externalIPs                                              | `[]`                                                    |
| `service.healthCheckNodePort`        | Kubernetes Service healthCheckNodePort                                      | `nil`                                                   |
| `service.externalName`               | Kubernetes Service externalName                                             | `nil`                                                   |
| `service.loadBalancerSourceRanges`   | Kubernetes Service loadBalancerSourceRanges                                 | `[]`                                                    |
| `service.loadBalancerIP`             | Kubernetes Service loadBalancerIP                                           | `nil`                                                   |
| `service.annotations`                | Kubernetes Service annotations                                              | `{}`                                                    |
| `ingress.enabled`                    | Enable ingress controller resource                                          | `false`                                                 |
| `ingress.annotations`                | Ingress annotations                                                         | `[]`                                                    |
| `ingress.hosts`                      | Ingress accepted hostnames                                                  | `[]`                                                    |
| `ingress.tls`                        | Ingress TLS configuration                                                   | `[]`                                                    |
| `resources`                          | CPU/Memory resource requests/limits                                         | `{}`                                                    |
| `nodeSelector`                       | Node labels for pod assignment                                              | `{}`                                                    |
| `tolerations`                        | Toleration labels for pod assignment                                        | `[]`                                                    |
| `affinity`                           | Affinity settings for pod assignment                                        | `{}`                                                    |
| `securityContext`                    | Security context for pod assignment                                         | `{}`                                                    |
| `podAnnotations`                     | Pod annotations                                                             | `{}`                                                    |
| `podLabels`                          | Pod labels                                                                  | `{}`                                                    |
| `priorityClassName`                  | Priority class name                                                         | `nil`                                                   |
| `livenessProbe.enabled`              | Enable livenessProbe                                                        | `true`                                                  |
| `livenessProbe.initialDelaySeconds`  | Initial delay seconds for livenessProbe                                     | `30`                                                    |
| `livenessProbe.periodSeconds`        | Period seconds for livenessProbe                                            | `30`                                                    |
| `livenessProbe.timeoutSeconds`       | Timeout seconds for livenessProbe                                           | `5`                                                     |
| `livenessProbe.failureThreshold`     | Failure threshold for livenessProbe                                         | `3`                                                     |
| `livenessProbe.successThreshold`     | Success threshold for livenessProbe                                         | `1`                                                     |
| `readinessProbe.enabled`             | Enable readinessProbe                                                       | `true`                                                  |
| `readinessProbe.initialDelaySeconds` | Initial delay seconds for readinessProbe                                    | `30`                                                    |
| `readinessProbe.periodSeconds`       | Period seconds for readinessProbe                                           | `30`                                                    |
| `readinessProbe.timeoutSeconds`      | Timeout seconds for readinessProbe                                          | `5`                                                     |
| `readinessProbe.failureThreshold`    | Failure threshold for readinessProbe                                        | `3`                                                     |
| `readinessProbe.successThreshold`    | Success threshold for readinessProbe                                        | `1`                                                     |
| `extraEnvs`                          | Extra environment variables to be set on Home Assistant container           | `[]`                                                    |
| `extraVolumeMounts`                  | Extra volume mounts to be set on Home Assistant container                   | `[]`                                                    |


