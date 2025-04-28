# 📈 Prometheus & Grafana Setup for Flask App (Kubernetes)

## 📚 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
- [Kubernetes Manifests](#kubernetes-manifests)
- [Install Helm](#install-helm)
- [Install Kube Prometheus Stack](#install-kube-prometheus-stack)
- [Expose Services](#expose-services)
- [Deploy Flask App](#deploy-flask-app)
- [Access Grafana Dashboard](#access-grafana-dashboard)
- [Prometheus Useful Queries](#prometheus-useful-queries)
- [Conclusion](#conclusion)

---

## Overview
This project demonstrates:
- Deploying a **Flask** web application on a **Kubernetes** cluster.
- Installing **Prometheus** and **Grafana** using Helm.
- Monitoring application metrics.
  
---

## Project Structure

```
.
├── k8s/
│   ├── deployment.yml    # Flask App Deployment
│   ├── namespace.yml     # Namespace definition
│   └── service.yml       # Flask App Service
├── templates/
│   ├── dns_lookup.html
│   ├── home.html
│   └── ip_lookup.html
├── Dockerfile             # Flask App Dockerfile
├── app.py                 # Flask Application
├── config.yaml            # Helm Values for Prometheus/Grafana
├── get_helm.sh            # Helm Installation Script
├── kind.sh                # Kind Cluster Setup Script
├── prom_grap.txt          # Prometheus/Grafana Notes
├── requirements.txt       # Python Dependencies
```

---

## Prerequisites

- [Docker](https://www.docker.com/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Kind](https://kind.sigs.k8s.io/) 
- [Helm](https://helm.sh/)
- Kubernetes and Helm knowledge.

---

## Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Prometheus_Grafana.git
cd Prometheus_Grafana
```

### 2. Set Up Kubernetes Cluster

```bash
bash kind.sh
```

---

## Kubernetes Manifests

### 1. Create Namespace

```bash
kubectl apply -f k8s/namespace.yml
```

### 2. Deploy Flask App

```bash
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
```

---

## Install Helm

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

Verify Helm:

```bash
helm version
```

---

## Install Kube Prometheus Stack

### Add Helm Repositories

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo update
```

### Create Monitoring Namespace

```bash
kubectl create namespace monitoring
```

### Install Prometheus Stack

```bash
helm install kind-prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.service.nodePort=30000 \
  --set prometheus.service.type=NodePort \
  --set grafana.service.nodePort=31000 \
  --set grafana.service.type=NodePort \
  --set alertmanager.service.nodePort=32000 \
  --set alertmanager.service.type=NodePort \
  --set prometheus-node-exporter.service.nodePort=32001 \
  --set prometheus-node-exporter.service.type=NodePort
```

### Verify Services

```bash
kubectl get svc -n monitoring
kubectl get namespace
```

---

## Expose Services

### Port-Forward Prometheus and Grafana

```bash
kubectl port-forward svc/kind-prometheus-kube-prome-prometheus -n monitoring 9090:9090 --address=0.0.0.0 &
kubectl port-forward svc/kind-prometheus-grafana -n monitoring 31000:80 --address=0.0.0.0 &
```

Now access:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:31000`

---

## Deploy Flask App

Make sure the Flask app deployment is running:

```bash
kubectl get pods -n default
```

---

## Access Grafana Dashboard

Open browser:

```plaintext
http://localhost:31000
```

Default Credentials:
- Username: `admin`
- Password: `prom-operator`

---

## Prometheus Useful Queries

> Use these queries inside Prometheus or Grafana panels:

- **CPU Usage (%)**
```promql
sum(rate(container_cpu_usage_seconds_total{namespace="default"}[1m])) / sum(machine_cpu_cores) * 100
```

- **Memory Usage (Bytes)**
```promql
sum(container_memory_usage_bytes{namespace="default"}) by (pod)
```

- **Network Receive (Bytes)**
```promql
sum(rate(container_network_receive_bytes_total{namespace="default"}[5m])) by (pod)
```

- **Network Transmit (Bytes)**
```promql
sum(rate(container_network_transmit_bytes_total{namespace="default"}[5m])) by (pod)
```

---

## Conclusion

✅ This project provides:
- Full Kubernetes deployment of a Flask app.
- Full monitoring setup with Prometheus and Grafana using Helm.
- Practical PromQL queries for real-time monitoring.

---
