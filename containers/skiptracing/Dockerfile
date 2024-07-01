FROM public.ecr.aws/lambda/python:3.9

# Copy requirements.txt
COPY containers/skiptracing/requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python packages without cache
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy function code
COPY containers/skiptracing/lambda_function.py ${LAMBDA_TASK_ROOT}
COPY utils ${LAMBDA_TASK_ROOT}/utils

# Pass the name of the function handler as an argument to the runtime
CMD [ "lambda_function.handler" ]