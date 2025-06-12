# AI-Mlops-Kafka-Project

You have to create Ec2 Instance than create EKS Cluster 
---- CMD ----

AWSCLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
aws configure
 
 
KUBECTL
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin
kubectl version --short --client
 
EKSCTL
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
 
 
eksctl create cluster --name demo-eks1 --region ap-south-1 --nodegroup-name my-nodes --node-type t2.large --managed --nodes 2
eksctl get cluster --name demo-eks1 --region ap-south-1
aws eks update-kubeconfig --name demo-eks1 --region ap-south-1


eksctl utils associate-iam-oidc-provider \
--region ap-south-1 \
--cluster demo-eks1 \
--approve

eksctl create iamserviceaccount \
--name ebs-csi-controller-sa \
--namespace kube-system \
--cluster demo-eks1 \
--attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
--approve \
--role-name AmazonEKS_EBS_CSI_DriverRole \
--override-existing-serviceaccounts

GO to EKS Cluster --> Add on EBS --> create it attach RBAC which we created 


create sc.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer


kubectl patch storageclass ebs-sc -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

Download Strimzi of kubernetes 
-- kubectl create namespace kafka
-- kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
-- kubectl apply -f https://strimzi.io/examples/latest/kafka/kafka-single-node.yaml -n kafka 
-- kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka 

# kubectl get pods -n kafka
# kubectl get nodes
# apply the deployment files and kafka and kowl 



