build-docker-image:
	docker image build -t mam10eks/tira-flask-file-upload:0.0.1 .
	docker image tag mam10eks/tira-flask-file-upload:0.0.1 mam10eks/tira-flask-file-upload:latest

upload-docker-image:
	docker login && \
	docker push mam10eks/tira-flask-file-upload:0.0.1 && \
	docker push mam10eks/tira-flask-file-upload:latest

run:
	docker run --rm -ti -p 5000:5000 -u 1010:1010 -v ${PWD}/tmp-out:/mnt/ceph/tira/data/runs/scai-qrecc21-toy-dataset-2021-05-15/ -v ${PWD}:/app tira-flask-file-upload:latest


k8s-deploy:
	kubectl -n webisservices apply -f k8s-tira-flask-file-upload.yaml

