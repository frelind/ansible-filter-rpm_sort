# ansible-filter-rpm_sort
Custom Jinja2 filter for sorting RPM packages by version

I've modified the rpmdev-sort script from rpmdevtools to a jinja2 filter.

## Usage
Copy the `filter_plugins` directory to a role or same location as playbooks.

```
tasks:
- name: get list of installed kernel packages
  command: rpm -q kernel
  register: packages
  changed_when: no

- name: print latest kernel package
  debug:
    msg: "{{ packages.stdout | rpm_sort | last }}"
```

```
TASK [print latest kernel package] *************************
ok: [localhost] => {
    "msg": "kernel-5.8.12-200.fc32.x86_64"
}
```
