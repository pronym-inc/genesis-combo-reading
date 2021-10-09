This is a set of Ansible scripts for deploy the genesis_combo_reading Django application.

You can also use this to set up a local vagrant development:

We assume a modest amount of prerequisities:

1. You have [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installed.
1. You have [Vagrant](https://www.vagrantup.com/downloads.html) installed
1. You have an [SSH key](https://help.github.com/en/articles/adding-a-new-ssh-key-to-your-github-account) and have it set up with your GitHub account (this will be used by Ansible to download the code)
1. That SSH key is located in `~/.ssh/id_rsa` (which is the default location for your SSH key).
1. You have `make` installed

You should then be able to run

```
make spinup
```

which will create the virtual machine, configure it with Ansible scripts, and then load the site in browser.  You will be able to login with the credentials "admin" / "password123"

Note:

The `Makefile` was written for use on OSX, but it should be easy to achieve the same effect with a little more effort on other operating systems.  Basically, it just does a few things:

1. Add an entry to /etc/hosts file so our local DNS works correctly.  This will be a different file you need to edit on Windows.
1. Copy our SSH private key to the local directory.  We do this because we use it as the private key on the vagrant server, so we can use the git repositories.
1. Run `vagrant up`
1. There is a final step where we open up [http://genesiscomboreadingvagrant.local](http://genesishealth.local) in Chrome, and that will surely fail on non-OSX Linux machines, but only after the rest of the command has finished.