resource "aws_db_subnet_group" "pm-db" {
  name_prefix = "pm"
  subnet_ids = [
    data.aws_subnet.subnet1.id,
    data.aws_subnet.subnet2.id,
  ]
}
