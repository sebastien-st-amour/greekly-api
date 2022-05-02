output "postgres_endpoint" {
    value = aws_db_instance.postgres.endpoint
}

output "ecr_repository_greekly_api_endpoint" {
    value = aws_ecr_repository.greekly_api.repository_url
}