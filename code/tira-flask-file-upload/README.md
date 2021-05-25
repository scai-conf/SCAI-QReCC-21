# Tira Flask File Upload

## How to manualy upload a file

- In [app.py](app.py) manipulate the method `vm_name` to always return your `"<VM-NAME>"`
- Execute `make run` to start the upload server locally
- Navigate to [localhost:5000/run-upload-scai-qrecc21](localhost:5000/run-upload-scai-qrecc21) in your browser and upload the run file.
- Now you should have something like `tmp-out/<VM-NAME>/2021-05-25-09-03-43/` in your filesystem (Optionally, double check that the md5 sum is correct)
- Mount ceph: `sudo  mount /mnt/ceph/tira/`
- Go to: `/mnt/ceph/tira/model/softwares/scai-qrecc`
  - Check if there is already a directory `<VM-NAME>`. if not, continue (in case there is already such a directory and a associated software.prototext, please adjust the software accordingly.
  - Copy the content of `tmp-out/softwares/scai-qrecc/<VM-NAME>` to `/mnt/ceph/tira/model/softwares/scai-qrecc/<VM-NAME>`
  - Adapt the permissions accordingly: `sudo chown 1010:1010 -R <VM-NAME>`  and `sudo chmod 775 <VM-NAME>`
- Go to: `/mnt/ceph/tira/data/runs/scai-qrecc21-test-dataset-2021-05-15`
  - Copy the content of `tmp-out/<VM-NAME>` to `/mnt/ceph/tira/data/runs/scai-qrecc21-test-dataset-2021-05-15`
  - Adapt the permissions accordingly: `sudo chown 1010:1010 -R <VM-NAME>`  and `sudo chmod -R 775 <VM-NAME>`
- Go to the TIRA UI to check that everything looks fine: https://www.tira.io/task/scai-qrecc/user/<VM-NAME>
