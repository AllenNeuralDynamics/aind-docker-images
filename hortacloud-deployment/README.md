# hortacloud-deployment

Dockerfile to build an image for deployment of hortacloud

## Usage
Refer to hortacloud [deployment instructions](https://hortacloud.janelia.org/docs/administration/aws/deployment/) for detailed steps
### Container setup
- Run `docker pull ghcr.io/allenneuraldynamics/hortacloud-deployment:latest hortacloud` to pull the docker image.
- Run `docker run -it hortacloud bash` to run a container interactively.
### Horta deployment
- From your local machine, generate temporary aws credentials by running `aws sts -get-session-token`. Note the **AWS_ACCESS_KEY_ID**, **AWS_SECRET_ACCESS_KEY** and **AWS_SESSION_TOKEN** values from the output.
- Set up AWS credentials environment variables using the values from the the previous step.
- Run `git clone **https://github.com/JaneliaSciComp/hortacloud/**.
- In the cloned **hortacloud** folder, create/copy the **.env** file that contains all the required environment variables. If the **.env** variable is stored in a bucket, you can run `aws s3 cp s3://BUCKET_NAME/.env .env` to download it.

