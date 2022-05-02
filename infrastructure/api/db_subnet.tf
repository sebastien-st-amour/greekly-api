resource "aws_db_subnet_group" "db_subnet_group" {
    subnet_ids  = [aws_subnet.pub_subnet_1.id, aws_subnet.pub_subnet_2.id]
}