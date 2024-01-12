# hortacloud-deployment

Dockerfile to build an image for deployment of hortacloud

## Usage
Refer to hortacloud [deployment instruction](https://hortacloud.janelia.org/docs/administration/aws/deployment/) for detailed steps
### Container setup
- Create a **.env** file that contains all required environment variables.
- Run `docker build .` to build a docker image.
- Once an image is built, run `docker images` to list the image and note the image id.
- Run `docker run it IMAGE_ID bash` to run a container interactively.
### Horta deployment
- 


