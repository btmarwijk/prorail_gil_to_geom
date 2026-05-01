terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}
data "digitalocean_project" "spoorkabels" {
  name = "spoorkabels"
}

data "digitalocean_ssh_key" "main_key" {
  name = "Fedora" # Must match the name in the DO dashboard exactly
}

# Define a variable for the token so it's not hard-coded
variable "do_token" {}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "spoorkabel_app" {
  name   = "test-droplet"
  region = "ams"
  size   = "s-2vcpu-2gb"
  image  = "almalinux-9-x64"
  ssh_keys = [data.digitalocean_ssh_key.main_key.id]
}

resource "digitalocean_project_resources" "project_assets" {
  project = data.digitalocean_project.spoorkabels.id
  resources = [digitalocean_droplet.spoorkabel_app.urn]
}

output "droplet_ip" {
  value       = digitalocean_droplet.spoorkabel_app.ipv4_address
  description = "The public IP address of your Droplet"
}