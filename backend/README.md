
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `poetry run cdk ls`          list all stacks in the app
 * `poetry run cdk synth`       emits the synthesized CloudFormation template
 * `poetry run cdk deploy`      deploy this stack to your default AWS account/region
 * `poetry run cdk diff`        compare deployed stack with current state
 * `poetry run cdk docs`        open CDK documentation

Enjoy!
