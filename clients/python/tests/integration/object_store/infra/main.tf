terraform {
    required_providers {
        plausible = {
            source = "localhost/org/plausible"
            version = "0.1"
        }
    }
}

provider "plausible" {}

resource "plausible_object_store" "obj" {

}