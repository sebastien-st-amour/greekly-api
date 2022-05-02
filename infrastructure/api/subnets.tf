resource "aws_subnet" "pub_subnet_1" {
    vpc_id                  = aws_vpc.vpc.id
    cidr_block              = "10.0.0.0/24"
    availability_zone       = "ca-central-1a"
}

resource "aws_subnet" "pub_subnet_2" {
    vpc_id                  = aws_vpc.vpc.id
    cidr_block              = "10.0.1.0/24"
    availability_zone       = "ca-central-1b"
}