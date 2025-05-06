# Helm chart for Home Assistant

![Latest Released Version](https://img.shields.io/github/v/tag/pajikos/home-assistant-helm-chart?sort=semver)
![Helm Chart Release](https://github.com/pajikos/home-assistant-helm-chart/actions/workflows/build-helm-chart-release.yaml/badge.svg)
![Auto-update latest HA version](https://github.com/pajikos/home-assistant-helm-chart/actions/workflows/check_ha_release.yml/badge.svg)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/helm-hass)](https://artifacthub.io/packages/search?repo=helm-hass)

## Introduction

This chart bootstraps a [Home Assistant](https://home-assistant.io) deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

It is updated **automatically** with each new release of Home Assistant, ensuring you always have access to the latest features and improvements.

## Features

- **Automatic Updates**: The chart is updated with each new release of Home Assistant.
- **Flexibility**: Extensive configuration options to tailor Home Assistant to your needs.
- **Addons Support**: Extend Home Assistant's functionality with supported addons, such as code-server.

## Quick Start

To deploy Home Assistant using this Helm chart, follow these steps:

```console
$ helm repo add pajikos http://pajikos.github.io/home-assistant-helm-chart/
$ helm repo update
$ helm install home-assistant pajikos/home-assistant
```

This will deploy Home Assistant with the default configuration. See the [Configuration](#configuration) section for details on customizing the deployment.


> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `home-assistant` deployment:

```console
$ helm delete home-assistant
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
| `controller.type` | Type of controller to use: StatefulSet or Deployment | `StatefulSet` |
| `statefulSetAnnotations` | Annotations to add to the StatefulSet | `{}` |
| `deploymentAnnotations` | Annotations to add to the Deployment | `{}` |
| `podSecurityContext` | Pod security context settings | `{}` |
| `env` | Environment variables | `[]` |
| `envFrom` | Use environment variables from ConfigMaps or Secrets | `[]` |
| `hostNetwork` | Specifies if the containers should be started in `hostNetwork` mode. | `false` |
| `dnsPolicy` | Specifies the [`dnsPolicy`](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy) for the pod. | `false` |
| `hostPort.enabled` | Enable 'hostPort' or not | `false` |
| `hostPort.port` | Port number | `8123` |
| `dnsConfig` | Override the default dnsConfig and set your own nameservers or ndots, among other options | `{}` |
| `service.type` | Service type (ClusterIP, NodePort, LoadBalancer, or ExternalName) | `ClusterIP` |
| `service.port` | Service port | `8080` |
| `service.annotations` | Annotations to add to the service | `{}` |
| `ingress.enabled` | Enable ingress for Home Assistant | `false` |
| `ingress.external` | Enable external ingress (cannot be true when ingress.enabled is true) | `false` |
| `resources` | Resource settings for the container | `{}` |
| `nodeSelector` | Node selector settings for scheduling the pod on specific nodes | `{}` |
| `tolerations` | Tolerations settings for scheduling the pod based on node taints | `[]` |
| `affinity` | Affinity settings for controlling pod scheduling | `{}` |
| `priorityClassName` | Priority class name for Home Assistant pods | `""` |
| `persistence.enabled` | Enables the creation of a Persistent Volume Claim (PVC) for Home Assistant. | `false` |
| `persistence.accessMode` | The access mode of the PVC. | `ReadWriteOnce` |
| `persistence.size` | The size of the PVC to create. | `5Gi` |
| `persistence.storageClass` | The storage class to use for the PVC. If empty, the default storage class is used. | `""` |
| `persistence.existingVolume` | The name of an existing Persistent Volume to bind to when using StatefulSet. This bypasses dynamic provisioning. | `""` |
| `persistence.existingClaim` | The name of an existing PVC to use when using Deployment. | `""` |
| `persistence.matchLabels` | Label selectors to apply when binding to an existing Persistent Volume. | `{}` |
| `persistence.matchExpressions` | Expression selectors to apply when binding to an existing Persistent Volume. | `{}` |
| `persistence.annotations` | Annotations to add to the PVC. | `{}` |
| `additionalVolumes` | Additional volumes to be mounted in the home assistant container | `[]` |
| `additionalMounts` | Additional volume mounts to be mounted in the home assistant container | `[]` |
| `initContainers` | List of initialization containers | `[]` |
| `configuration.enabled` | Enable or disable the configuration setup for Home Assistant | `false` |
| `configuration.forceInit` | Force init will merge the current configuration file with the default configuration on every start | `false` |
| `configuration.trusted_proxies` | List of trusted proxies in CIDR notation | `["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/8"]` |
| `configuration.templateConfig` | Template for the `configuration.yaml` file | See Advanced Configuration |
| `configuration.initScript` | Init script for Home Assistant initialization | See values.yaml for the complete configuration options  |
| `configuration.initContainer` | Configuration for the init container | See values.yaml for the complete configuration options |
| `addons.codeserver.enabled` | Enable or disable the code-server addon | `false` |
| `addons.codeserver.resources` | Resource settings for the code-server container | `{}` |
| `addons.codeserver.image.repository` | Repository for the code-server image | `ghcr.io/coder/code-server` |
| `addons.codeserver.image.pullPolicy` | Image pull policy for the code-server image | `IfNotPresent` |
| `addons.codeserver.image.tag` | Tag for the code-server image | `latest released version, automatically updated` |
| `addons.codeserver.service.type` | Service type for the code-server addon | `ClusterIP` |
| `addons.codeserver.service.port` | Service port for the code-server addon | `12321` |
| `addons.codeserver.ingress.enabled` | Enable or disable the ingress for the code-server addon | `false` |
| `addons.codeserver.ingress.hosts` | Hosts for the code-server addon | `[]` |
| `addons.codeserver.ingress.tls` | TLS settings for the code-server addon | `[]` |
| `addons.codeserver.ingress.annotations` | Annotations for the code-server addon | `{}` |

## Controller Type

This chart supports two types of controllers for deploying Home Assistant:

1. `StatefulSet` (default): Recommended for production use, especially when persistence is enabled. StatefulSets provide stable network identities and persistent storage that survives pod rescheduling.

2. `Deployment`: Simpler controller type that might be preferred in some scenarios. When using a Deployment with persistence enabled, a separate PVC is created instead of using volumeClaimTemplates.

To specify the controller type, set the `controller.type` value:

```yaml
controller:
  type: StatefulSet  # or Deployment
```

## Persistence

The default configuration of this chart uses an `emptyDir` volume for persistence, which means that data is lost when the pod is removed. To enable persistent storage that survives pod restarts and redeployments, you can configure the chart to use a Persistent Volume Claim (PVC).

### Enabling Persistence

To enable persistence, set `persistence.enabled` to `true`. You can also specify the desired `accessMode` and `size` for the PVC. By default, the `accessMode` is set to `ReadWriteOnce`, and there is no default storage class (`storageClass: ""`), meaning the cluster's default storage class will be used.

```yaml
persistence:
  enabled: true
  accessMode: ReadWriteOnce
  size: 5Gi
  storageClass: ""
```

### Using an Existing Volume or PVC

Depending on the controller type you're using, you can either bind to an existing Persistent Volume (PV) or use an existing Persistent Volume Claim (PVC):

#### With StatefulSet (default)

If you already have a Persistent Volume (PV) that you wish to use with a StatefulSet, you can specify the name of this existing volume in the `persistence.existingVolume` field. This will direct the chart to use the specified PV, bypassing dynamic volume provisioning.

```yaml
controller:
  type: StatefulSet
persistence:
  enabled: true
  existingVolume: "my-existing-volume"
```

#### With Deployment

If you're using a Deployment and already have a PVC that you wish to use, you can specify the name of this existing claim in the `persistence.existingClaim` field:

```yaml
controller:
  type: Deployment
persistence:
  enabled: true
  existingClaim: "my-existing-pvc"
```

Alternatively, if you want to bind to a specific PV with a Deployment, you can create a new PVC that binds to the PV by setting `persistence.existingVolume`:

```yaml
controller:
  type: Deployment
persistence:
  enabled: true
  existingVolume: "my-existing-volume"
```

When using an existing volume or claim, ensure that the `accessMode` and `size` specified in the chart values match the capabilities and capacity of the existing PV/PVC.

### Selectors

You can further refine the selection of an existing PV using `matchLabels` or `matchExpressions` under the `persistence` section. These selectors will be used to match the existing PVs based on their labels.

```yaml
persistence:
  enabled: true
  matchLabels:
    type: fast-ssd
  matchExpressions:
    - key: "failure-domain.beta.kubernetes.io/zone"
      operator: "In"
      values: ["us-west-1a"]
```

### PVC Annotations

You can add annotations to the PVC by specifying them in the `persistence.annotations` field. This is useful for backup solutions like k8up that use annotations to identify resources for backup.

```yaml
persistence:
  enabled: true
  annotations:
    k8up.io/backup: "true"
    another-annotation: "value"
```

> **Note**: When specifying an `existingVolume`, ensure that the PV is not already bound to another PVC, as a PV can only be bound to a single PVC at a time.

## Ingress

The chart provides two mutually exclusive ways to configure ingress:

1. `ingress.enabled`: Traditional Kubernetes ingress configuration
2. `ingress.external`: For scenarios where the ingress is managed externally

Note: These two options cannot be enabled simultaneously. Attempting to set both to `true` will result in a validation error.

Example configuration:

```yaml
ingress:
  enabled: true   # Traditional ingress
  external: false # External ingress
```

In addition, you can specify the `ingress.hosts` and `ingress.tls` values. The default values are `[]` and `[]` respectively.
The second option is to set `service.type` to `NodePort` or `LoadBalancer` (when ingress is not available in your cluster)

## HostPort and HostNetwork

To enable hostPort, set `hostPort.enabled` to `true`. In addition, you can specify the `hostPort.port` value. The default value is `8123`.
To enable hostNetwork, set `hostNetwork` to `true`.
HostNetwork is required for auto-discovery of Home Assistant, when not using auto-discovery, hostNetwork is not required and not recommended.

## ServiceMonitor

If you have the Prometheus Operator installed, you can enable a ServiceMonitor to scrape Home Assistant metrics by setting `serviceMonitor.enabled` to `true`. This requires the [Prometheus integration](https://www.home-assistant.io/integrations/prometheus/) to be configured in Home Assistant.

```yaml
serviceMonitor:
  enabled: true
  scrapeInterval: 30s
  labels:
    release: prometheus
  # Bearer token authentication configuration (optional)
  bearerToken:
    secretName: "prometheus-token"
    secretKey: "token"
```

### Bearer Token Authentication

To use bearer token authentication for the ServiceMonitor, simply provide both:
- `secretName`: The name of the Kubernetes secret containing the token
- `secretKey`: The key within that secret containing the actual token

This lets you secure the metrics endpoint with a bearer token that Prometheus will use for authentication.


## Addons

The Home Assistant chart supports the following addons:

* [code-server](https://github.com/coder/code-server)

## Additional volumes and volume mounts

To add additional volumes and volume mounts, you can use the `additionalVolumes` and `additionalMounts` values. The default values are `[]`.
Example mounting usb devices:

```yaml

additionalVolumes:
  - hostPath:
      path: >-
        /dev/serial/by-id/usb-ITEAD_SONOFF_Zigbee_3.0_USB_Dongle_Plus_V2_20230509111242-if00
      type: CharDevice
    name: usb

additionalMounts:
  - mountPath: /dev/ttyACM0
    name: usb

```

Note: When mounting usb devices, you need to set the `securityContext.privileged` value to `true`.

## Advanced Configuration

### Init Containers

Use init containers to perform tasks before starting Home Assistant, such as waiting for a dependency:

```yaml
initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']
```

### Home Assistant Configuration

Customize Home Assistant's configuration directly through the Helm chart:

```yaml
# Configuration for Home Assistant
configuration:
  # Enable or disable the configuration setup for Home Assistant
  enabled: true
  # Force init will merge the current configuration file with the default configuration on every start
  # This is useful when you want to ensure that the configuration file is always up to date
  forceInit: true
  # List of trusted proxies in the format of CIDR notation in a case of using a reverse proxy
  # Here is the list of the most common private IP ranges, use your list of possible trusted proxies, usually, it's the IP of the reverse proxy
  trusted_proxies:
    - 10.42.0.0/16      # Add the IP address of your cluster CIDR
  # Editing templateConfig allows you to customize the configuration.yaml file
  # You can use Go template functions to customize the configuration
  templateConfig: |-
    # Loads default set of integrations. Do not remove.
    default_config:

    {{- if .Values.ingress.enabled }}
    http:
      use_x_forwarded_for: true
      trusted_proxies:
        {{- range .Values.configuration.trusted_proxies }}
        - {{ . }}
        {{- end }}
    {{- end}}
    # Load frontend themes from the themes folder
    frontend:
      themes: !include_dir_merge_named themes

    automation: !include automations.yaml
    script: !include scripts.yaml
    scene: !include scenes.yaml
```

This allows for dynamic configuration based on your Helm values.


## code-server

To enable the code-server addon, set `addons.codeserver.enabled` to `true`. In addition, you can specify the `addons.codeserver.resources` values. The default value is `{}`.
To be able to access the code-server addon, you need to enable the ingress for the code-server addon by setting `addons.codeserver.ingress.enabled` to `true` or setting `service.type` to `NodePort` or `LoadBalancer`.

## Upgrade Notes (v0.3)

This release adds support for both `StatefulSet` (default/legacy) and `Deployment` controllers, and clarifies persistence usage.

### Key Changes
- New value: `controller.type`—default remains `StatefulSet` for backward compatibility; use `Deployment` by setting `controller.type: Deployment`.
- The auto-generated PVC for `controller.type: Deployment` is now named `<fullname>-pvc` (vs. prior defaults for StatefulSet). Update all references if switching controller type!
- `persistence.existingClaim` is only supported with Deployment; `persistence.existingVolume` with StatefulSet.
- Manual cleanup may be needed if switching controller kind (e.g. legacy StatefulSet/PVC may remain until manually deleted).

### Migration Guidance
- If you keep using StatefulSet, no changes required.
- If switching to Deployment:
  - Update any automation or manifests to refer to the new PVC name (`-pvc` suffix).
  - Review and clean up old StatefulSet/volume resources as needed after migration.

See "Controller Type" and "Persistence" sections above for full explanation.
