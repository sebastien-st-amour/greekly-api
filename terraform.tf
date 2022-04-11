terraform {
    backend "s3" {
        bucket = "terraformecsproject-1"
        key    = "state.tfstate"
    }
}