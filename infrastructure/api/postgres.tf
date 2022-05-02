resource "aws_db_instance" "postgres" {
  identifier             = "postgres"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "14.2"
  username               = "greekly"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.id
  vpc_security_group_ids = [aws_security_group.rds_sg.id, aws_security_group.ecs_sg.id]
  publicly_accessible    = true
  skip_final_snapshot    = true
}