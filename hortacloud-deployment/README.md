# hortacloud-deployment

Dockerfile to build an image for deployment of hortacloud

## Usage
Refer to hortacloud [deployment instructions](https://hortacloud.janelia.org/docs/administration/aws/deployment/) for detailed steps
### Container setup
- From your local machine, generate temporary aws credentials by running `aws sts get-session-token`. Note the **AWS_ACCESS_KEY_ID**, **AWS_SECRET_ACCESS_KEY** and **AWS_SESSION_TOKEN** values from the output.
- Create a folder with the format **horta_build_YYYYMMDD**. i.e. horta_build_20240314 
- Run `docker run --name hortacloud-deployment -v horta_build_YYYYMMDD:/horta_build_YYYYMMDD -it ghcr.io/allenneuraldynamics/hortacloud-deployment:latest bash` to run a container interactively. This also mounts the local folder to the container. 
- After the interactive shell begins, export AWS credentials environment variables using the values from the step above.
- Run `git clone **https://github.com/JaneliaSciComp/hortacloud/**`
- Open the cloned **hortacloud** folder and create/copy the **.env** file that contains all the required environment variables. If the **.env** variable is stored in a bucket, you can run `aws s3 cp s3://BUCKET_NAME/.env .env` to download it.
### Horta deployment
- Follow the hortacloud deployment instructions for the remaining steps.
### Horta upgrade
- Run `npm install`
- Run `npm run setup -- -i`
- Run `npm run destroy`
- Follow the hortacloud deployment instructions for the remaining steps.
