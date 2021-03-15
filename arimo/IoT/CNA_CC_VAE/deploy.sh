export AWS_ACCOUNT=$(aws sts get-caller-identity | jq -r '.Account')
export AWS_DEFAULT_REGION=ap-northeast-1

$(aws ecr get-login --no-include-email)

docker build -t cn_coldchain .
docker tag cn_coldchain:latest ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/cn_coldchain:latest
docker push ${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/cn_coldchain:latest
