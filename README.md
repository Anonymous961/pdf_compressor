# PDF compressor Flask server

This is the backend of PDFLite, which primarily offers three main features.

1. Compress PDF

   1. This feature uses `ghostscript`.
   1. There are quality such as `screen`, `ebook`, `printer`, `prepress`.

2. Convert PDF to DOC
3. Compress img

   1. Accepts any image type
   2. There are quality range from 0 to 100.

      - Best quality is between 20 to 80

## Setup local development evironment

### Prerequisites

1. python3
2. ghostscript
3. AWS account with S3 bucket

### Setup virtual environment

```py
$ mkdir myproject
$ cd myproject
$ python3 -m venv .venv
```

- To activate virtual environment

```py
$ . .venv/bin/activate
```

- install dependencies

```py
$ pip install -r requirement.txt
```

### Create `.env` file

```py
# in .env file

AWS_BUCKET_NAME=your_bucket_name
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DOMAIN=http://your_bucket_name.s3.amazonaws.com/
```

- To run flask server

```py
$ flask --debug run
```

## Setup S3 bucket for public access

Bucket policy should look like this

```
{
    "Version": "2012-10-17",
    "Id": "IDxyz",
    "Statement": [
        {
            "Sid": "Stmt731289371238",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<bucketname>/<key>"
        }
    ]
}
```

- You can get policy examples from [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
- Or you can generate policy from [here](https://awspolicygen.s3.amazonaws.com/policygen.html)
- **NOTE:** untick block public access.

### File access

- Files uploaded to a S3 bucket can be accessed via a public URL that usually looks like this:

```py
https://nextagram-backend.s3.amazonaws.com/nextagram.jpg
https://<bucket_name>.s3.amazonaws.com/<filename>.<extension>
```
