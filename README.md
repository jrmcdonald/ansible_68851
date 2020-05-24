# Demo for Ansible#68851

## Overview

This is a demonstration repo for [https://github.com/ansible/ansible/issues/68851](https://github.com/ansible/ansible/issues/68851).

The real world example is attempting to use the hcloud inventory plugin to fetch servers for use in [kubernetes-sigs/kubespray](https://github.com/kubernetes-sigs/kubespray). Kubespray requires a very specific inventory format with invalid characters in the group names. The example from their documentation is as follows (note the dashes/colons):

```
## Configure 'ip' variable to bind kubernetes services on a
## different ip than the default iface
node1 ansible_host=95.54.0.12 ip=10.3.0.1
node2 ansible_host=95.54.0.13 ip=10.3.0.2
node3 ansible_host=95.54.0.14 ip=10.3.0.3
node4 ansible_host=95.54.0.15 ip=10.3.0.4
node5 ansible_host=95.54.0.16 ip=10.3.0.5
node6 ansible_host=95.54.0.17 ip=10.3.0.6

[kube-master]
node1
node2

[etcd]
node1
node2
node3

[kube-node]
node2
node3
node4
node5
node6

[k8s-cluster:children]
kube-node
kube-master
```

## Running

Tested with Ansible 2.9.6.

Execute `ansible-inventory -i inventories/example.yaml --graph -vvvv` and observe the output:

```
...
Replacing invalid character(s) "{':', '-'}" in group name (k8s-cluster:children)
[WARNING]: Invalid characters were found in group names and automatically replaced, use -vvvv to see details
...
@all:
  |--@k8s_cluster_children:
  |  |--master-1
  |--@ungrouped:
```

Note that the group according to the example.yaml should have been `k8s-cluster:children`.

## The Problem

The plugin `example.py` extends Constructable and calls `self._add_host_to_composed_groups`.

This eventually hits line 357 of `__init__.py` which calls `group_name = original_safe(group_name, force=True)`, note the `force=True`.

This eventually hits line 40 of `group.py` - `if C.TRANSFORM_INVALID_GROUP_CHARS not in ('never', 'ignore') or force:` where it ignores the value of `never` for `TRANSFORM_INVALID_GROUP_CHARS` because force is true.