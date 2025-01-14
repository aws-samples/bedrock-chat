import * as path from 'path';
import { spawnSync } from 'child_process';
import { PythonFunction, PythonFunctionProps } from "@aws-cdk/aws-lambda-python-alpha";
import { Construct } from 'constructs';

export class ValidatedPythonFunction extends PythonFunction {
  constructor(scope: Construct, id: string, props: PythonFunctionProps) {
    // Run validation during synthesis
    const validateScript = path.join(__dirname, '../../validate-python.sh');
    const result = spawnSync('bash', [validateScript], {
      stdio: 'inherit',
      shell: true
    });

    if (result.status !== 0) {
      throw new Error('Python validation failed during synthesis');
    }

    // Create the Lambda function only if validation passes
    super(scope, id, props);
  }
}
