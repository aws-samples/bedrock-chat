# Docker Compose Setup for Backend API

This README provides instructions on how to use the provided `docker-compose.yml` file to set up and run the backend API service, including AWS credential setup and Docker Compose commands.

---

## Prerequisites

- **Docker**: Ensure Docker is installed and running on your system.
- **AWS CLI**: Required for managing AWS credentials.
- **jq**: A command-line JSON processor used in the Zsh function for handling AWS credentials.

---

## Setup Instructions

### Clone the Repository

```bash
git clone git@github.com:ai-trails/bedrock-claude-chat.git
cd bedrock-claude-chat
```

### AWS Credentials Setup

1. Add the following function to your `.zshrc` or `bashrc` file to dynamically load AWS credentials:

    ```bash
    setssocredentials() {
        local profilename="${1:-your-default-profile}" # Default profile

        # Fetch credentials using AWS CLI
        local credentials=$(aws configure export-credentials --profile "$profilename" 2>/dev/null)

        # Validate credentials
        if [ -z "$credentials" ]; then
            echo "Error: Failed to fetch credentials for profile '$profilename'."
            return 1
        fi

        # Export credentials
        export AWS_ACCESS_KEY_ID=$(echo "$credentials" | jq -r '.AccessKeyId')
        export AWS_SECRET_ACCESS_KEY=$(echo "$credentials" | jq -r '.SecretAccessKey')
        export AWS_SESSION_TOKEN=$(echo "$credentials" | jq -r '.SessionToken')

        echo "AWS credentials loaded for profile '$profilename'."
    }
    ```

2. Reload the `.zshrc` or `.bashrc` file:

    ```bash
    source ~/.zshrc
    ```

3. Use the function to load credentials and ensure `aws sso login --profile profilename` is completedfor a specific profile:

    ```bash
    setssocredentials profilename
    ```
4. Generate the environment variables from the .env-backend.local and .env-frontend.local files.

    ```bash
    ./generate-env.sh
    ```

### Run Docker Compose

1. Build and start the services:

    ```bash
    docker-compose up --build
    ```
    In daemon mode:
    ```bash
    docker-compose up --build -d
    ```

2. Access the backend API service at:

    ```
    http://localhost:8000
    ```

3. Stop the services:

    ```bash
    docker-compose down
    ```

---

## Docker Compose Commands

### Build and Start Services

```bash
docker-compose up --build
```

### Start Services Without Rebuilding

```bash
docker-compose up
```

### Stop Services

```bash
docker-compose down
```

---

## AWS CLI Login Command

To log in using an AWS CLI profile:

```bash
aws sso login --profile profilename
```

Replace `profilename` with the desired AWS profile name.

---

## Troubleshooting

1. **Check Docker Logs**:
   If services fail to start, view the logs:

   ```bash
   docker-compose logs
   ```

2. **Verify AWS Credentials**:
   Ensure the AWS CLI is configured correctly:

   ```bash
   aws configure list-profiles
   ```

3. **Install Missing Tools**:
   If `jq` is missing:

   ```bash
   sudo apt install jq      # Ubuntu/Debian
   brew install jq          # macOS
   

