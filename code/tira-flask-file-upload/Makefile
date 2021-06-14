VERSION := 0.0.1
.PHONY:test

build-docker-image:
	docker image build -t mam10eks/tira-flask-file-upload:${VERSION} .
	docker image tag mam10eks/tira-flask-file-upload:${VERSION} mam10eks/tira-flask-file-upload:latest

upload-docker-image:
	docker login && \
	docker push mam10eks/tira-flask-file-upload:${VERSION} && \
	docker push mam10eks/tira-flask-file-upload:latest

run:
	@sudo rm -Rf tmp-out/* \
	&& mkdir -p ${PWD}/tmp-out/toy-dataset \
	&& mkdir -p ${PWD}/tmp-out/test-dataset \
	&& mkdir -p ${PWD}/tmp-out/softwares \
	&& sudo chmod 777 -R ${PWD}/tmp-out \
	&& docker run --rm -ti -p 5000:5000 -u 1010:1010 \
		-v ${PWD}/tmp-out/toy-dataset:/mnt/ceph/tira/data/runs/scai-qrecc21-toy-dataset-2021-05-15/ \
		-v ${PWD}/tmp-out/test-dataset:/mnt/ceph/tira/data/runs/scai-qrecc21-test-dataset-2021-05-15/ \
		-v ${PWD}/tmp-out/softwares:/mnt/ceph/tira/model/softwares/scai-qrecc/ \
		-v ${PWD}:/app \
		mam10eks/tira-flask-file-upload:latest

test:
	@docker run --rm -ti \
		-v ${PWD}:/app \
		-v ${PWD}/test/test-resources/:/mnt/ceph/tira/model/softwares/:ro \
		mam10eks/tira-flask-file-upload:${VERSION} nosetests


k8s-deploy:
	kubectl -n webisservices apply -f k8s-tira-flask-file-upload.yaml

